import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("This is a text", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertEqual(node.text, "This is a text")
        self.assertNotEqual(node, node2)

    def test_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_not_textnode(self):
        node = TextNode("This is a text node", TextType.BOLD)
        not_a_node = "hi"
        self.assertNotEqual(node, not_a_node)


if __name__ == "__main__":
    unittest.main()
