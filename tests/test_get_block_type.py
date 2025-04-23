import unittest

from src.htmlblock import BlockType
from src.utils.block_checker import get_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_get_block_type_code(self):
        block = """```
        code
        ```
        """
        self.assertEqual(
            get_block_type(block),
            BlockType.CODE,
        )

    def test_get_block_type_code_multiline(self):
        block = """ ```
        code
        another code


        ```
        """
        self.assertEqual(
            get_block_type(block),
            BlockType.CODE,
        )

    def test_get_block_type_not_code(self):
        block = "```test``"
        self.assertEqual(
            get_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_get_block_type_quote(self):
        block = "> test\n> test2"
        self.assertEqual(
            get_block_type(block),
            BlockType.QUOTE,
        )

    def test_get_block_type_quote_2(self):
        block = "> test\n> test2"
        self.assertEqual(
            get_block_type(block),
            BlockType.QUOTE,
        )

    def test_get_block_type_not_quote(self):
        block = ">test"
        self.assertEqual(
            get_block_type(block),
            BlockType.PARAGRAPH,
        )
