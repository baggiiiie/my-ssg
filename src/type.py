from enum import Enum


class InlineTextType(Enum):
    TEXT = None
    BOLD = "b"
    ITALIC = "i"
    INLINE_CODE = "code"
    LINK = "link"
    IMAGE = "image"


class LineType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "pre"
    CODE_START = "code_start"
    CODE_END = "code_end"
    QUOTE = "blockquote"
    UNORDERED_LIST_ITEM = "ul"
    ORDERED_LIST_ITEM = "ol"
    HORIZONTAL_RULE = "hr"
    TABLE = "table"
    NORMAL = "normal"


class BlockChildrenType(Enum):
    PARAGRAPH = None
    HEADING = None
    CODE = "code"
    QUOTE = None
    UNORDERED_LIST = "li"
    ORDERED_LIST = "li"
