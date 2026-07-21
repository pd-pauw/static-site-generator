from textnode import TextNode, TextType
import re

def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        if len(split_nodes) % 2 == 0:
            raise Exception(f"Not valid Markdown Syntax: {node}")
        for i in range(len(split_nodes)):
            if split_nodes[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_nodes[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        node_text = node.text
        for image in images:
            split_node = node_text.split(f"![{image[0]}]({image[1]})",1)
            if len(split_node) < 2:
                raise ValueError("Invalid markdown syntax")
            if split_node[0]:
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = split_node[1]
        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        node_text = node.text
        for link in links:
            split_node = node_text.split(f"[{link[0]}]({link[1]})",1)
            if len(split_node) < 2:
                raise ValueError("Invalid markdown syntax")
            if split_node[0]:
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = split_node[1]
        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)