from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code_block"
    QUOTE = "quote_block"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
