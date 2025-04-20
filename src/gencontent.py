import os
from markdown_blocks import markdown_to_html_node
import re


def extract_title(markdown):
    split_markdown = markdown.split("\n")

    for line in split_markdown:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
        
    raise Exception("No header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as data:
        contents = data.read().strip()  # Strip any extra spaces in markdown

    with open(template_path, "r") as data: 
        template = data.read()

    html_node = markdown_to_html_node(contents)
    html = html_node.to_html().strip()  # Strip whitespace from generated HTML

    title = extract_title(contents).strip()  # Strip spaces from title

    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html).strip()

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_html)

    print("Final HTML successfully written!")



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    with open(template_path, "r") as f:
        template = f.read()

    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)

    entries = os.listdir(dir_path_content)


    for entry in entries:
        
        src_path = os.path.join(dir_path_content, entry)
        base_dest = os.path.join(dest_dir_path, entry)
        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, base_dest)

        elif entry.endswith(".md"):
            with open(src_path, "r") as f:
                contents = f.read().strip()
            #####ADDED THIS TO TRY AND GET THE CONTACT ME TO HAVE A SPACE
            contents = re.sub(r'([^\s])(\[)', r'\1 \2', contents)
            #######
            html = markdown_to_html_node(contents).to_html().strip()
            title = extract_title(contents).strip()

            final_html = template.replace("{{ Title }}", title) \
                     .replace("{{ Content }}", html)
            
            name, _ = os.path.splitext(entry)
            html_name = name + ".html"

            out_path = os.path.join(dest_dir_path, html_name)

            with open(out_path, "w") as out:
                out.write(final_html)





        


