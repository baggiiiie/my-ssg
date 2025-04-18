import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_init_node(self):
        node = HTMLNode("p", "This is a text node")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a text node")
        self.assertEqual(node.children, [])

    def test_props_to_html(self):
        node = HTMLNode("p", "This is a text node", props={"class": "text"})
        html_text = ' class="text"'
        self.assertEqual(node.props_to_html(), html_text)

    def test_repr(self):
        node = HTMLNode("p", "This is a text node", props={"class": "text"})
        self.assertEqual(
            repr(node),
            "HTMLNode(p, This is a text node, [], {'class': 'text'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()
