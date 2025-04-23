import unittest

from src.textnode import TextNode, TextType
from src.utils import text_node_to_html_leaf_node


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_textnode_no_tag(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_textnode_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_textnode_invalid_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
