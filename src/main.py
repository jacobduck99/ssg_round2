import os
import shutil
import sys

from copy_static import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static  = "./static"
dir_path_content = "./content"
dir_path_docs = "./docs"

def main():

    args = sys.argv

    if len(args) > 1:
        base_path = args[1]
    else:
        base_path = "/"

    if not base_path.endswith("/"):
        base_path += "/"

    print(f"Using base_path = {base_path!r}")

    print("Deleting docs directory…")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying files from static to docs…")
    copy_files_recursive(dir_path_static, dir_path_docs)
    
    if not os.path.exists(dir_path_docs):
        os.makedirs(dir_path_docs, exist_ok=True)

    print("Generating HTML pages from markdown…")
    generate_pages_recursive(
        dir_path_content,   # scan every folder under content/
        "template.html",    # your page template
        dir_path_docs, 
        base_path     # mirror into public/
    )

if __name__ == "__main__":
    main()
