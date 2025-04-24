import unittest

from src.utils.utils import md_to_htmlnode


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = md_to_htmlnode(md)
        html = node.to_html()
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is: {html}\nexpected is {expected}",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = md_to_htmlnode(md)
        html = node.to_html()
        expected = r"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is: {html}\nexpected is {expected}",
        )

    def test_unordered_list(self):
        md = """
    - item 1 with trailing spaces  
    - item 2
    """

        node = md_to_htmlnode(md)
        html = node.to_html()
        expected = (
            r"<div><ul><li>item 1 with trailing spaces</li><li>item 2</li></ul></div>"
        )
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is:\n{html}\nexpected is:\n{expected}",
        )

    def test_quote(self):
        md = """
    > quote line 1 with trailing spaces  
    > quote line 2 
    """

        node = md_to_htmlnode(md)
        html = node.to_html()
        expected = r"<div><blockquote>quote line 1 with trailing spaces\nquote line 2</blockquote></div>"
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is:\n{html}\nexpected is:\n{expected}",
        )
