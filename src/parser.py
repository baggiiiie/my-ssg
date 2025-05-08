import re
from htmlblock import BlockType
from utils import LINE_REGEX, INLINE_REGEX
from type import LineType, InlineTextType
from htmlblock import BLOCK_CHILDREN_MAP

NEW_LINE_CHAR = "{{new_line}}"
INLINE_CODE_PLACE_HOLDER = "${{PLACEHOLDER}}$"


class MarkdownParser:
    def __init__(self):
        self.final_html_string = ""
        self.reset_block()

    def get_line_type(self, md: str) -> LineType:
        for line_type, regex in LINE_REGEX.items():
            if regex.match(md):
                return line_type
        return LineType.NORMAL

    def trailing_space_handler(self, md: str) -> str:
        if md.endswith("  "):
            md = md.strip() + NEW_LINE_CHAR
        else:
            md = md.strip() + " "
        return md

    def inline_parser(self, md: str) -> str:
        # deal with inline text
        inline_code_blocks = []
        code_match_pattern, code_replace_pattern = INLINE_REGEX[
            InlineTextType.INLINE_CODE
        ]

        def inline_code_replace(md: str) -> str:
            md = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            inline_code_blocks.extend(re.findall(code_match_pattern, md))
            return code_match_pattern.sub(INLINE_CODE_PLACE_HOLDER, md)

        def restore_inline_code(md: str) -> str:
            for inline_code in inline_code_blocks:
                md = md.replace(
                    INLINE_CODE_PLACE_HOLDER,
                    code_replace_pattern.format(inline_code),
                    1,
                )
            return md

        md = inline_code_replace(md)
        for _, regex in INLINE_REGEX.items():
            match_pattern, repalce_pattern = regex
            md = match_pattern.sub(repalce_pattern, md)
        if inline_code_blocks:
            md = restore_inline_code(md)
        md = md.replace(NEW_LINE_CHAR, "<br>")
        return md

    def reset_block(self) -> None:
        # let's treat them all as string now
        self.current_block_type: BlockType = BlockType.PARAGRAPH
        self.current_block_content: list = []
        self.others = ""

    def add_to_html_string(self) -> None:
        tag = self.current_block_type.value
        content = self.current_block_content
        if not content:
            return
        parent_content = ""
        for line in content:
            if self.current_block_type != BlockType.CODE:
                line = self.inline_parser(line)
            # else:
            #     line = repr(line).strip("'")
            if child_tag := BLOCK_CHILDREN_MAP[self.current_block_type].value:
                # TODO: code shouldn't be striped by `line.strip()`
                line = f"<{child_tag}>{line.strip()}</{child_tag}>"
            parent_content += line
        if self.current_block_type == BlockType.CODE:
            self.final_html_string += rf"<{tag}>{parent_content.strip()}</{tag}>"
        else:
            self.final_html_string += f"<{tag}>{parent_content.strip()}</{tag}>"

    def line_parse(self, md: str) -> str:
        # from md to html
        # 1. read line by line
        # 2. determine the type of line, save to state
        # 3. if block, don't format, don't convert inline
        # 4. else, format trailing spaces, convert inline
        # 5. convert to html: add tags
        for line in md.split("\n"):
            line_type = self.get_line_type(line)

            if self.current_block_type == BlockType.CODE:
                if not self.current_block_content:
                    self.current_block_content.append("")
                if line_type != LineType.CODE_END:
                    self.current_block_content[0] += line + "\n"
                    continue
                self.add_to_html_string()
                self.reset_block()
                continue

            if not line or line.isspace():
                # empty line means new block (other than code block)
                # append current block to final html string
                # start new block
                self.add_to_html_string()
                self.reset_block()
                continue

            elif line_type == LineType.CODE_START:
                self.add_to_html_string()
                self.reset_block()
                self.current_block_type = BlockType.CODE
                self.others = line.strip()[3:]
                continue

            elif line_type == LineType.HEADING:
                parts = line.split(" ", 1)
                heading_level = len(parts[0])
                tag = f"h{heading_level}"
                # manually add first to deal with heading level
                # self.current_block_type = BlockType.HEADING
                self.current_block_content.append(parts[1].strip())
                self.final_html_string += f"<{tag}>{self.inline_parser(self.current_block_content[0])}</{tag}>"
                # self.add_to_html_string()
                self.reset_block()
                continue
            elif line_type == LineType.QUOTE:
                # TODO: we can definitely use regex's matching group to do this
                # string extraction, like $1 $2 etc, instead of this kind of
                # line.split
                line = self.trailing_space_handler(line)
                line = line.split(" ", 1)[1]
                self.current_block_type = BlockType.QUOTE
                # TODO: this doesn't seem too ideal to me
                if not self.current_block_content:
                    self.current_block_content.append(line)
                else:
                    self.current_block_content[0] += line
                continue
            elif line_type in (
                LineType.ORDERED_LIST_ITEM,
                LineType.UNORDERED_LIST_ITEM,
            ):
                # TODO: need to check indent level, the strip() here wouldn't work
                line = line.strip().split(" ", 1)[1]
                if line_type == LineType.ORDERED_LIST_ITEM:
                    self.current_block_type = BlockType.ORDERED_LIST
                else:
                    self.current_block_type = BlockType.UNORDERED_LIST
                self.current_block_content.append(line)
                continue
            elif line_type == LineType.HORIZONTAL_RULE:
                self.add_to_html_string()
                self.reset_block()
                continue
            else:
                line = self.trailing_space_handler(line)
                self.current_block_type = BlockType.PARAGRAPH
                self.current_block_content.append(line)

        self.add_to_html_string()
        return self.final_html_string


if __name__ == "__main__":
    md = """
1. list   
2. list
"""
    # __AUTO_GENERATED_PRINT_VAR_START__
    print(rf" md: {md}")  # __AUTO_GENERATED_PRINT_VAR_END__
    result = MarkdownParser().line_parse(md.strip())
    print(result)
