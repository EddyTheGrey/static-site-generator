import os
from markdown_to_blocks import markdown_to_html_node
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode 




def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()     
    raise Exception("No title found in markdown")

def generate_page(from_path, template_path, dest_path, base_url="/"):
    print("Generating page from: " + from_path + " to " + dest_path +"using " + template_path+'.')
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    nodes = markdown_to_html_node(markdown)
    html_string = nodes.to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Content }}", html_string)
    template = template.replace("{{ Title }}", title)
    template = template.replace('src="/', f'src="{base_url}')
    template = template.replace('href="/', f'href="{base_url}"')
    with open(dest_path, 'w') as f:
        f.write(template)
    
def generate_pages_recursive(dir_path, template_path, dest_dir_path, base_url="/"):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path)
                dest_path = os.path.join(dest_dir_path, relative_path[:-3] + ".html")
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(from_path, template_path, dest_path, base_url)

if __name__ == "__main__":
    title = extract_title("# Hello World\nThis is some markdown content.")
    print(f"Extracted title: {title}")

