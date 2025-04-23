from src.utils.block_checker import get_block_type
from src.nodes.htmlnode import HTMLNode, ParentNode
from src.utils.node_utils import str_to_textnodes, textnode_to_leafnode
from src.utils.str_utils import format_block, md_to_blocks


def md_to_htmlnode(md: str) -> HTMLNode:
    # converts a full markdown string into a single parent HTMLNode
    # convert md to blocks
    # for each block, convert to textnodes
    # for each textnode, convert to LeafNode
    # put LeafNodes (inline) into ParentNode (block)
    # put ParentNode (block) into HTMLNode (document)
    # return a single parent HTMLNode
    # convert md to blocks
    blocks = md_to_blocks(md)
    block_nodes = []
    for block in blocks:
        # get block type
        block_type = get_block_type(block)
        # format block based on block type
        block = format_block(block, block_type)
        # convert block to text node based on block type
        text_nodes = str_to_textnodes(block)
        inline_nodes = []
        for text_node in text_nodes:
            # convert text node to html node
            leaf_node = textnode_to_leafnode(text_node)
            inline_nodes.append(leaf_node)

        block_nodes.append(ParentNode(tag=block_type.value, children=inline_nodes))

    leaf_node = HTMLNode(tag="div", children=block_nodes)
    return leaf_node
