from enum import Enum
import re
from textfunctions import text_to_textnodes
from textnode import TextNode 
from textnode import TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "# Heading"
    CODE = "```code block```"
    QUOTE = "> quote"
    UNORDERED_LIST = "- unordered_list"
    ORDERED_LIST = "1. ordered_list"


def markdown_to_blocks(markdown):
    '''
    Converts a markdown string into a list of blocks, where each block is a list of TextNodes.
    '''
    # Split the markdown into lines and process each line separately
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    content_lines = []
    for segments in blocks:
        lines = segments.split("\n")
        stripped_lines = [line.strip() for line in lines]
        stripped_lines = [line for line in stripped_lines if line != ""]
        rejoined_line = "\n".join(stripped_lines)
        stripped_blocks.append(rejoined_line.strip("\n"))
        stripped_blocks = [b for b in stripped_blocks if b != ""]
    return stripped_blocks

def block_to_block_type(block):
    '''
    Determines the block type of a given block of text.
    '''
    if block.startswith(("# ","## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\. ", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def blocks_and_types(markdown):
    '''
    Converts a markdown string into a list of tuples, where each tuple contains a block and its corresponding block type.
    '''
    blocks = markdown_to_blocks(markdown)
    block_types = [block_to_block_type(block) for block in blocks]
    return list(zip(blocks, block_types))
    
def split_markdown_to_blocks(markdown):
    '''
    Splits a markdown string into blocks and determines the block type for each block.
    '''
    blocks = markdown_to_blocks(markdown)
    #block_types = [block_to_block_type(block) for block in blocks]
    return list(blocks)

def blocks_to_html_nodes(blocks):
    '''
    Converts a list of blocks into a list of HTML nodes. Uses text_to_textnodes to handle inline markdown syntax within each block.
    '''
    html_nodes = []
    blocks_and_types = [(block, block_to_block_type(block)) for block in blocks]
    for block, block_type in blocks_and_types:
        if block_type == BlockType.HEADING:
            level = 0 # Default to h1 if somehow the block type is HEADING without a specific level
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            text = block[level +1:]
            html_nodes.append(ParentNode(f"h{level}", text_to_children(text)))
        elif block_type == BlockType.CODE:
            text_node = TextNode(block[4:-3], TextType.CODE)
            code = LeafNode("code", text_node.text)
            pre = ParentNode("pre", [code])
            html_nodes.append(pre)
        elif block_type == BlockType.QUOTE:
            html_nodes.append(ParentNode("blockquote", text_to_children(block[2:].strip())))
        elif block_type == BlockType.UNORDERED_LIST:
            items = [item.strip()[2:].strip() for item in block.split("\n") if item.strip().startswith("- ")]
            html_nodes.append(ParentNode("ul", [ParentNode("li", text_to_children(item)) for item in items]))
        elif block_type == BlockType.ORDERED_LIST:
            items = [item.strip()[re.match(r"^\d+\. ", item).end():].strip() for item in block.split("\n") if re.match(r"^\d+\. ", item.strip())]
            html_nodes.append(ParentNode("ol", [ParentNode("li", text_to_children(item)) for item in items]))
        else:  # Paragraph
            paragraph = " ".join(block.split("\n"))
            html_nodes.append(ParentNode("p", text_to_children(paragraph)))
    return html_nodes

def text_to_children(text):
    '''
    Converts a markdown text into a list of HTML nodes, handling inline markdown syntax.
    '''
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes

def inline_markdown_to_text_nodes(text):
    '''
    Converts a markdown text into a list of TextNodes, handling inline markdown syntax.
    '''
    return text_to_textnodes(text)

def markdown_to_html_node(markdown):
    '''
    Converts a markdown string into an HTML node representation.
    '''
    blocks = markdown_to_blocks(markdown)
    html_nodes = blocks_to_html_nodes(blocks)
    return ParentNode("div", html_nodes)