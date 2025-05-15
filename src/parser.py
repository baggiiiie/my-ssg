import os
import re
from htmlblock import BlockType
from utils.utils import LINE_REGEX, INLINE_REGEX
from type import LineType, InlineTextType
from htmlblock import BLOCK_CHILDREN_MAP
from utils.utils import extract_title

NEW_LINE_CHAR = "{{NEWLINECHAR}}"
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
            # md = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
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
                if line_type not in (LineType.CODE_START, LineType.CODE_END):
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
                line = line.split(">", 1)[1].lstrip()
                line = self.trailing_space_handler(line)
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
                # TODO: this hasn't been done
                self.add_to_html_string()
                self.reset_block()
                continue
            else:
                line = self.trailing_space_handler(line)
                self.current_block_type = BlockType.PARAGRAPH
                self.current_block_content.append(line)

        self.add_to_html_string()
        return self.final_html_string


SRC_MD_PATH, DST_HTML_PATH = "content/index.md", "public/index.html"
TEMPLATE_PATH = "template.html"


def generate_page(
    src_md_path: str = SRC_MD_PATH,
    dst_html_path: str = DST_HTML_PATH,
    html_template_path: str = TEMPLATE_PATH,
) -> None:
    src_str = open(src_md_path, "r").read()
    template_str = open(html_template_path, "r").read()
    src_html_str = MarkdownParser().line_parse(src_str)
    title = extract_title(src_str)
    output_html_str = template_str.replace("{{ Content }}", src_html_str).replace(
        "{{ Title }}", title
    )
    if os.path.exists(dst_html_path):
        os.remove(dst_html_path)
    os.makedirs(os.path.dirname(dst_html_path), exist_ok=True)
    with open(dst_html_path, "w") as f:
        print(f"abs path is {os.path.abspath(dst_html_path)}")
        print(f"Writing to {dst_html_path}")
        f.write(output_html_str)


def generate_pages(
    src_dir: str, dst_dir: str, template_path: str = TEMPLATE_PATH
) -> None:
    dir_content = os.listdir(src_dir)
    for content in dir_content:
        content_path = os.path.join(src_dir, content)
        if os.path.isdir(content_path):
            generate_pages(
                os.path.join(src_dir, content),
                os.path.join(dst_dir, content),
            )
        elif content.endswith(".md"):
            generate_page(
                src_md_path=content_path,
                dst_html_path=os.path.join(dst_dir, content[:-3] + ".html"),
                html_template_path=template_path,
            )