import os
import shutil

SRC_PATH = "static"
DST_PATH = "public"


def copy_dir(src_dir: str = SRC_PATH, dst_dir: str = DST_PATH) -> None:
    def _copy_dir_helper(src_dir: str, dst_dir: str) -> None:
        # list and loop thru all content in src dir
        # if file,
        #   copy src file to dst dir
        # if dir,
        #   create dir in dst dir
        #   recursion
        dir_content = os.listdir(src_dir)
        os.mkdir(dst_dir)
        for content in dir_content:
            if content.startswith("_"):
                continue
            dir = os.path.join(src_dir, content)
            if os.path.isdir(dir):
                dest_dir = os.path.join(dst_dir, content)
                copy_dir(dir, dest_dir)
            else:
                shutil.copy(dir, dst_dir)

    if not os.path.exists(src_dir):
        print(f"Source directory does not exist: {str(src_dir)}")
        return
    if os.path.exists(dst_dir):
        print(f"Destination directory already exists, nuking it: {str(dst_dir)}")
        shutil.rmtree(dst_dir)
    _copy_dir_helper(src_dir, dst_dir)


# __AUTO_GENERATED_PRINT_VAR_START__
if __name__ == "__main__":
    # Test the functions
    print("Testing file utilities")
    cwd = os.getcwd()
    print(f" cwd: {str(cwd)}")
    test_dir = os.path.join(cwd, "src")
    dst_path = os.path.join(cwd, DST_PATH)
    copy_dir(test_dir, dst_path)  # __AUTO_GENERATED_PRINT_VAR_END__
