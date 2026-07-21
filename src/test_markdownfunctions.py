import unittest
from markdownfunctions import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownFuntions(unittest.TestCase):
    def test_markdown_to_block(self):
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
    
    def test_markdown_to_block_excess_newline(self):
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
    
    def test_block_to_block_type_heading(self):
        block = "# this is a heading"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, result)

    def test_block_to_block_type_invalid_heading(self):
        block = "#this is a heading"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_paragraph(self):
        block = """This is a paragraph
with 2 lines
"""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_paragraph_second_line_whitespace(self):
        block = """This is a paragraph
                     with 2 lines""" 
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_code(self):
        block = """```
this is codeblock
with mulitple lines ```"""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, result)

    def test_block_to_block_type_code_invalid(self):
        block = """```
        this is a broken codeblock
with mulitple lines ``"""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_quote(self):
        block = """>this is a quote
> with multiple lines"""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, result)

    def test_block_to_block_type_quote_invalid(self):
        block = """>this is a quote
> with multiple lines
- I added a wrong starting char
"""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_unordered_list(self):
        block = """-this is a list
- that uses no numbers"""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, result) 

    def test_block_to_block_type_ordered_list(self):
        block = """1. this is a list
2. that uses numbers"""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, result) 

    def test_block_to_block_type_ordered_list_invalid_ordering(self):
        block = """2. this is a bad list
1. that uses numbers wrongly
"""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result) 
        

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

    def test_headings(self):
        md = """
# Heading1

## Heading2 **with some bold text**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h1>Heading1</h1><h2>Heading2 <b>with some bold text</b></h2></div>",
    )

    def test_blockquote(self):
            md = """
> this is a quote

> this is a quote
> with a secondline
    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html,
            "<div><blockquote>this is a quote</blockquote><blockquote>this is a quote with a secondline</blockquote></div>",
        )

    def test_unorderedlist(self):
            md = """
- this is an unordered list
- this is the second item in the list
- this is the third item
    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html,
            "<div><ul><li>this is an unordered list</li><li>this is the second item in the list</li><li>this is the third item</li></ul></div>",
        )
            
    def test_orderedlist(self):
            md = """
1. this is an unordered list
2. this is the second item in the list
3. this is the third item
    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html,
            "<div><ol><li>this is an unordered list</li><li>this is the second item in the list</li><li>this is the third item</li></ol></div>",
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