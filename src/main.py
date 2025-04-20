import os
import shutil
import sys

from copy_static import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static  = "./static"
dir_path_content = "./content"
dir_path_public = "./docs"
template_path = "./template.html"
default_basepath = "/"

def main():

    base_path = default_basepath

    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    if not base_path.endswith("/"):
        base_path += "/"

    print(f"Using base_path = {base_path!r}")

    print("Deleting docs directory…")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying files from static to docs…")
    copy_files_recursive(dir_path_static, dir_path_public)
    
    if not os.path.exists(dir_path_public):
        os.makedirs(dir_path_public, exist_ok=True)

    print("Generating HTML pages from markdown…")
    generate_pages_recursive(
        dir_path_content,   # scan every folder under content/
        template_path,    # your page template
        dir_path_public, 
        base_path     # mirror into public/
    )

if __name__ == "__main__":
    main()
