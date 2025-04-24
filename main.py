from src.utils.utils import md_to_htmlnode
from src.utils.block_checker import get_block_type

if __name__ == "__main__":
    md1 = """
    - this is a list with trailing spaces  
    - and without 
    - okay
    """
    md2 = """
    > quote line 1 with trailing spaces  
    > quote line 2 without trailing spaces
    > quote line 3
    """
    md3 = """
    Para line 3 with **bold** text
    """
    node = md_to_htmlnode(md3)
    print(rf"{node.to_html()}")
    print("-" * 50)
    # node = md_to_htmlnode(md2)
    # print(node.to_html())
    # print("-" * 50)
    # node = md_to_htmlnode(md3)
    # print(node.to_html())
