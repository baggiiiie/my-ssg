from textnode import TextNode, TextType


def main():
    my_node = TextNode("text", TextType.LINK, "www.google.com")
    print(my_node)


if __name__ == "__main__":
    main()
