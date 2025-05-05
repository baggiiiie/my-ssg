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


# TODO:
# actually for code block and blockquote, it's not really children tags
# for list, it's every child(line in block) has a tag for itself
# but for code, not every line in code block has a tag
# it's more like the parent has double tags


class BlockChildrenType(Enum):
    PARAGRAPH = None
    HEADING = None
    CODE = "code"
    QUOTE = "p"
    UNORDERED_LIST = "li"
    ORDERED_LIST = "li"


BLOCK_CHILDREN_MAP = {
    BlockType.PARAGRAPH: BlockChildrenType.PARAGRAPH,
    BlockType.HEADING: BlockChildrenType.HEADING,
    BlockType.CODE: BlockChildrenType.CODE,
    BlockType.QUOTE: BlockChildrenType.QUOTE,
    BlockType.UNORDERED_LIST: BlockChildrenType.UNORDERED_LIST,
    BlockType.ORDERED_LIST: BlockChildrenType.ORDERED_LIST,
}
