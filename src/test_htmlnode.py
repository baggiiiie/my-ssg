import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(None, None)
            node.to_html()

    def test_to_html_with_children(self):
        child_node_1 = LeafNode("span", "child1")
        child_node_2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_htmll_with_empty_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", [])
            node.to_html()

    def test_parent_no_tag(self):
        with self.assertRaises(ValueError):
            child_node = ParentNode("span", [])
            node = ParentNode("", [child_node])
            node.to_html()


if __name__ == "__main__":
    unittest.main()
