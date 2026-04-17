import re
from textnode import TextNode 
from textnode import TextType

def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextType.TEXT) -> list:
    '''
    takes a list of "old nodes", a delimiter, and a text type. Returns a list of new nodes 
    where the text of each old node is split by the delimiter 
    and wrapped in a new TextNode with the specified text type.
    '''
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
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
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_node):
    '''
    takes a TextNode with text type TextType.LINK and splits it into multiple TextNodes if there are multiple links in the text. 
    Returns a list of new TextNodes.
    '''
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    '''
    Extracts markdown image syntax from the input text and returns a list of tuples containing the alt text and image URL.
    '''
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    '''
    Extracts markdown link syntax from the input text and returns a list of tuples containing the anchor text and URL.
    '''
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text):
    '''
    Converts a plain text string into a list of TextNodes with text type TextType.TEXT.
    '''
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, delimiter="**", text_type=TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, delimiter="_", text_type=TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, delimiter="`", text_type=TextType.CODE) 
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    '''
    Converts a markdown string into a list of blocks, where each block is a list of TextNodes.
    '''
    # Split the markdown into lines and process each line separately
    lines = markdown.split("\n\n")
    blocks = []
    for line in lines:
        if line.strip() == "":
            continue  # Skip empty lines
        blocks.append(line.strip("\n"))
    print(blocks)
    return blocks





if __name__ == "__main__":
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))