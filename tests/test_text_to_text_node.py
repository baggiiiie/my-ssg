import unittest

from nodes.textnode import TextNode, TextType
from utils.node_utils import str_to_textnodes


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_to_textnodes_normal(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = str_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_empty(self):
        text = ""
        new_nodes = str_to_textnodes(text)
        self.assertEqual([], new_nodes)

    def test_text_to_textnodes_none(self):
        text = None
        new_nodes = str_to_textnodes(text)
        self.assertEqual([], new_nodes)

    def test_text_to_textnodes_broken_delimiter(self):
        text = "this is a broken ` code block"
        with self.assertRaises(Exception):
            str_to_textnodes(text)

    def test_text_to_textnodes_broken_delimiter_2(self):
        text = "this is a broken ` code ` *block"
        with self.assertRaises(Exception):
            str_to_textnodes(text)


if __name__ == "__main__":
    unittest.main()
