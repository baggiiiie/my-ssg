import re

from src.htmlblock import BlockType


def check_heading(md: str) -> bool:
    # NOTE: do i have to come back eventually to count???
    regex = r"^#{1,6} "
    match = re.match(regex, md)
    if match:
        return True
    return False


def check_code_block(md: str) -> bool:
    regex = r"```(.*?)\n([\s\S]*?)```"
    match = re.match(regex, md)
    if match:
        return True
    return False


def check_quote_block(md: str) -> bool:
    regex = r"^> .*"
    lines = md.split("\n")
    for line in lines:
        if not re.match(regex, line.strip()):
            return False
    return True


def check_unordered_list(md: str) -> bool:
    regex = r"^[-+*] .*"
    lines = md.split("\n")
    for line in lines:
        if not re.match(regex, line.strip()):
            return False
    return True


def check_ordered_list(md: str) -> bool:
    regex = r"^\d+\. .*"
    lines = md.split("\n")
    index = 1
    for line in lines:
        match = re.match(regex, line.strip())
        if not match:
            return False
        line_number = match.group(0).split(".", 2)[0]
        if line_number != str(index):
            return False
        index += 1

    return True


def get_block_type(markdown: str | None) -> BlockType:
    # takes in a single block of markdown text, return BlockType
    if not markdown:
        return BlockType.PARAGRAPH
    BLOCK_TYPE_CHECKER = {
        BlockType.HEADING: check_heading,
        BlockType.CODE: check_code_block,
        BlockType.QUOTE: check_quote_block,
        BlockType.ORDERED_LIST: check_ordered_list,
        BlockType.UNORDERED_LIST: check_unordered_list,
    }
    for block_type, checker in BLOCK_TYPE_CHECKER.items():
        if checker(markdown.strip()):
            return block_type
    return BlockType.PARAGRAPH
