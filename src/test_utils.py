import unittest

from textnode import TextNode, TextType
from htmlblock import BlockType
from utils import (
    text_node_to_html_leaf_node,
    split_nodes_delimiter,
    split_nodes_delimiters,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)


class TestUtils(unittest.TestCase):
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

    def test_text_to_textnodes_normal(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
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
        new_nodes = text_to_textnodes(text)
        self.assertEqual([], new_nodes)

    def test_text_to_textnodes_none(self):
        text = None
        new_nodes = text_to_textnodes(text)
        self.assertEqual([], new_nodes)

    def test_text_to_textnodes_broken_delimiter(self):
        text = "this is a broken ` code block"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_text_to_textnodes_broken_delimiter_2(self):
        text = "this is a broken ` code ` *block"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here  
    This is the same paragraph on a new line
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "    This is another paragraph with _italic_ text and `code` here  \n    This is the same paragraph on a new line",
            ],
        )

    def test_markdown_to_blocks_multiline(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\n        text in a p\n        tag here",
                "        This is another paragraph with _italic_ text and `code` here",
            ],
        )

    def test_markdown_to_blocks_multiline_empty(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here



        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\n        text in a p\n        tag here",
                "        This is another paragraph with _italic_ text and `code` here",
            ],
        )

    def test_block_to_block_type_code(self):
        block = """```
        code
        ```
        """
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_block_to_block_type_code_multiline(self):
        block = """ ```
        code
        another code


        ```
        """
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_block_to_block_type_not_code(self):
        block = "```test``"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_quote(self):
        block = "> test\n> test2"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_block_to_block_type_quote_2(self):
        block = "> test\n> test2"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_block_to_block_type_not_quote(self):
        block = ">test"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is: {html}\nexpected is {expected}",
        )

    # def test_codeblock(self):
    #     md = """
    # ```
    # This is text that _should_ remain
    # the **same** even with inline stuff
    # ```
    # """
    #
    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    #     )


if __name__ == "__main__":
    unittest.main()
