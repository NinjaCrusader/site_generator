import unittest
from node_splitter import *

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


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
    
    
    def test_split_images_no_image(self):
        node = TextNode("This is just plain text.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is just plain text.", TextType.TEXT)],
            new_nodes,
        )
    

    def test_split_images_only_image(self):
        node = TextNode("![alt text](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")],
            new_nodes,
        )
    

    def test_split_images_start_and_end(self):
        node = TextNode(
            "![start](https://example.com/start.png) some text ![end](https://example.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" some text ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )
    

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("Text before image ![img1](https://img.com/1.png)", TextType.TEXT),
            TextNode("Just plain text", TextType.TEXT),
            TextNode("![img2](https://img.com/2.png) end text", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Text before image ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://img.com/1.png"),
                TextNode("Just plain text", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://img.com/2.png"),
                TextNode(" end text", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_images_malformed_syntax(self):
        node = TextNode("This is ![not an image](missing end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is ![not an image](missing end", TextType.TEXT)],
            new_nodes,
        )



    def test_plain_text(self):
        input_text = "Hello, world!"
        expected = [TextNode("Hello, world!", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(input_text), expected)

    def test_bold_text(self):
        input_text = "This is **bold** text."
        result = text_to_textnodes(input_text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT)
        ])

    def test_italic_text(self):
        input_text = "Some _italic_ word."
        result = text_to_textnodes(input_text)
        self.assertEqual(result, [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT)
        ])

    def test_code_text(self):
        input_text = "Use `print()` to output."
        result = text_to_textnodes(input_text)
        self.assertEqual(result, [
            TextNode("Use ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" to output.", TextType.TEXT)
        ])

    def test_image_parsing(self):
        input_text = "Here is an image ![cat](http://cat.com/cat.jpg)"
        result = text_to_textnodes(input_text)
        self.assertEqual(result, [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "http://cat.com/cat.jpg")
        ])

    def test_link_parsing(self):
        input_text = "Check this [link](http://example.com)"
        result = text_to_textnodes(input_text)
        self.assertEqual(result, [
            TextNode("Check this ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com")
        ])

    def test_combined_markdown(self):
        input_text = "Here is a **bold** word and an _italic_ one. Also `code`, a [link](http://a.com), and ![img](http://img.com/img.png)."
        result = text_to_textnodes(input_text)

        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" one. Also ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://a.com"),
            TextNode(", and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "http://img.com/img.png"),
            TextNode(".", TextType.TEXT)
        ]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()