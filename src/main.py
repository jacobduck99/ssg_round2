import os
import shutil

from copy_static import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static  = "./static"
dir_path_content = "./content"
dir_path_public  = "./public"

def main():
    print("Deleting public directory…")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying files from static to public…")
    copy_files_recursive(dir_path_static, dir_path_public)
    
    print("Generating HTML pages from markdown…")
    generate_pages_recursive(
        dir_path_content,   # scan every folder under content/
        "template.html",    # your page template
        dir_path_public     # mirror into public/
    )

if __name__ == "__main__":
    main()
