import unittest

from src.textnode import TextNode, TextType
from src.utils import (
    split_nodes_delimiter,
    split_nodes_delimiters,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
)


class TestUtils(unittest.TestCase):
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

    def test_split_textnodes_start(self):
        node = TextNode("`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes, expected)

    def test_split_textnodes_end(self):
        node = TextNode("word `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("word ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(len(new_nodes), 2)
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

    def test_split_textnodes_delimiters_with_space(self):
        node = TextNode(
            "This is a    `code block` and another `code block` word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiters([node])
        expected = [
            TextNode("This is a    ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and another ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 5, f"new nodes are {new_nodes}")
        self.assertEqual(new_nodes, expected, f"new nodes are {new_nodes}")

    def test_split_textnodes_same_delimiters(self):
        node = TextNode(
            "This is a `code block` and another `code block` word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiters([node])
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and another ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 5, f"new nodes are {new_nodes}")
        self.assertEqual(new_nodes, expected, f"new nodes are {new_nodes}")

    def test_split_textnodes_diff_delimiters(self):
        node = TextNode("This is *italic text* and a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiters([node])
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 5, f"new nodes are {new_nodes}")
        self.assertEqual(new_nodes, expected, f"new nodes are {new_nodes}")

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

    def test_split_node_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
