import unittest

from src.htmlblock import BlockType
from src.utils import block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
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
