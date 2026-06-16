import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_child_with_props(self):
        child_node = LeafNode("a", "child", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a href="https://www.google.com">child</a></div>',
        )

    def test_to_html_with_nested_grandChildren(self):
        grandchild_node = LeafNode("b", "button text")
        grandchild2_node = LeafNode("b","buttonText2")
        child_node = ParentNode("button", [grandchild_node])
        child2_node = ParentNode("button",[grandchild2_node])
        parent_node = ParentNode("div", [child_node, child2_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><button><b>button text</b></button><button><b>buttonText2</b></button></div>"
                         )

    def test_to_html_with_parent_props_children_props(self):
        child_node = LeafNode("a", "child", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node], {"active" : "True"})
        self.assertEqual(parent_node.to_html(), '<div active="True"><a href="https://www.google.com">child</a></div>')

    def test_to_html_with_no_tag(self):
        child = LeafNode("p","test")
        node = ParentNode(None,[child])
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_to_html_with_no_child(self):
        node = ParentNode("div",None)
        with self.assertRaises(ValueError):
            node.to_html()
