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
