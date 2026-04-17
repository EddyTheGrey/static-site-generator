import re

from textnode import TextNode, TextType
from spliter import split_nodes_delimiter, split_nodes_image, split_nodes_link 



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
    list_of_text = split_nodes_delimiter([TextNode(text, TextType.TEXT)], " ", TextType.TEXT)
    
    for i in range(len(list_of_text)):
        if list_of_text[i].text_type == TextType.TEXT:
            list_of_text[i] = split_nodes_image(list_of_text[i])
    for i in range(len(list_of_text)):
        if list_of_text[i].text_type == TextType.TEXT:
            list_of_text[i] = split_nodes_link(list_of_text[i])
    # Flatten the list of lists into a single list of TextNodes
    flat_list_of_text = []
    for item in list_of_text:
        if isinstance(item, list):
            flat_list_of_text.extend(item)
        else:
            flat_list_of_text.append(item)
    return flat_list_of_text

if __name__ == "__main__":
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))