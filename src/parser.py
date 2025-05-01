from htmlblock import BlockType
from utils import LINE_REGEX_PATTERNS, INLINE_REGEX_PATTERNS
from type import LineType, InlineTextType

NEW_LINE_CHAR = "{{new_line}}"


class MarkdownParser:
    def __init__(self): ...

    def get_line_type(self, md: str) -> LineType:
        for line_type, regex in LINE_REGEX_PATTERNS.items():
            if regex.match(md):
                return line_type
        return LineType.NONE

    def get_inline_type(self, md: str) -> InlineTextType:
        for text_type, regex in INLINE_REGEX_PATTERNS.items():
            if regex.match(md):
                return text_type
        return InlineTextType.TEXT

    def trailing_space_handler(self, md: str) -> str:
        if md.endswith(" "):
            md = md.rstrip() + NEW_LINE_CHAR
        return ""

    def inline_parse(self, md: str) -> str:
        # deal with inline text
        for text_type, regex in INLINE_REGEX_PATTERNS.items():
            md = regex[0].sub(regex[1], md)
            return md
        return ""

    def line_parse(self, md: str) -> str:
        # from md to html
        # 1. read line by line
        # 2. determine the type of line, save to state
        # 3. if block, don't format, don't convert inline
        # 4. else, format trailing spaces, convert inline
        # 5. convert to html: add tags
        final_html_string = ""
        current_block = {
            "block_type": None,
            "content": "",
        }
        for line in md.split("\n"):
            if current_block["block_type"] == BlockType.CODE:
                # if it's within a code block, just return as is
                ...
                continue

            line_type = self.get_line_type(line)
            if line_type == LineType.CODE_START:
                current_block["block_type"] = BlockType.CODE
                code_block = {
                    "lang": line.strip()[3:],
                    "content": "",
                }
                continue
            if line_type == LineType.CODE_END:
                # TODO: convert to html string and save to result
                continue
            if line_type == LineType.HEADING:
                heading_level = len(line.strip().split(" ")[0])
                tag = LineType.HEADING.value + str(heading_level)
                # TODO: 1. get inline, 2. convert to html string and save to result
                ...
            if line_type == LineType.QUOTE:
                # TODO: 1. get inline, 2. convert to html string and save to result
                ...
            if line_type in (LineType.ORDERED_LIST_ITEM, LineType.UNORDERED_LIST_ITEM):
                # TODO: 1. get inline, 2. convert to html string and save to result
                ...
            if line_type == LineType.HORIZONTAL_RULE:
                ...
            if line_type == LineType.PARAGRAPH:
                line = self.trailing_space_handler(line)
                # TODO: convert to html string and save to result

        return ""
