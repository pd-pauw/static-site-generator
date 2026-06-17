import unittest
from markdownfunctions import markdown_to_blocks, block_to_block_type, BlockType

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
        