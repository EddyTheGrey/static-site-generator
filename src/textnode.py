from enum import Enum
from pydoc import plain, text
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
    NORMAL = "text(plain)"
    TEXT = "Text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](image_url)"


class TextNode:
    def __init__(self, text: str, text_type: TextType, URL: str = None):
        self.text = text
        self.text_type = text_type
        self.url = URL  # For LINK and IMAGES types

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

    

def text_node_to_html_node(text_node):
   if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
   if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
   if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
   if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
   if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
   if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
   else:
        raise Exception("Unsupported TextType")
   
