import unittest

from nodes.textnode import TextNode, TextType
from utils.node_utils import textnode_to_leafnode


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_textnode_no_tag(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = textnode_to_leafnode(node)
        self.assertEqual(html_node.tag, "")
        self.assertEqual(html_node.value, "This is a text node")

    def test_textnode_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = textnode_to_leafnode(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_textnode_invalid_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = textnode_to_leafnode(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
