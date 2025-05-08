import shutil
import os
import sys
from block_splitter import markdown_to_blocks, markdown_to_html_node
from htmlnode import *
from pathlib import Path


def copy_static_to_public(source_path, dest_path):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
        print(f"Created directory: {dest_path}")

    items = os.listdir(source_path)

    for item in items:
        source_item_path = os.path.join(source_path, item)
        dest_item_path = os.path.join(dest_path, item)

        if os.path.isfile(source_item_path):
            shutil.copy(source_item_path, dest_item_path)
            print(f"Copied file: {source_item_path} -> {dest_item_path}")
        else:
            copy_static_to_public(source_item_path, dest_item_path)


def get_files_ready(script_dir):
    docs_dir = "docs"
    static_dir = "static"
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
        print("Content in docs dictionary was deleted!")
    os.mkdir(docs_dir)
    if not os.path.exists(static_dir):
        print("Error: Static directory not found!")
        return
    copy_static_to_public(static_dir, docs_dir)


def extract_title(markdown):
    markdown_blocked = markdown_to_blocks(markdown)
    for block in markdown_blocked:
        if block.startswith('# '):
            stripped_string = block[2:].strip()
            return stripped_string
    raise Exception("No h1 was provided")

# Create a generate_page(from_path, template_path, dest_path) function. It should:

#     Print a message like "Generating page from from_path to dest_path using template_path".
#     Read the markdown file at from_path and store the contents in a variable.
#     Read the template file at template_path and store the contents in a variable.
#     Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
#     Use the extract_title function to grab the title of the page.
#     Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
#     Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Path {from_path} does not exist")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Path {template_path} does not exist")
    print("Reading files in paths...")
    with open(from_path) as fpath:
        read_from = fpath.read()
    with open(template_path) as tpath:
        read_temp = tpath.read()
    print("Done reading files and now creating html content...")
    html_content = markdown_to_html_node(read_from).to_html()
    print("Done creating html content...")
    print("Extracting title...")
    title = extract_title(read_from)
    print("Putting the Title and Content in the final html file. Please wait...")
    final_html = read_temp.replace("{{ Title }}", title).replace("{{ Content }}", html_content).replace('href="/', f'href={basepath}').replace('src="/', f'src={basepath}')
    print("On to the next step")
    directory_path = os.path.dirname(dest_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    with open(dest_path, "w") as f:
        print("Waiting for file")
        f.write(final_html)
        print(dest_path + " " + "was made")
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Checking if {dir_path_content} exists...")
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"Path {dir_path_content} does not exist")
    print(f"Congrats {dir_path_content} exists! Now taking a peek at the content...")
    content_path = Path(dir_path_content)
    for item in content_path.iterdir():
        if item.is_file():
            if item.suffix == ".md":
                print(f"found a markdown file! {item} and checking if the destination file exists...")
                if not os.path.exists(dest_dir_path):
                    os.makedirs(dest_dir_path, exist_ok=True)
                print("Reading tmeplate path...")
                with open(template_path) as tpath:
                    read_temp = tpath.read()
                with open(item) as ipath:
                    read_mark = ipath.read()
                print(f"Generating html file from {item}...")
                html_content = markdown_to_html_node(read_mark).to_html()
                print("content converted to html, now extracting title...")
                title = extract_title(read_mark)
                print("Putting the Title and Content in the final html file. Please wait...")
                final_html = read_temp.replace("{{ Title }}", title).replace("{{ Content }}", html_content).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
                relative_path = item.relative_to(content_path)
                output_filename = relative_path.with_suffix('.html')
                output_path = Path(dest_dir_path) / output_filename
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w') as f:
                    f.write(final_html)
        elif item.is_dir():
            new_dest_dir = Path(dest_dir_path) / item.name
            new_dest_dir.mkdir(parents=True, exist_ok=True)
            generate_pages_recursive(item, template_path, new_dest_dir, basepath)

        
    
        



def main():
  if len(sys.argv) > 1:
    basepath = sys.argv[1]
  else:
    basepath = '/'
  script_dir = os.path.dirname(os.path.abspath(__file__))  
  get_files_ready(script_dir)
  content_path = "content"
  template_path = "template.html"
  docs_path = "docs"
  generate_pages_recursive(content_path, template_path, docs_path, basepath)  
    
    




if __name__ == "__main__":
    main()
