import textnode
import os
import shutil
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from page_generator import generate_page, generate_pages_recursive

def main():
    obj =textnode.TextNode("This is some anchor text", textnode.TextType.LINK, "https://www.boot.dev")
    print('TextNode('+str(obj)+')')
    clear_public_directory()
    copy_static_files()
    arg = sys.argv[1] if len(sys.argv) > 1 else '/'
    generate_all_pages()
    generate_pages_recursive("content", "template.html", "docs", arg)


def clear_public_directory():
    public_dir = 'docs'
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)

def copy_static_files():
    static_dir = 'static'
    public_dir = 'docs'
    if os.path.exists(static_dir):
        for item in os.listdir(static_dir):
            s = os.path.join(static_dir, item)
            d = os.path.join(public_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

def generate_all_pages():
    pages = [
        {
            "from_path": "content/index.md",
            "template_path": "template.html",
            "dest_path": "docs/index.html"
        }
    ]
    for page in pages:
        generate_page(page["from_path"], page["template_path"], page["dest_path"])

if __name__ == "__main__":
    main()