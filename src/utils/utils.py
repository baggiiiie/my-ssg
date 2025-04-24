from src.htmlblock import BLOCK_CHILDREN_MAP, BlockType
from src.utils.block_checker import get_block_type
from src.nodes.htmlnode import HTMLNode, LeafNode, ParentNode
from src.utils.node_utils import str_to_textnodes, textnode_to_leafnode
from src.utils.str_utils import format_block, md_to_blocks


def md_to_htmlnode(md: str) -> HTMLNode:
    blocks = md_to_blocks(md)
    block_nodes = []
    for block in blocks:
        block_type = get_block_type(block)
        formatted_block = format_block(block, block_type)
        parent_nodes = []
        if block_type == BlockType.CODE:
            leaf_node = LeafNode(tag="code", value=formatted_block)
            block_nodes.append(ParentNode(tag=block_type.value, children=[leaf_node]))
            continue
        for line in formatted_block.split("\n"):
            inline_textnodes = str_to_textnodes(line)
            children_nodes = []
            for inline_textnode in inline_textnodes:
                leaf_node = textnode_to_leafnode(inline_textnode)
                children_nodes.append(leaf_node)
            if BLOCK_CHILDREN_MAP[block_type]:
                parent_node = ParentNode(
                    tag=BLOCK_CHILDREN_MAP[block_type], children=children_nodes
                )
            else:
                parent_node = HTMLNode(tag=None, children=children_nodes)
            parent_nodes.append(parent_node)

        parent_node = ParentNode(tag=block_type.value, children=parent_nodes)
        block_nodes.append(parent_node)

    return HTMLNode(tag="div", children=block_nodes)
