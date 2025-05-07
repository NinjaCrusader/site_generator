import unittest
from block_splitter import *
from htmlnode import ParentNode, HTMLNode, LeafNode


class TestBlockSplitter(unittest.TestCase):
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


    def test_single_paragraph(self):
        md = "This is just one paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just one paragraph."])

    def test_multiple_paragraphs(self):
        md = """
This is the first paragraph.

This is the second paragraph.

This is the third paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is the first paragraph.",
                "This is the second paragraph.",
                "This is the third paragraph.",
            ],
        )

    def test_paragraph_with_multiple_lines(self):
        md = """
This is a paragraph
that spans multiple lines.

And this is another.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph\nthat spans multiple lines.",
                "And this is another.",
            ]
        )

    def test_list_blocks(self):
        md = """
- Item 1
- Item 2

- Item 3
- Item 4
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- Item 1\n- Item 2",
                "- Item 3\n- Item 4"
            ]
        )

    def test_extra_blank_lines_and_whitespace(self):
        md = """


    First paragraph with leading and trailing whitespace.    




    Second paragraph.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph with leading and trailing whitespace.",
                "Second paragraph.",
            ]
        )

    def test_example_case_from_prompt(self):
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


    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Smallest heading"), BlockType.HEADING)

    def test_code(self):
        self.assertEqual(block_to_block_type("```print('hello')```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```code block```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Another quote"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item one"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Another item"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("2. Second item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("10. Tenth item"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is just a paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Hello world!"), BlockType.PARAGRAPH)


    




if __name__ == "__main__":
    unittest.main()