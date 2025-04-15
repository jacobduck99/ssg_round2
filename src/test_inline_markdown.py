import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNode(unittest.TestCase):
    def test_single_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)


        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ], 
        result,
        )


    def test_no_delimiter(self):
        node = TextNode("This is text has no delimiter", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual([node], result)


    def test_multiple_delimiters(self):
        node = TextNode("This is text with two delimiters **here is one** and **here is two**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual([
            TextNode("This is text with two delimiters ", TextType.TEXT),
            TextNode("here is one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("here is two", TextType.BOLD),
            TextNode("", TextType.TEXT)
        ],
        result,
        )

    def test_only_delimiter(self):
        node = TextNode("**This is all code**", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual([
            TextNode("", TextType.TEXT),
            TextNode("This is all code", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ],
            result,
        )


    def test_wrong_delimiters(self):
        node = TextNode("this is wrong delimiters **can you see them__ ?", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        



        















if __name__ == "__main__":
    unittest.main()