import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode
from node_splitter import text_to_textnodes


def markdown_to_blocks(markdown):
    split_markdown = markdown.strip().split("\n\n")
    result = []
    for block in split_markdown:
        if block.strip():
            new_block = block.strip()
            result.append(new_block)
    return result


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if re.match(r'^#{1,6}', block):
        return BlockType.HEADING
    if re.match(r'```.*?```', block):
        return BlockType.CODE
    if re.match(r'^>.*', block):
        return BlockType.QUOTE
    if re.match(r'^- .*', block):
        return BlockType.UNORDERED_LIST
    if re.match(r'^(\d+)\. .+', block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH



def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = TextNode.text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes
    


def determine_heading(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    heading_tag = f"h{count}"
    heading_text = block[count:].strip()
    return heading_tag, heading_text


def markdown_to_html_node(markdown):
    block_list = []
    split_markdown = markdown_to_blocks(markdown)
    for block in split_markdown:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            heading_tag, heading_text = determine_heading(block)
            heading_children = text_to_children(heading_text)
            html_node = ParentNode(heading_tag, heading_children)
            block_list.append(html_node)
        elif block_type == BlockType.PARAGRAPH:
            paragraph_children = text_to_children(block)
            html_node = ParentNode("p", paragraph_children)
            block_list.append(html_node)
        elif block_type == BlockType.CODE:
            code_content = block.replace("```", "")
            code_text_node = TextNode(code_content, TextType.TEXT)
            code_html_node = TextNode.text_node_to_html_node(code_text_node)
            code_node = ParentNode("code", [code_html_node])
            pre_node = ParentNode("pre", [code_node])
            block_list.append(pre_node)
        elif block_type == BlockType.QUOTE:
            quote_text = re.sub(r'^>\s*', '', block, flags=re.MULTILINE).strip()
            quote_children = text_to_children(quote_text)
            html_node = ParentNode("blockquote", quote_children)
            block_list.append(html_node)
        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split('\n')
            list_items = []
            for item in items:
                if item.strip():
                     item_text = re.sub(r'^-\s*', '', item).strip()
                     item_children = text_to_children(item_text)
                     li_node = ParentNode("li", item_children)
                     list_items.append(li_node)
            html_node = ParentNode("ul", list_items)
            block_list.append(html_node)
        elif block_type == BlockType.ORDERED_LIST:
            items = block.split('\n')
            list_items = []
            for item in items:
                if item.strip():  # Skip empty lines
                    item_text = re.sub(r'^\d+\.\s*', '', item).strip()
                    item_children = text_to_children(item_text)
                    li_node = ParentNode("li", item_children)
                    list_items.append(li_node)
            html_node = ParentNode("ol", list_items)
            block_list.append(html_node)
    parent_node = ParentNode("div", block_list)
    return parent_node