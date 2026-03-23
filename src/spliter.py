import re
from textnode import TextNode 
from textnode import TextType

def split_nodes_delimiter(old_nodes:list, delimieter:str, text_type:TextType.CODE) -> list:
    '''
    takes a list of "old nodes", a delimiter, and a text type. Returns a list of new nodes 
    where the text of each old node is split by the delimiter 
    and wrapped in a new TextNode with the specified text type.
    '''
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.CODE:
            # Split the text of the node by the delimiter
            if delimieter not in node.text:
                raise Exception(f"Delimiter '{delimieter}' not found in node text: '{node.text}'")
            split_texts = re.split(delimieter, node.text)
            for split_text in split_texts:
                new_nodes.append(TextNode(split_text, text_type))
        else:
            new_nodes.append(node)
    return new_nodes
