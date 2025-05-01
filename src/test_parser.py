import unittest


class TestParser(unittest.TestCase):
    def test_parser(self):
        block = """
        ```
        code
        ```
        """
        self.assertEqual(
            get_block_type(block),
            BlockType.CODE,
        )
