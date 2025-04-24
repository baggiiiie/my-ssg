from src.utils.utils import md_to_htmlnode

if __name__ == "__main__":
    md3 = """
        this is a [link](https://test) and an ![img](img_link)
        """

    node = md_to_htmlnode(md3)
    print(rf"{node.to_html()}")
    print("-" * 50)
    # node = md_to_htmlnode(md2)
    # print(node.to_html())
    # print("-" * 50)
    # node = md_to_htmlnode(md3)
    # print(node.to_html())
