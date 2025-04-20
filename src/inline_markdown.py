from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(parts)):
            part = parts[i]
            if i % 2 == 0:
                node = TextNode(part, TextType.TEXT)
            else:
                node = TextNode(part, text_type)
            split_nodes.append(node)
        new_nodes.extend(split_nodes)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if not images:
            new_nodes.append(old_node)
            continue

        for image in images:
            alt, url = image
            delimiter = f"![{alt}]({url})"
            parts = original_text.split(delimiter, 1)
            
            if len(parts) != 2:
                raise ValueError("Invalid markdown, image section not closed")
        
            if len(parts[0]) != 0:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            original_text = parts[1]
        
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
        

    return new_nodes
        

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if not links:
            new_nodes.append(old_node)
            continue
        
        for link_text, url in links:
            delimiter = f"[{link_text}]({url})"
            parts = original_text.split(delimiter, 1)

            if len(parts) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if len(parts[0]) != 0:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link_text, TextType.LINK, url))

            original_text = parts[1]

        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def extract_markdown_links(text):
    matches = re.findall(r"\[([^\]]*)\]\(([^)]*)\)", text)
    return matches


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)
    return matches


def text_to_textnodes(text):
    nodes = [TextNode(text.strip(), TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes




