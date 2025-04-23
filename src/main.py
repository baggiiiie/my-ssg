from src.utils.utils import md_to_htmlnode

if __name__ == "__main__":
    md1 = """
    ```
    This is text that _should_ remain 
    the **same** even with inline stuff
    ```

    """
    md2 = """
    - this is a list 
    - another item
        """
    node = md_to_htmlnode(md1)
    print(node.to_html())
    print()
    node = md_to_htmlnode(md2)
    print(node.to_html())
