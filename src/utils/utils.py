import os
from htmlblock import BLOCK_CHILDREN_MAP, BlockType
from utils.block_checker import get_block_type
from nodes.htmlnode import HTMLNode, LeafNode, ParentNode
from utils.node_utils import str_to_textnodes, textnode_to_leafnode
from utils.str_utils import format_block, md_to_blocks, extract_title


def md_to_htmlnode(md: str) -> HTMLNode:
    blocks = md_to_blocks(md)
    block_nodes = []
    for block in blocks:
        block_type = get_block_type(block)
        formatted_block = format_block(block, block_type)
        parent_nodes = []
        if block_type == BlockType.CODE:
            # code block is the leaf node
            leaf_node = LeafNode(
                tag=BLOCK_CHILDREN_MAP[block_type], value=formatted_block
            )
            block_nodes.append(ParentNode(tag=block_type.value, children=[leaf_node]))
            continue
        for line in formatted_block.split("\n"):
            inline_textnodes = str_to_textnodes(line)
            leaf_nodes = [
                textnode_to_leafnode(inline_textnodes)
                for inline_textnodes in inline_textnodes
            ]
            parent_node = HTMLNode(
                tag=BLOCK_CHILDREN_MAP[block_type], children=leaf_nodes
            )
            parent_nodes.append(parent_node)

        parent_node = ParentNode(tag=block_type.value, children=parent_nodes)
        block_nodes.append(parent_node)

    return HTMLNode(tag="div", children=block_nodes)


SRC_MD_PATH, DST_HTML_PATH = "content/index.md", "public/index.html"
TEMPLATE_PATH = "template.html"


def generate_page(
    src_md_path: str = SRC_MD_PATH,
    dst_html_path: str = DST_HTML_PATH,
    html_template_path: str = TEMPLATE_PATH,
) -> None:
    src_file = open(src_md_path, "r").read()
    template_file = open(html_template_path, "r").read()
    src_html_str = md_to_htmlnode(src_file).to_html()
    title = extract_title(src_file)
    final_html_str = template_file.replace("{{ Content }}", src_html_str).replace(
        "{{ Title }}", title
    )
    if os.path.exists(dst_html_path):
        print(f"{dst_html_path} already exists, removing it")
        ...
    os.makedirs(os.path.dirname(dst_html_path), exist_ok=True)
    with open(dst_html_path, "w") as f:
        print(f"abs path is {os.path.abspath(dst_html_path)}")
        print(f"Writing to {dst_html_path}")
        f.write(final_html_str)


def generate_pages(
    src_dir: str, dst_dir: str, template_path: str = TEMPLATE_PATH
) -> None:
    dir_content = os.listdir(src_dir)
    for content in dir_content:
        content_path = os.path.join(src_dir, content)
        if os.path.isdir(content_path):
            generate_pages(
                os.path.join(src_dir, content),
                os.path.join(dst_dir, content),
            )
        elif content.endswith(".md"):
            generate_page(
                src_md_path=content_path,
                dst_html_path=os.path.join(dst_dir, content[:-3] + ".html"),
                html_template_path=template_path,
            )
