from enum import Enum


class InlineTextType(Enum):
    TEXT = "normal_text"
    BOLD = "bold_text"
    ITALIC = "italic_text"
    INLINE_CODE = "inline_code"
    LINK = "link"
    IMAGE = "image"


class LineType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "pre"
    CODE_START = "code_start"
    CODE_END = "code_start"
    QUOTE = "blockquote"
    UNORDERED_LIST_ITEM = "ul"
    ORDERED_LIST_ITEM = "ol"
    HORIZONTAL_RULE = "hr"
    TABLE = "table"
    NONE = ""


class BlockChildrenType(Enum):
    PARAGRAPH = None
    HEADING = None
    CODE = "code"
    QUOTE = None
    UNORDERED_LIST = "li"
    ORDERED_LIST = "li"
