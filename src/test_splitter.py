import unittest
from spliter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [
            TextNode("This is code text with a delimiter", TextType.CODE),
            TextNode("This is normal text", TextType.NORMAL)
        ]
        delimiter = " "
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, TextType.CODE)
        expected_new_nodes = [
            TextNode("This", TextType.CODE),
            TextNode("is", TextType.CODE),
            TextNode("code", TextType.CODE),
            TextNode("text", TextType.CODE),
            TextNode("with", TextType.CODE),
            TextNode("a", TextType.CODE),
            TextNode("delimiter", TextType.CODE),
            TextNode("This is normal text", TextType.NORMAL)
        ]
        self.assertEqual(new_nodes, expected_new_nodes)


    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = [
            TextNode("This is code text without the delimiter", TextType.CODE)
        ]
        delimiter = ","
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(old_nodes, delimiter, TextType.CODE)
        self.assertIn("Delimiter ',' not found in node text: 'This is code text without the delimiter'", str(context.exception))
