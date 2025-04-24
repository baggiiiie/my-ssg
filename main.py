from src.utils.utils import md_to_htmlnode
from src.utils.block_checker import get_block_type

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
    # node = md_to_htmlnode(md1)
    # print(node.to_html())
    # print("-" * 50)
    # node = md_to_htmlnode(md2)
    # print(node.to_html())
    print(get_block_type(md2))
