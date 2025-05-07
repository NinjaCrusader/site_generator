import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    
    for old_node in old_nodes:
        # Skip non-TEXT nodes
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        # Process TEXT nodes
        text = old_node.text
        parts = []
        remaining_text = text
        
        # Keep looking for delimiter pairs until none are left
        while delimiter in remaining_text:
            # Find the first occurrence of the delimiter
            start_idx = remaining_text.find(delimiter)
            
            # Extract the text before the delimiter
            if start_idx > 0:
                parts.append((remaining_text[:start_idx], TextType.TEXT))
            
            # Look for the closing delimiter
            end_idx = remaining_text.find(delimiter, start_idx + len(delimiter))
            if end_idx == -1:
                # No closing delimiter found - this is invalid markdown
                raise ValueError(f"No closing delimiter {delimiter} found")
            
            # Extract the text between delimiters
            content = remaining_text[start_idx + len(delimiter):end_idx]
            parts.append((content, text_type))
            
            # Update remaining_text to continue searching
            remaining_text = remaining_text[end_idx + len(delimiter):]
        
        # Add any remaining text after the last delimiter
        if remaining_text:
            parts.append((remaining_text, TextType.TEXT))
        
        # Create TextNodes from the parts and add to result
        for text_content, node_type in parts:
            result.append(TextNode(text_content, node_type))
    
    return result



def extract_markdown_images(text):
    capture = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return capture


def extract_markdown_links(text):
    capture = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return capture


def split_nodes_image(old_nodes):
    resulting_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            resulting_list.append(node)
            continue
        images = extract_markdown_images(node.text)
        
        if len(images) == 0:
            resulting_list.append(node)
            continue
        # We have at least one image, let's process it
        current_text = node.text
        
        for image_alt, image_url in images:
            # Split the text at the image markdown
            image_markdown = f"![{image_alt}]({image_url})"
            parts = current_text.split(image_markdown, 1)
            
            # Add text before the image (if not empty)
            if parts[0]:
                resulting_list.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the image node
            resulting_list.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Update current_text to the remaining part
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        
        # Add any remaining text (if not empty)
        if current_text:
            resulting_list.append(TextNode(current_text, TextType.TEXT))
    return resulting_list


def split_nodes_link(old_nodes):
    resulting_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            resulting_list.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            resulting_list.append(node)
            continue
        current_text = node.text
        for link_alt, link_url in links:
            link_markdown = f"[{link_alt}]({link_url})"
            parts = current_text.split(link_markdown, 1)

            if parts[0]:
                resulting_list.append(TextNode(parts[0], TextType.TEXT))

            resulting_list.append(TextNode(link_alt, TextType.LINK, link_url))

            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        
        if current_text:
            resulting_list.append(TextNode(current_text, TextType.TEXT))
    return resulting_list


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes