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

    def test_md_parser_single_line_p(self):
        md = "hello world"
        result = MarkdownParser().line_parse(md)
        expected = "<p>hello world</p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_h(self):
        md = "# hello world"
        result = MarkdownParser().line_parse(md)
        expected = "<h1>hello world</h1>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_not_h(self):
        md = "#hello world"
        result = MarkdownParser().line_parse(md)
        expected = "<p>#hello world</p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_h2(self):
        md = "## hello world"
        result = MarkdownParser().line_parse(md)
        expected = "<h2>hello world</h2>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_code(self):
        md = "this is a `code block`"
        result = MarkdownParser().line_parse(md)
        expected = "<p>this is a <code>code block</code></p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_code_format(self):
        md = "this is a `*code block*`"
        result = MarkdownParser().line_parse(md)
        expected = "<p>this is a <code>*code block*</code></p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_format(self):
        md = "this is a *italic* and **bolded**"
        result = MarkdownParser().line_parse(md)
        expected = "<p>this is a <i>italic</i> and <b>bolded</b></p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_nested_format(self):
        md = "this is a _italic and **bolded**_"
        result = MarkdownParser().line_parse(md)
        expected = "<p>this is a <i>italic and <b>bolded</b></i></p>"
        self.assertEqual(result, expected)

    def test_md_parser_single_line_quote(self):
        md = "> this is a quote"
        result = MarkdownParser().line_parse(md)
        expected = "<blockquote><p>this is a quote</p></blockquote>"
        self.assertEqual(result, expected)

    def test_md_parser_multi_line_quote(self):
        md = """> this is a quote  
> another quote"""
        result = MarkdownParser().line_parse(md)
        expected = r"<blockquote><p>this is a quote<br>another quote</p></blockquote>"
        self.assertEqual(result, expected)

    def test_md_parser_multi_line_code(self):
        md = """this is a
```
*code block*
```
        """
        result = MarkdownParser().line_parse(md)
        expected = "<p>this is a</p><pre><code>*code block*</code></pre>"
        self.assertEqual(result, expected)

    def test_md_parser_multi_line_trailing_spaces(self):
        md = """this is a  
new line
        """
        result = MarkdownParser().line_parse(md)
        expected = "<p>this is a<br>new line</p>"
        self.assertEqual(result, expected)
