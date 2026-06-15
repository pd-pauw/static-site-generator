from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT= "Text"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url:str|None = None):
        self.text= text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        if (self.text == other.text 
        and self.text_type == other.text_type 
        and self.url == other.url):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    tag = None
    props = None
    match(text_node.text_type):
        case TextType.TEXT:
            tag = None
        case TextType.BOLD:
            tag="b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a"
            props = {"href": text_node.url}
        case TextType.IMAGE:
            props = {"src": text_node.url, "alt": text_node.text}
            text_node.text = ""
        case _:
            raise Exception("Textnode does not have a valid type")
    return LeafNode(tag, text_node.text, props)