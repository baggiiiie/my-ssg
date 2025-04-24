import re
from src.htmlblock import BlockType
from src.nodes.textnode import TextType
from src.nodes.textnode import TextNode

DELIMITER_TO_TEXTTYPE_MAPPING = {
    "`": TextType.CODE,
    # i think i'll need to put BOLD before ITALIC?
    "**": TextType.BOLD,
    "__": TextType.BOLD,
    "*": TextType.ITALIC,
    "_": TextType.ITALIC,
}


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


def md_to_blocks(markdown: str | None) -> list[str]:
    if not markdown:
        return []
    return markdown.strip().split("\n\n")


# NOTE: this is only used in UT for now
def extract_markdown_images(text: str) -> list[tuple]:
    # Returning [(anchor, URL)]
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
    return matches


# NOTE: this is only used in UT for now
def extract_markdown_links(text: str) -> list[tuple]:
    # Returning [(anchor, URL)]
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_pattern, text)
    return matches


def trailing_spaces_to_new_line(lines: list) -> str:
    new_block = []
    current_line = ""
    for line in lines:
        if not line:  # remove empty lines
            continue
        if line.endswith("  "):
            line = line.strip()
            current_line += line + "\\n"
            continue

        # line doesn't end with 2 or more spaces, append a space and append next line
        current_line += line.strip() + " "
        new_block.append(current_line)
        current_line = ""
    return "".join(new_block)


def format_paragraph(block: str | None) -> str:
    # paragraphs: deal with trailing spaces
    if not block:
        return ""
    lines = block.split("\n")
    return trailing_spaces_to_new_line(lines)


def format_list(md: str) -> str:
    new_lines = []
    lines = md.split("\n")
    for line in lines:
        line = line.strip()[2:]
        new_lines.append(line)
    return "\n".join(new_lines)


def format_quote(md: str) -> str:
    # we wanna remove `> ` at the start of lines
    new_lines = []
    lines = md.split("\n")
    for line in lines:
        line = line.lstrip()
        line = line[2:]
        new_lines.append(line)
    return trailing_spaces_to_new_line(new_lines)


def format_others(md: str) -> str:
    # format the input md string
    # if it's a new line, it's a new line
    # no trailing spaces logic
    lines = md.split("\n")
    new_lines = []
    for line in lines:
        line = line.strip()
        new_lines.append(line)
    return "\\n".join(new_lines)


def format_code(md: str) -> str:
    # format the input md string
    # if it's a new line, it's a new line
    # no trailing spaces logic
    lines = md.split("\n")[1:-1]
    new_lines = []
    for line in lines:
        line = line.strip()
        new_lines.append(line)
    return "\\n".join(new_lines)


def format_block(block: str | None, block_type=BlockType.PARAGRAPH) -> str:
    if not block:
        return ""

    if block_type == BlockType.PARAGRAPH:
        block = format_paragraph(block)
    elif block_type == BlockType.CODE:
        block = format_code(block)
    elif block_type == BlockType.QUOTE:
        block = format_quote(block)
    elif block_type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
        block = format_list(block)
    else:
        block = format_others(block)
    return block.strip()
