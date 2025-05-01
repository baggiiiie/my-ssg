import unittest
from parser import MarkdownParser


class TestParser(unittest.TestCase):
    def test_parser(self):
        md = "this is a test"
        parser = MarkdownParser()
        md = parser.inline_parser(md)
        self.assertEqual(md, "this is a test")
