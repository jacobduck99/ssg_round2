import unittest

from gencontent import extract_title

from markdown_blocks import markdown_to_html_node

class TestExtractTitle(unittest.TestCase):
    def test_extracts_h1(self):
        md = """
# Hello World


This is some paragraph text.
"""
        self.assertEqual(extract_title(md), "Hello World")

    def test_raises_when_no_h1(self):
        md = """
## This is a subtitle


Some content here.
"""
        with self.assertRaises(Exception):
            extract_title(md)
        