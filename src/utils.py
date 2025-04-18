import re
from textnode import TextType
from htmlnode import LeafNode
from textnode import TextNode

DELIMITER_TO_TEXTTYPE_MAPPING = {
    "`": TextType.CODE,
    "*": TextType.ITALIC,
    "_": TextType.ITALIC,
    "**": TextType.BOLD,
    "__": TextType.BOLD,
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


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    # TODO: include nested delimiter, meaning we should have parent and children TextNode?
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
                new_nodes.append(TextNode(content, TextType.TEXT))
            else:
                new_nodes.append(TextNode(content, text_type))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    # Returning [(anchor, URL)]
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
    return matches


def extract_markdown_image(text: str) -> list[tuple]:
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
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


def split_node_image(old_node: TextNode) -> list[TextNode]:
    text_type = TextType.IMAGE
    return split_node(old_node, text_type)


def split_node_link(old_node: TextNode) -> list[TextNode]:
    text_type = TextType.LINK
    return split_node(old_node, text_type)


if __name__ == "__main__":
    # Test the functions
    text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"

    node = TextNode(text, TextType.TEXT)
    new_nodes = split_node_image(node)
    new_nodes = split_node_link(node)
    print(new_nodes)
