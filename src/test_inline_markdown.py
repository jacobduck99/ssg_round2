import unittest

from inline_markdown import (split_nodes_delimiter, 
                             extract_markdown_images, 
                             extract_markdown_links, 
                             split_nodes_image,
                             split_nodes_link, 
                             text_to_textnodes)

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
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")

        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_no_images(self):
        result = extract_markdown_images("This has no images in it")

        self.assertListEqual([], result)

    def test_no_links(self):
        result = extract_markdown_links("this has no links in it")

        self.assertListEqual([], result)


    def test_multiple_links(self):
        matches = extract_markdown_links("This is text with an [link](https://www.google.com), here is another [link](https://www.google.com), and here is another [link](https://www.google.com)")
        self.assertListEqual([
        ("link", "https://www.google.com"),
        ("link", "https://www.google.com"),
        ("link", "https://www.google.com")
    ], matches)
        

    def test_multiple_images(self):
        matches = extract_markdown_images("This is text with an image ![image](https://i.imgur.com/zjjcJKZ.png) and here have another ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([
        ("image", "https://i.imgur.com/zjjcJKZ.png"),
        ("image", "https://i.imgur.com/zjjcJKZ.png"),
        ("image", "https://i.imgur.com/zjjcJKZ.png")

        ], matches)


    def test_empty_string_images(self):
        result = extract_markdown_images("")

        self.assertListEqual([], result)


    def test_empty_string_links(self):
        result = extract_markdown_links("")

        self.assertListEqual([], result)


    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another "
        "![second image](https://i.imgur.com/3elNhQu.png)",
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
        

    def test_no_images_in_text(self):
        node = TextNode(
            "This is text with no images", TextType.TEXT
            )

        new_nodes = split_nodes_image([node])
        expected = [TextNode("This is text with no images", TextType.TEXT)]
        self.assertListEqual(expected, new_nodes)

    
    def test_no_links_in_text(self):
        node = TextNode("This is text with no links in it", TextType.TEXT)

        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is text with no links in it", TextType.TEXT)]
        self.assertListEqual(expected, new_nodes)


    def test_single_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/example.png) in it", 
        TextType.TEXT)

        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/example.png"),
            TextNode(" in it", TextType.TEXT)
        ], new_nodes)


    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
        "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/3elNhQu.png) and a [link](https://www.google.com)"
    )
        self.assertListEqual(
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com"),
        ],
        nodes,
    )




if __name__ == "__main__":
    unittest.main()