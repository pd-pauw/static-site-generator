from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_node_to_html_node, TextNode, TextType
from textnodefunctions import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown:str)-> list[str]:
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == "":
           continue
        block = block.strip()
        new_blocks.append(block)
    return new_blocks

def block_to_block_type(block:str) -> BlockType:
    first_char = block[0]
    if first_char == "#": 
        count_char = block.count("#")
        if block[count_char] == " ":
            return BlockType.HEADING
        else:
            return BlockType.PARAGRAPH
    if first_char == "`":
        if block[:4] == "```\n" and block[-3:] == "```":
            return BlockType.CODE
        else:
            return BlockType.PARAGRAPH
    lines = block.split("\n")
    count = 0
    if first_char == "-" or first_char == "1" or first_char ==">":
        for line in lines:
            if line.startswith(first_char):
                count += 1
            else:
                count = 0
                break
        if count == len(lines):
            return BlockType.QUOTE if first_char == ">" else BlockType.UNORDERED_LIST
        for i in range(len(lines)):
            if lines[i].startswith(f"{i+1}."):
                count += 1
            else:
                count = 0
                break
        if count == len(lines):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_html_node(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    leaf_nodes = map(text_node_to_html_node, text_nodes)
    return list(leaf_nodes)


def markdown_to_html_node(markdown: str):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            cleaned_block = " ".join(block.splitlines())
            children = text_to_children(cleaned_block)
            parent = ParentNode("p", children)
            html_nodes.append(parent)

        if block_type == BlockType.HEADING:
            count_char = block.count("#")
            cleaned_block = block[count_char:].strip()
            children = text_to_html_node(cleaned_block)
            parent = ParentNode(f"h{count_char}", children)
            html_nodes.append(parent)

        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            children = text_to_children(content)
            parent = ParentNode("blockquote", children)
            html_nodes.append(parent)

        if block_type == BlockType.UNORDERED_LIST:
            list_lines = block.split("\n")
            li_nodes = []
            for line in list_lines:
                if line == "":
                    continue
                cleaned_line = line[1:].strip()
                line_children = text_to_html_node(cleaned_line)
                li_node = ParentNode("li", line_children)
                li_nodes.append(li_node)
            parent = ParentNode("ul", li_nodes)
            html_nodes.append(parent)

        if block_type == BlockType.ORDERED_LIST:
            list_lines = block.split("\n")
            li_nodes = []
            for line in list_lines:
                if line == "":
                    continue
                cleaned_line = line[2:].strip()
                line_children = text_to_html_node(cleaned_line)
                li_node = ParentNode("li", line_children)
                li_nodes.append(li_node)
            parent = ParentNode("ol", li_nodes)
            html_nodes.append(parent)

        if block_type == BlockType.CODE:
            cleaned_block = block[4:-3]
            child = LeafNode("code",cleaned_block)
            parent = ParentNode("pre",[child])
            html_nodes.append(parent)

    return ParentNode("div", html_nodes)


def text_to_children(text: str):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
