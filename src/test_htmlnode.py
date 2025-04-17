import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    # Test if props defaults to None
    def test_props_to_html_none(self):
        # Test Node created with parameters
        node = HTMLNode()
        # What the result should be when calling the .props_to_html() method
        self.assertEqual(node.props_to_html(),"")

    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_props_to_html_multi_prop(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

    def test_leaf_to_html_text(self):
        node = LeafNode(tag="p",value="This is text",props=None)
        self.assertEqual(node.to_html(), '<p>This is text</p>')

    def test_leaf_to_html_props(self):
        node = LeafNode(tag="a",value="Click Me!",props={"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Click Me!</a>')

    def test_leaf_t0_html_no_tag(self):
        node = LeafNode(tag=None,value="This is raw text",props=None)
        self.assertEqual(node.to_html(), 'This is raw text')

    def test_parentnode_to_html(self):
        node = ParentNode("div",[LeafNode("b","Bold Text")])
        self.assertEqual(node.to_html(), '<div><b>Bold Text</b></div>')

    def test_multi_parentnode_to_html(self):
        node = ParentNode("p",[LeafNode("b","Bold Text"),LeafNode("i","Italic Text")])
        self.assertEqual(node.to_html(), '<p><b>Bold Text</b><i>Italic Text</i></p>')



if __name__ == "__main__":
    unittest.main()