from textnode import TextNode, TextType

def main():
    print("hello")
    text_node = TextNode("some string", TextType.BOLD, "https://www.google.com")
    print(text_node)


main()