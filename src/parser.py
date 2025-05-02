import re
from htmlblock import BlockType
from utils import LINE_REGEX, INLINE_REGEX
from type import LineType, InlineTextType

NEW_LINE_CHAR = "{{new_line}}"


class MarkdownParser:
    def __init__(self):
        self.final_html_string = ""
        self.reset_block()

    def get_line_type(self, md: str) -> LineType:
        for line_type, regex in LINE_REGEX.items():
            if regex.match(md):
                return line_type
        return LineType.NORMAL

    # def get_inline_type(self, md: str) -> InlineTextType:
    #     for text_type, regex in INLINE_REGEX_PATTERNS.items():
    #         if regex.match(md):
    #             return text_type
    #     return InlineTextType.TEXT

    def trailing_space_handler(self, md: str) -> str:
        if md.endswith(" "):
            md = md.rstrip() + NEW_LINE_CHAR
        return ""

    def inline_parser(self, md: str) -> str:
        # deal with inline text
        INLINE_CODE_PLACE_HOLDER = "${{PLACEHOLDER}}$"
        inline_code_blocks = []
        code_match_pattern, code_replace_pattern = INLINE_REGEX[
            InlineTextType.INLINE_CODE
        ]

        def inline_code_replace(md: str) -> str:
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
        for text_type, regex in INLINE_REGEX.items():
            match_pattern, repalce_pattern = regex
            md = match_pattern.sub(repalce_pattern, md)
        if inline_code_blocks:
            md = restore_inline_code(md)
        md.replace(NEW_LINE_CHAR, "<br>")
        return md

    def reset_block(self) -> None:
        # let's treat them all as string now
        self.current_block_type = BlockType.PARAGRAPH.value
        self.current_block_content = ""
        self.others = ""

    def add_to_html_string(self) -> None:
        tag = self.current_block_type
        content = self.current_block_content
        if not content:
            return
        if self.current_block_type != BlockType.CODE.value:
            content = self.inline_parser(content)
        # TODO: wrap parent tag
        # if need_parent_tag:
        #     ...
        self.final_html_string += f"<{tag}>{content}</{tag}>"

    def line_parse(self, md: str) -> str:
        # from md to html
        # 1. read line by line
        # 2. determine the type of line, save to state
        # 3. if block, don't format, don't convert inline
        # 4. else, format trailing spaces, convert inline
        # 5. convert to html: add tags
        for line in md.split("\n"):
            line_type = self.get_line_type(line)

            if self.current_block_type == BlockType.CODE.value:
                if line_type != LineType.CODE_END:
                    self.current_block_content += line
                    continue
                self.add_to_html_string()
                self.reset_block()
                continue

            if not line:
                # empty line means new block (other than code block)
                # append current block to final html string
                # start new block
                tag = self.current_block_type
                self.add_to_html_string()
                self.reset_block()
                continue

            if line_type == LineType.NORMAL:
                self.current_block_content += line
                continue
            # elif line_type == LineType.CODE_END:
            #     self.add_to_html_string()
            #     self.reset_block()
            #     continue
            elif line_type == LineType.CODE_START:
                self.add_to_html_string()
                self.reset_block()
                self.current_block_type = BlockType.CODE.value
                self.others = line.strip()[3:]
                continue

            elif line_type == LineType.HEADING:
                parts = line.split(" ", 1)
                heading_level = len(parts[0])
                tag = f"h{heading_level}"
                # manually add first to deal with heading level
                # self.current_block_type = BlockType.HEADING.value
                self.current_block_content += parts[1].strip()
                self.final_html_string += (
                    f"<{tag}>{self.inline_parser(self.current_block_content)}</{tag}>"
                )
                # self.add_to_html_string()
                self.reset_block()
                continue
            elif line_type == LineType.QUOTE:
                # TODO: 1. get inline, 2. convert to html string and save to result
                self.current_block_type = BlockType.QUOTE.value
                self.current_block_content += line.split(" ", 1)[1]
                continue
            elif line_type in (
                LineType.ORDERED_LIST_ITEM,
                LineType.UNORDERED_LIST_ITEM,
            ):
                # TODO: need to check indent level
                ...
                continue
            elif line_type == LineType.HORIZONTAL_RULE:
                self.add_to_html_string()
                self.reset_block()
                continue
            else:
                line = self.trailing_space_handler(line)
                # TODO: convert to html string and save to result
                self.current_block_type = BlockType.PARAGRAPH.value
                self.current_block_content += line

        self.add_to_html_string()
        return self.final_html_string


if __name__ == "__main__":
    md = "# hello world"
    # __AUTO_GENERATED_PRINT_VAR_START__
    print(f" md: {str(md)}")  # __AUTO_GENERATED_PRINT_VAR_END__
    result = MarkdownParser().line_parse(md)
    print(result)
