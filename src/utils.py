import re
from htmlblock import BlockType
from textnode import TextType
from htmlnode import LeafNode
from textnode import TextNode

DELIMITER_TO_TEXTTYPE_MAPPING = {
    "`": TextType.CODE,
    # i think i'll need to put BOLD before ITALIC?
    "**": TextType.BOLD,
    "__": TextType.BOLD,
    "*": TextType.ITALIC,
    "_": TextType.ITALIC,
}


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Invalid text type")


def split_nodes_delimiter(
    old_nodes: list, delimiter: str, text_type: TextType
) -> list[TextNode]:
    # TODO: include nested delimiter, meaning we should have parent and children TextNode?
    # NOTE: TextNode could be broken into multiple TextNode
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        # TODO: deal with no closing delimiter
        contents = node.text.split(delimiter)
        # even number of length indicates no closing delimiter
        if len(contents) % 2 == 0:
            raise Exception("No closing delimiter")
        for index, content in enumerate(contents):
            # if index is odd, it's inside the delimiter
            if index % 2 == 0:
                # outside of the delimiter might not be text?
                if content:
                    new_nodes.append(TextNode(content, node.text_type))
            else:
                new_nodes.append(TextNode(content, text_type))
    return new_nodes


# NOTE: this is only used in UT for now
def split_nodes_delimiters(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for delimiter, text_type in DELIMITER_TO_TEXTTYPE_MAPPING.items():
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        old_nodes = new_nodes
    return new_nodes


# NOTE: this is only used in UT for now
def extract_markdown_images(text: str) -> list[tuple]:
    # Returning [(anchor, URL)]
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple]:
    # Returning [(anchor, URL)]
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_pattern, text)
    return matches


def find_pattern(pattern: str, text: str) -> tuple[str, str] | tuple[None, None]:
    match = re.search(pattern, text)
    if match:
        anchor, url = match.groups()
        return anchor, url
    return None, None


def split_node(
    old_node: TextNode, text_type: TextType, node_list: list[TextNode] | None = None
) -> list[TextNode]:
    # take 1 TextNode, find the first link
    # save before-link as TEXT and link as LINK in list
    # save the rest as another TextNode, pass into recursion
    if not node_list:
        node_list = []
    if text_type == TextType.LINK:
        regex_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        split_pattern = "[{}]({})"
    else:
        # IMAGE
        regex_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        split_pattern = "![{}]({})"

    anchor, url = find_pattern(regex_pattern, old_node.text)
    if not anchor:
        # no link found, return the original node
        if old_node.text:
            node_list.append(old_node)
        return [old_node]

    parts = old_node.text.split(split_pattern.format(anchor, url), 1)
    node_list.append(TextNode(parts[0], TextType.TEXT))
    node_list.append(TextNode(anchor, text_type, url))
    split_node(TextNode(parts[1], TextType.TEXT), text_type, node_list)
    return node_list


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    text_type = TextType.IMAGE
    new_nodes = []
    for node in old_nodes:
        new_node = split_node(node, text_type)
        new_nodes.extend(new_node)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    text_type = TextType.LINK
    new_nodes = []
    for node in old_nodes:
        new_node = split_node(node, text_type)
        new_nodes.extend(new_node)
    return new_nodes


def text_to_textnodes(text: str | None) -> list[TextNode]:
    # take a markdown string and turn it into a list of TextNodes
    if not text:
        return []
    original = TextNode(text, TextType.TEXT)
    # NOTE: i don't need so many variables, but just keep them for now
    after_delimiter = split_nodes_delimiters([original])
    after_link = split_nodes_link(after_delimiter)
    after_image = split_nodes_image(after_link)

    return after_image


def markdown_to_blocks(markdown: str | None) -> list[str]:
    # find block by \n\n delimiter
    # strip leading and trailing whitespace
    # remove empty block
    def format_paragraph(block: str | None) -> str:
        if not block:
            return ""
        lines = block.split("\n")
        new_block = []
        for line in lines:
            line = line.strip()
            if not line:  # remove empty lines
                continue
            new_block.append(line)
        return "\n".join(new_block)

    if not markdown:
        return []
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if not block:
            continue
        new_block = format_paragraph(block)
        new_blocks.append(new_block)
    return new_blocks


def check_heading(md: str) -> bool:
    # NOTE: do i have to come back eventaully to count???
    regex = r"^#{1,6} "
    match = re.match(regex, md)
    if match:
        return True
    return False


def check_code_block(md: str) -> bool:
    regex = r"^```.*?```$"
    match_start = re.match(regex, md)
    if match_start:
        return True
    return False


def check_quote_block(md: str) -> bool:
    regex = r"^> .*"
    lines = md.split("\n")
    for line in lines:
        if not re.match(regex, line):
            return False
    return True


def check_unordered_list(md: str) -> bool:
    regex = r"^[-+*] .*"
    lines = md.split("\n")
    for line in lines:
        if not re.match(regex, line):
            return False
    return True


def check_ordered_list(md: str) -> bool:
    regex = r"^\d+\. .*"
    lines = md.split("\n")
    index = 1
    for line in lines:
        match = re.match(regex, line)
        if not match:
            return False
        line_number = match.group(0).split(".", 2)[0]
        if line_number != str(index):
            return False
        index += 1

    return True


BLOCK_TYPE_CHECKER = {
    BlockType.HEADING: check_heading,
    BlockType.CODE: check_code_block,
    BlockType.QUOTE: check_quote_block,
    BlockType.ORDERED_LIST: check_ordered_list,
    BlockType.UNORDERED_LIST: check_unordered_list,
}


def block_to_block_type(markdown: str | None) -> BlockType:
    # takes in a single block of markdown text, return BlockType
    if not markdown:
        return BlockType.PARAGRAPH
    for block_type, checker in BLOCK_TYPE_CHECKER.items():
        if checker(markdown):
            return block_type
    return BlockType.PARAGRAPH


if __name__ == "__main__":
    md = "1. test\n2. test2"
    blocks = check_ordered_list(md)
    print(blocks)
