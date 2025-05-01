import unittest

from src.utils.str_utils import md_to_blocks


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here  
    This is the same paragraph on a new line
    """
        blocks = md_to_blocks(md)
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
        blocks = md_to_blocks(md)
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
        blocks = md_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\n        text in a p\n        tag here",
                "        This is another paragraph with _italic_ text and `code` here",
            ],
        )

    def test_markdown_to_blocks_single_text_node(self):
        md = """
        - **this is a bolded text**
        """
        blocks = md_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- **this is a bolded text**",
            ],
        )
