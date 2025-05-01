import re
from src.nodes.htmlnode import LeafNode
from src.nodes.textnode import TextNode, TextType
from src.utils.str_utils import DELIMITER_TO_TEXTTYPE_MAPPING, split_nodes_delimiter


def textnode_to_leafnode(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode("", text_node.text)
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


def split_nodes_into_img_link(old_nodes: list[TextNode], text_type) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        new_node = split_node(node, text_type)
        new_nodes.extend(new_node)
    return new_nodes


def split_nodes_delimiters(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for delimiter, text_type in DELIMITER_TO_TEXTTYPE_MAPPING.items():
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        old_nodes = new_nodes
    return new_nodes


def str_to_textnodes(text: str | None) -> list[TextNode]:
    # take a markdown string and turn it into a list of TextNodes
    if not text:
        return []
    original = TextNode(text, TextType.TEXT)
    # NOTE: i don't need so many variables, but just keep them for now
    after_delimiter = split_nodes_delimiters([original])
    after_link = split_nodes_into_img_link(after_delimiter, TextType.LINK)
    after_image = split_nodes_into_img_link(after_link, TextType.IMAGE)

    return after_image


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
    if parts[0]:
        node_list.append(TextNode(parts[0], TextType.TEXT))
    node_list.append(TextNode(anchor, text_type, url))
    split_node(TextNode(parts[1], TextType.TEXT), text_type, node_list)
    return node_list
