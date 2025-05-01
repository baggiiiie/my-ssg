from htmlblock import BlockType
from nodes.textnode import TextType
from nodes.textnode import TextNode

DELIMITER_TO_TEXTTYPE_MAPPING = {
    "`": TextType.CODE,
    "**": TextType.BOLD,
    "__": TextType.BOLD,
    "*": TextType.ITALIC,
    "_": TextType.ITALIC,
}


def split_nodes_delimiter(
    old_nodes: list, delimiter: str, text_type: TextType
) -> list[TextNode]:
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
                if content:
                    new_nodes.append(TextNode(content, node.text_type))
            else:
                new_nodes.append(TextNode(content, text_type))
    return new_nodes


def md_to_blocks(markdown: str | None) -> list[str]:
    if not markdown:
        return []
    return markdown.strip().split("\n\n")


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


def format_heading(md: str) -> str:
    lines = md.split(" ", 2)[1]
    return lines


def format_block(block: str | None, block_type=BlockType.PARAGRAPH) -> str:
    if not block:
        return ""
    BLOCK_FORMAT_HELPER = {
        BlockType.PARAGRAPH: format_paragraph,
        BlockType.HEADING: format_heading,
        BlockType.CODE: format_code,
        BlockType.QUOTE: format_quote,
        BlockType.UNORDERED_LIST: format_list,
        BlockType.ORDERED_LIST: format_list,
    }
    format_func = BLOCK_FORMAT_HELPER.get(block_type, format_others)
    block = format_func(block).strip()

    return block or ""


def extract_title(md: str) -> str:
    # im only gonna get the first line to use it as title
    title = md.split("\n")[0]
    if title.startswith("# "):
        title = title[2:]
    return title
