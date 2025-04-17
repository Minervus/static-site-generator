from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode():
    def __init__(self,text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (self.text,self.text_type) == (other.text,other.text_type)
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        text_node.props = {"href": text_node.url}
        return LeafNode("a", text_node.text, text_node.props)
    elif text_node.text_type == TextType.IMAGE:
        text_node.props = {"src": text_node.url, "alt": text_node.text}
        return LeafNode("img", "", text_node.props)
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")



            
