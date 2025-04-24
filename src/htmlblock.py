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


class BlockChildrenType(Enum):
    PARAGRAPH = None
    HEADING = None
    CODE = "code"
    QUOTE = None
    UNORDERED_LIST = "li"
    ORDERED_LIST = "li"


BLOCK_CHILDREN_MAP = {
    BlockType.PARAGRAPH: BlockChildrenType.PARAGRAPH.value,
    BlockType.HEADING: BlockChildrenType.HEADING.value,
    BlockType.CODE: BlockChildrenType.CODE.value,
    BlockType.QUOTE: BlockChildrenType.QUOTE.value,
    BlockType.UNORDERED_LIST: BlockChildrenType.UNORDERED_LIST.value,
    BlockType.ORDERED_LIST: BlockChildrenType.ORDERED_LIST.value,
}
