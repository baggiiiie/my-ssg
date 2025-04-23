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
    # new_blocks = []
    return markdown.strip().split("\n\n")
    # for block in blocks:
    #     if not block or block.isspace():
    #         continue
    #     new_block = format_paragraph(block)
    #     new_blocks.append(new_block.strip())
    # return new_blocks


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


def format_paragraph(block: str | None) -> str:
    # paragraphs: deal with trailing spaces
    if not block:
        return ""
    lines = block.split("\n")
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


def format_others(md: str) -> str:
    # format the input md string
    # if it's a new line, it's a new line
    # no trailing spaces logic
    lines = md.split("\n")
    new_lines = []
    for line in lines:
        line = line.strip()
        new_lines.append(line)
    return "\n".join(new_lines)


def format_code(md: str) -> str:
    # format the input md string
    # if it's a new line, it's a new line
    # no trailing spaces logic
    lines = md.split("\n")[1:-2]
    new_lines = []
    for line in lines:
        line = line.strip()
        new_lines.append(line)
    formatted_line = "```" + "\n".join(new_lines) + "```"
    return formatted_line


def format_block(block: str | None, block_type=BlockType.PARAGRAPH) -> str | None:
    if not block:
        return None
    if block_type == BlockType.PARAGRAPH:
        block = format_paragraph(block)
    elif block_type == BlockType.CODE:
        block = format_code(block)
    else:
        block = format_others(block)
    return block.strip()
