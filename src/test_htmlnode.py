import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        props={
            "href": "https://www.google.com",
        }
        node = HTMLNode("a", "hello",None, props)
        self.assertEqual(node.__repr__(), "HtmlNode(a, hello, None, {'href': 'https://www.google.com'})")
    
    def test_props_to_html_1_prop(self):
        props = {
            "href": "https://www.google.com",
        }
        node = HTMLNode("a","google", None, props)
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com"')

    def test_props_to_html_2_props(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        node = HTMLNode("a","google", None, props)
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_no_props(self):
        node = HTMLNode("a","google", None, None)
        result = node.props_to_html()
        self.assertEqual(result, '')

