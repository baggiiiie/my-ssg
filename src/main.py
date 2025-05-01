from utils.file_utils import copy_dir
from utils.utils import generate_pages


if __name__ == "__main__":
    copy_dir()
    generate_pages(src_dir="content", dst_dir="public")
