from typing import ParamSpec
from src.htmlblock import BlockChildrenType, BlockType, BLOCK_CHILDREN_MAP
from src.utils.block_checker import get_block_type
from src.nodes.htmlnode import HTMLNode, LeafNode, ParentNode
from src.utils.node_utils import str_to_textnodes, textnode_to_leafnode
from src.utils.str_utils import format_block, md_to_blocks, trailing_spaces_to_new_line


def md_to_htmlnode(md: str) -> HTMLNode:
    # split by `\n\n`
    blocks = md_to_blocks(md)
    block_nodes = []
    for block in blocks:
        block_type = get_block_type(block)
        block = format_block(block, block_type)
        parent_nodes = []
        for line in block.split("\n"):
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
                parent_node = LeafNode(tag=None, value=line)
            parent_nodes.append(parent_node)

        parent_node = ParentNode(tag=block_type.value, children=parent_nodes)
        block_nodes.append(parent_node)

    leaf_node = HTMLNode(tag="div", children=block_nodes)
    return leaf_node

    # if BLOCK_CHILDREN_MAP[block_type]:
    #     print(block_type)
    #     print(BLOCK_CHILDREN_MAP[block_type])
    #     children_nodes = [
    #         ParentNode(
    #             tag=BLOCK_CHILDREN_MAP[block_type].value,
    #             children=children_nodes,
    #         )
    #     ]
    #     parent_node = ParentNode(
    #         tag=block_type.value,
    #         children=children_nodes,
    #     )
    #     parent_nodes.append(parent_node)
    #
    # if block_type == BlockType.CODE:
    #     child_node = LeafNode(tag="code", value=block)
    #     block_nodes.append(ParentNode(tag="pre", children=[child_node]))
    #     continue
    # elif block_type == BlockType.UNORDERED_LIST:
    #     children_nodes = parent_nodes
