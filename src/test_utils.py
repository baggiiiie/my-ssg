import unittest

from textnode import TextNode, TextType
from utils import text_node_to_html_node, split_nodes_delimiter


class TestUtils(unittest.TestCase):
    def test_textnode_no_tag(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_textnode_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_textnode_invalid_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_textnodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes, expected)

    def test_split_textnodes_no_closing(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_textnodes_multiple_same(self):
        node = TextNode("This is `text with` a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text with", TextType.CODE),
            TextNode(" a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes, expected)

    # TODO: Need to add support for mixed delimiters
    # def test_split_textnodes_multiple_mixed(self):
    #     node = TextNode("This is *text with* a `code block` **word**", TextType.TEXT)
    #     new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    #     expected = [
    #         TextNode("This is ", TextType.TEXT),
    #         TextNode("text with", TextType.ITALIC),
    #         TextNode(" a ", TextType.TEXT),
    #         TextNode("code block", TextType.CODE),
    #         TextNode(" ", TextType.TEXT),
    #         TextNode("word", TextType.BOLD),
    #     ]
    #     self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
