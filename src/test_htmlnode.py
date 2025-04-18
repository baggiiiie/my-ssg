import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
