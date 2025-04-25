import os

DST_PATH = "public"


def nuke_dir(directory: str) -> None:
    # delete all files in the directory
    ...


def check_create_dir(dst_dir: str) -> None:
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)


def copy_dir(): ...
