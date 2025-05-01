import re
from htmlblock import BlockType
from utils import LINE_REGEX, INLINE_REGEX
from type import LineType, InlineTextType

NEW_LINE_CHAR = "{{new_line}}"


class MarkdownParser:
    def __init__(self): ...

    def get_line_type(self, md: str) -> LineType:
        for line_type, regex in LINE_REGEX.items():
            if regex.match(md):
                return line_type
        return LineType.NONE

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
        return md

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

            if not line:
                # empty line means new block
                ...
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
