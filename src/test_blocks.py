import unittest
from markdown_to_blocks import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node, blocks_and_types, split_markdown_to_blocks, blocks_to_html_nodes
from textnode import TextNode, TextType

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            )
    def test_heading_block_type(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    def test_code_block_type(self):
        block = "```This is a code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    def test_quote_block_type(self):
        block = "> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
    def test_unordered_list_block_type(self):
        block = "- This is an unordered list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    def test_ordered_list_block_type(self):
        block = "1. This is an ordered list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    def test_paragraph_block_type(self):
        block = "This is a normal paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_quote(self):
        md = """
    > This is a quote with **bold** text and _italic_ text and `code` and a [link](https://boot.dev)
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> text and <i>italic</i> text and <code>code</code> and a <a href=\"https://boot.dev\">link</a></blockquote></div>",
        )
    
    def test_unordered_list(self):
        md = """
    - Item 1 with **bold** text
    - Item 2 with _italic_ text
    - Item 3 with `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1 with <b>bold</b> text</li><li>Item 2 with <i>italic</i> text</li><li>Item 3 with <code>code</code></li></ul></div>",
        )   
    
    def test_ordered_list(self):
        md = """
    1. Item 1 with **bold** text
    2. Item 2 with _italic_ text
    3. Item 3 with `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1 with <b>bold</b> text</li><li>Item 2 with <i>italic</i> text</li><li>Item 3 with <code>code</code></li></ol></div>",
        )
    
    def test_headings(self):
        md = """
    # Heading 1

    ## Heading 2

    ### Heading 3

    #### Heading 4

    ##### Heading 5

    ###### Heading 6
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )
    
            

if __name__ == "__main__":    
    unittest.main()   