import unittest

from textnode import TextNode, TextType
from utils import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


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
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "this is text with an ![image](https://i.imgur.com/zjjcjkz.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcjkz.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "this is text with an ![image](https://i.imgur.com/zjjcjkz.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_links(self):
        text = "this is [link](test) text with an ![image](https://i.imgur.com/zjjcjkz.png)"
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcjkz.png")], img_matches
        )
        self.assertListEqual([("link", "test")], link_matches)


if __name__ == "__main__":
    unittest.main()
