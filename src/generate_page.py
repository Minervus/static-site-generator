import re
import os
import shutil
from split_delimiter import *


# 1. extract_title(markdown)
def extract_title(markdown):
    lines = markdown_to_blocks(markdown)

    # print(f"Lines list: {lines}")
    # print(f"lines list length: {len(lines)}")

    is_header = any(x.startswith("# ") for x in lines)

    #print(f"is_header resolves to: {is_header}")
    
    
    if is_header:
        for line in lines:
            if line.startswith("# "):
                header = line
        hash_stripped = re.sub(r'[^a-zA-Z0-9]',' ',header)
        return hash_stripped.strip()
    else:
        raise Exception("No Heading Found")


# check if h1 header exists
# if yes - return header text with # stripped and spaces removed
# if no - raise an exception

# 2. generate_page(from_path, template_path, dest_path)
def generate_page(from_path, template_path, dest_path, basepath):
    # Print message ("Generating page from from_path to dest_path using template_path")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Take markdown file at from_path and store in a variable
    # open it first?
    with open(from_path, 'r') as file:
        markdown_content = file.read()
    

    # Take template file at template_path and store in a variable
    with open(template_path, 'r') as file:
        template_content = file.read()

    # print(f"THIS IS THE MARKDOWN: {markdown_content}")
    # Use markdown_to_html_node and .tohtml() to convert markdown to html string
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()

    # Use extract_title (from above) to grab the title of the page
    page_title = extract_title(markdown_content)

    # Replace {{ Title }} and {{ Content }} in the template with HTML and title

    updated_template = template_content.replace("{{ Title }}",page_title)
    updated_template = updated_template.replace("{{ Content }}", html_string)
    updated_template = updated_template.replace('"href="/"', f"href={basepath}")
    updated_template = updated_template.replace('"src="/"', f"src={basepath}")

    # Write new full HTML page to a file at dest_path (create any necessary directories that don't exist)
    # check if dest_path exists - create it if not
    dest_dir = os.path.dirname(dest_path)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as created_html:
        created_html.write(updated_template)

    # Make directory for dest_path

# Genenerate pages percursively https://www.boot.dev/lessons/50bf720d-808f-4a55-9dab-cea526a8d734

def generate_pages_recursively(source_path, template_path, destination_path,basepath):

    # Crawl every entry in content directory
    for item in os.listdir(source_path):
        current_source_path = os.path.join(source_path,item)
        current_destination_path = os.path.join(destination_path,item)

        if os.path.isfile(current_source_path):
            os.makedirs(os.path.dirname(current_destination_path), exist_ok=True)

            file_tup = os.path.splitext(current_source_path)
            file_path = file_tup[0]
            file_extension = file_tup[1]
            # print(f"file_tup :{file_tup}")
            file_list = file_path.split('/')
            # print(f"file LIST: {file_list}")
            # print(f"index file name: {file_list[-1]}")
            # print(f"CURRENT DESTINATION PATH: {current_destination_path}")
            destination_tup = os.path.splitext(current_destination_path)
            # print(f"Destination TUP: {destination_tup}")
            final_destination = destination_tup[0] + '.html'
            print(f"FINAL DESTINATION: {final_destination}")
            

            if file_extension == '.md':
                    # html_file_name = file_path + '.html'
                    generate_page(current_source_path,template_path,final_destination,basepath)
            else:
                shutil.copy(current_source_path,current_destination_path)
        elif os.path.isdir(current_source_path):
            if not os.path.exists(current_destination_path):
                try:
                    os.mkdir(current_destination_path)
                    print(f"Created directory: {current_destination_path}")
                except FileExistsError:
                    print(f"Directory already exists: {current_destination_path}")
                except Exception as e:
                    print(f"Failed to create directory: {current_destination_path} due to {e}")
            generate_pages_recursively(current_source_path,template_path,current_destination_path)





