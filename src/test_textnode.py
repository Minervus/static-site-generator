import unittest

from textnode import *
from htmlnode import LeafNode
from split_delimiter import *
from extractor import *
from split_nodes import *
from generate_page import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
        node3 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is not a text node", TextType.TEXT)
        self.assertNotEqual(node3,node4)

        node5 = TextNode("This is text", TextType.TEXT)
        node6 = TextNode("This is a text node", TextType.TEXT,"https://google.com")
        self.assertNotEqual(node5,node6)

    def text_node_to_html_node_TEXT(self):
        # Create Text Node
        node = TextNode("This is the text", TextType.TEXT)
        # Run node through function and store in result
        result = text_node_to_html_node(node)
        # Create LeafNode 'result' with LeafNode constructor
        expected = LeafNode(None, "This is the text")
        # Check tags are the same
        self.assertEqual(result.tag, expected.tag)
        # Check value is the same i.e. raw text
        self.assertEqual(result.value, expected.value)
    
    def text_node_to_html_node_bold(self):
        # Create Text Node
        node = TextNode("This is the text", TextType.BOLD)
        # Run node through function and store in result
        result = text_node_to_html_node(node)
        # Create LeafNode 'result' with LeafNode constructor
        expected = LeafNode("b", "This is the text")
        # Check tags are the same
        self.assertEqual(result.tag, expected.tag)
        # Check value is the same i.e. raw text
        self.assertEqual(result.value, expected.value)

    def text_node_to_html_node_props(self):
        # Create Text Node
        node = TextNode("This is the text", TextType.LINK,"https://google.com")
        # Run node through function and store in result
        result = text_node_to_html_node(node)
        # Create LeafNode 'result' with LeafNode constructor
        expected = LeafNode("a", "This is the text",{"href": "https://google.com"})
        # Check tags are the same
        self.assertEqual(result.tag, expected.tag)
        # Check value is the same i.e. raw text
        self.assertEqual(result.value, expected.value)

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ])
        
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a **Legolas** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("Legolas", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ])

    def extract_markdown_images_test(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(result,[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(result,[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def split_nodes_links_test(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT)
        result = split_nodes_link(node)
        self.assertEqual(result, [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
            "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            ])   
    def split_nodes_images_test(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
        TextType.TEXT)
        result = split_nodes_image(node)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
            "obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            ]) 
        

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(result,[
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", """* This is the first list item in a list block
        * This is a list item
        * This is another list item"""])

    def test_block_to_block_type_heading(self):
        text = "# heading 1"
        result = block_to_block_type(text)
        self.assertEqual(result, "heading 1")
    
    def test_block_to_block_type_quote(self):
        text = "> some kind of quote"
        result = block_to_block_type(text)
        self.assertEqual(result, "quote")

    def test_block_to_block_type_unordered_list(self):
        text = "* list item 1\n* list item 2"
        result = block_to_block_type(text)
        self.assertEqual(result, "unordered list")

    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )



    def test_text_extract_header(self):
        markdown = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """
        result = extract_title(markdown)
        
        print(f"Actual result: {result}")
        self.assertEqual(result,"This is a heading")

    # def test_no_heading_text_extract(self):
    #     markdown = """ This is a heading

    #     This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    #     * This is the first list item in a list block
    #     * This is a list item
    #     * This is another list item
    #     """
    #     result = extract_title(markdown)
        
    #     print(f"Actual result: {result}")
    #     self.assertRaises(Exception)


if __name__ == "__main__":
    unittest.main()