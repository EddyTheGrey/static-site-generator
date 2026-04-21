import unittest
from page_generator import extract_title

class TestPageGenerator(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello World\nThis is some markdown content."
        title = extract_title(md)
        self.assertEqual(title, "Hello World")

    def test_extract_title_no_title(self):
        md = "This is some markdown content without a title."
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertTrue("No title found in markdown" in str(context.exception))

if __name__ == "__main__":
    unittest.main()