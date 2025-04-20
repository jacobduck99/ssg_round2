import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class TestMarkdownToHTML(unittest.TestCase):
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
        


    def test_collapse_multiple_blank_lines(self):
        md = "Para1\n\n\n\nPara2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
        [
            "Para1",
            "Para2",
        ]
    )


    def test_no_lines(self):
        md = """ 
This is a line with no line lol"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is a line with no line lol"
        ],
    )
        
    
    def test_empty_string_returns_empty(self):
        md = ""
        self.assertEqual(markdown_to_blocks(md), [])


    def test_headings(self):
        block = "# This is me testing the heading"

        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_code(self):
        block = "```\n this is code \n```"

        self.assertEqual(block_to_block_type(block), BlockType.CODE)


    def test_quotes(self):
        block = "> this is a quote"

        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_lists(self):
        block = "- This is a unordered list"

        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)


    def test_ordered_lists(self):
        block = "1. This is a ordered list"

        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        block = "This is just a paragraph"

        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_no_input(self):

        block = ""

        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


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
        

    def test_headings(self):
        md = """
# Heading Level 1


## Heading Level 2


### Heading Level 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading Level 1</h1><h2>Heading Level 2</h2><h3>Heading Level 3</h3></div>"
        )



    def test_ordered_lists(self):
        md = """
This is an ordered list

1. item
2. item
3. item

and that is the end of the list
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div>"
        "<p>This is an ordered list</p>"
        "<ol>"
        "<li> item</li>"
        "<li> item</li>"
        "<li> item</li>"
        "</ol>"
        "<p>and that is the end of the list</p>"
        "</div>"
    )
        


    def test_unordered_lists_with_html(self):
        md = """
This is an unordered list

- item 1
- item 2
- item 3

and that is the end of the list
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div>"
        "<p>This is an unordered list</p>"
        "<ul>"
        "<li>item 1</li>"
        "<li>item 2</li>"
        "<li>item 3</li>"
        "</ul>"
        "<p>and that is the end of the list</p>"
        "</div>"
    )
        

    def test_headings_with_bold(self):
        md = """
# **Heading with bold**


and now just normal text
"""


        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div>"
            "<h1><b>Heading with bold</b></h1>"
            "<p>and now just normal text</p>"
            "</div>"
        )


    def test_heading_with_italic(self):
        md = """
### _Heading with italic_


and now just normal text
"""


        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div>"
            "<h3><i>Heading with italic</i></h3>"
            "<p>and now just normal text</p>"
            "</div>"
        )

    def test_headings_with_italic(self):
        md = """
# _Heading1 with italic_


## _Heading2 with italic_


### _Heading3 with italic_

and now just normal text
"""


        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div>"
            "<h1><i>Heading1 with italic</i></h1>"
            "<h2><i>Heading2 with italic</i></h2>"
            "<h3><i>Heading3 with italic</i></h3>"
            "<p>and now just normal text</p>"
            "</div>"
        )


    def test_inline_link(self):
        md = """
Click [here](https://example.com) for more info.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Click <a href=\"https://example.com\">here</a> for more info.</p></div>"
        )
        

    def test_inline_images(self):
        md = """
Here is a ![image](https://i.imgur.com/3elNhQu.png) how cool is it.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div>"
        "<p>Here is a <img src=\"https://i.imgur.com/3elNhQu.png\" alt=\"image\"></img> how cool is it.</p>"
        "</div>"
    )
        





