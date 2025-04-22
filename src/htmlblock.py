from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "pre"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"
    HORIZONTAL_RULE = "hr"
    TABLE = "table"
