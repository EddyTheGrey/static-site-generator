import unittest
from spliter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestSplitter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [
            TextNode("This is code text with a delimiter", TextType.TEXT),
            TextNode("This is normal text", TextType.NORMAL)
        ]
        delimiter = " "
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, TextType.TEXT)
        expected_new_nodes = [
            TextNode("This", TextType.TEXT),
            TextNode("is", TextType.TEXT),
            TextNode("code", TextType.TEXT),
            TextNode("text", TextType.TEXT),
            TextNode("with", TextType.TEXT),
            TextNode("a", TextType.TEXT),
            TextNode("delimiter", TextType.TEXT),
            TextNode("This is normal text", TextType.NORMAL)
        ]
        self.assertEqual(new_nodes, expected_new_nodes)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.example2.com"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **bold** and _italic_ text with a [link](https://example.com) and ![image](https://i.imgur.com/image.png)"
        new_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" text with a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/image.png"),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()