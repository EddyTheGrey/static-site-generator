from enum import Enum
from pydoc import plain, text

class TextType(Enum):
    NORMAL = "text(plain)"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGES = "![alt text](image_url)"


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
    
