import unittest
from src.parser import MarkdownParser


class TestInlineParser(unittest.TestCase):
    def test_inline_parser_normal_text(self):
        md = "this is a test"
        result = MarkdownParser().inline_parser(md)
        expected = "this is a test"
        self.assertEqual(result, expected)

    def test_inline_parser_normal_code(self):
        md = "this is `code block`"
        result = MarkdownParser().inline_parser(md)
        expected = "this is <code>code block</code>"
        self.assertEqual(result, expected)

    def test_inline_parser_normal_italic(self):
        md = "this is *italic*"
        result = MarkdownParser().inline_parser(md)
        expected = "this is <i>italic</i>"
        self.assertEqual(result, expected)

    def test_inline_parser_normal_italic_2(self):
        md = "this is _italic_"
        result = MarkdownParser().inline_parser(md)
        expected = "this is <i>italic</i>"
        self.assertEqual(result, expected)

    def test_inline_parser_normal_bold(self):
        md = "this is **bold**"
        result = MarkdownParser().inline_parser(md)
        expected = "this is <b>bold</b>"
        self.assertEqual(result, expected)

    def test_inline_parser_normal_bold_2(self):
        md = "this is __bold__"
        result = MarkdownParser().inline_parser(md)
        expected = "this is <b>bold</b>"
        self.assertEqual(result, expected)

    def test_inline_parser_normal_multiple(self):
        md = "this is __bold__ and *italic*"
        result = MarkdownParser().inline_parser(md)
        expected = "this is <b>bold</b> and <i>italic</i>"
        self.assertEqual(result, expected)

    def test_inline_parser_normal_multiple_2(self):
        md = "this is __bold__ and `code`"
        result = MarkdownParser().inline_parser(md)
        expected = "this is <b>bold</b> and <code>code</code>"
        self.assertEqual(result, expected)

    def test_inline_parser_normal_nested(self):
        md = "this is __bolded *italic*__"
        result = MarkdownParser().inline_parser(md)
        expected = "this is <b>bolded <i>italic</i></b>"
        self.assertEqual(result, expected)

    def test_inline_parser_normal_nested_2(self):
        md = "this is `__non-bolded__ code`"
        result = MarkdownParser().inline_parser(md)
        expected = "this is <code>__non-bolded__ code</code>"
        self.assertEqual(result, expected)

    def test_inline_parser_normal_nested_3(self):
        md = "this is *`code`*"
        result = MarkdownParser().inline_parser(md)
        expected = "this is <i><code>code</code></i>"
        self.assertEqual(result, expected)

    def test_inline_parser_link(self):
        md = "this is a [link](https://example.com)"
        result = MarkdownParser().inline_parser(md)
        expected = 'this is a <a href="https://example.com">link</a>'
        self.assertEqual(result, expected)

    def test_inline_parser_img(self):
        md = "this is an ![image](https://example.com)"
        result = MarkdownParser().inline_parser(md)
        expected = 'this is an <img src="https://example.com" alt="image">'
        self.assertEqual(result, expected)

    def test_md_parser_single_line_p(self):
        md = "hello world"
        result = MarkdownParser().line_parse(md.strip())
        expected = "<p>hello world</p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_h(self):
        md = "# hello world"
        result = MarkdownParser().line_parse(md.strip())
        expected = "<h1>hello world</h1>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_not_h(self):
        md = "#hello world"
        result = MarkdownParser().line_parse(md.strip())
        expected = "<p>#hello world</p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_h2(self):
        md = "## hello world"
        result = MarkdownParser().line_parse(md.strip())
        expected = "<h2>hello world</h2>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_code(self):
        md = "this is a `code block`"
        result = MarkdownParser().line_parse(md.strip())
        expected = "<p>this is a <code>code block</code></p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_code_format(self):
        md = "this is a `*code block*`"
        result = MarkdownParser().line_parse(md.strip())
        expected = "<p>this is a <code>*code block*</code></p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_format(self):
        md = "this is a *italic* and **bolded**"
        result = MarkdownParser().line_parse(md.strip())
        expected = "<p>this is a <i>italic</i> and <b>bolded</b></p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_nested_format(self):
        md = "this is a _italic and **bolded**_"
        result = MarkdownParser().line_parse(md.strip())
        expected = "<p>this is a <i>italic and <b>bolded</b></i></p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_quote(self):
        md = "> this is a quote"
        result = MarkdownParser().line_parse(md.strip())
        expected = "<blockquote><p>this is a quote</p></blockquote>"
        self.assertEqual(result, expected)

    def test_md_parser_multi_line_quote(self):
        md = """> this is a quote  
> another quote"""
        result = MarkdownParser().line_parse(md.strip())
        expected = r"<blockquote><p>this is a quote<br>another quote</p></blockquote>"
        self.assertEqual(result, expected)

    def test_md_parser_multi_line_code(self):
        md = """this is a
```
*code block*
```
        """
        result = MarkdownParser().line_parse(md.strip())
        expected = "<p>this is a</p><pre><code>*code block*</code></pre>"
        self.assertEqual(result, expected)

    def test_md_parser_multi_line_trailing_spaces(self):
        md = """this is a  
new line
        """
        result = MarkdownParser().line_parse(md.strip())
        expected = "<p>this is a<br>new line</p>"
        self.assertEqual(result, expected)

    def test_md_parser_multi_line_with_link(self):
        md = """this is a [link](https://example.com)  
hello
        """
        result = MarkdownParser().line_parse(md.strip())
        expected = '<p>this is a <a href="https://example.com">link</a><br>hello</p>'
        self.assertEqual(result, expected)

    def test_md_parser_multi_line_with_img(self):
        md = """this is a ![link](link-to-img)  
hello
        """
        result = MarkdownParser().line_parse(md.strip())
        expected = '<p>this is a <img src="link-to-img" alt="link"><br>hello</p>'
        self.assertEqual(result, expected)


class TestTextToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        html = MarkdownParser().line_parse(md.strip())
        expected = "<p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p>"
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

        html = MarkdownParser().line_parse(md.strip())
        expected = "<pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre>"
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

        html = MarkdownParser().line_parse(md.strip())
        expected = r"<ul><li>item 1 with trailing spaces</li><li>item 2</li></ul>"
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

        html = MarkdownParser().line_parse(md.strip())
        expected = r"<blockquote><p>quote line 1 with trailing spaces<br>quote line 2</p></blockquote>"
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is:\n{html}\nexpected is:\n{expected}",
        )

    def test_all(self):
        md = """
this is a paragraph with trailing spaces  
**new line here**
_same line_

> quote line 1 with trailing spaces  
> quote line 2 

```
code block **bolded**
```

1. list item 1  
2. item 2
"""

        html = MarkdownParser().line_parse(md.strip())
        expected = """<p>this is a paragraph with trailing spaces<br><b>new line here</b> <i>same line</i></p><blockquote><p>quote line 1 with trailing spaces<br>quote line 2</p></blockquote><pre><code>code block **bolded**</code></pre><ol><li>list item 1</li><li>item 2</li></ol>"""
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is:\n{html}\nexpected is:\n{expected}",
        )

    def test_link_and_image(self):
        md = """
        this is a [link](https://test) and an ![img](img-link)
        """

        html = MarkdownParser().line_parse(md.strip())
        expected = '<p>this is a <a href="https://test">link</a> and an <img src="img-link" alt="img"></p>'
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is:\n{html}\nexpected is:\n{expected}",
        )

    def test_link_and_image_with_list(self):
        md = """
        - this is a [link](https://test) and an ![img](img-link)
        """

        html = MarkdownParser().line_parse(md.strip())
        expected = '<ul><li>this is a <a href="https://test">link</a> and an <img src="img-link" alt="img"></li></ul>'
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is:\n{html}\nexpected is:\n{expected}",
        )

    def test_link_and_image_with_list_2(self):
        md = """
        - [link](https://test)
        """
        html = MarkdownParser().line_parse(md.strip())
        expected = '<ul><li><a href="https://test">link</a></li></ul>'
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is:\n{html}\nexpected is:\n{expected}",
        )

    def test_bolded_in_list(self):
        md = """
        - **bolded text**
        """
        html = MarkdownParser().line_parse(md.strip())
        expected = "<ul><li><b>bolded text</b></li></ul>"
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is:\n{html}\nexpected is:\n{expected}",
        )

    def test_escape_sequence_in_code_block(self):
        md = """
```
code\nformat
```
        """
        html = MarkdownParser().line_parse(md.strip())
        expected = """<pre><code>code
format</code></pre>"""
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is:\n{html}\nexpected is:\n{expected}",
        )

    def test_code_in_paragraph(self):
        md = r"""
        this is a `code\nblock` in a paragraph
        """
        html = MarkdownParser().line_parse(md.strip())
        expected = r"<p>this is a <code>code\nblock</code> in a paragraph</p>"
        self.assertEqual(
            html,
            expected,
            f"\nhtml text is:\n{html}\nexpected is:\n{expected}",
        )
