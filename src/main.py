from textnode import *
from directory_copy import *
from generate_page import *


def main(text,text_type,url):
    dummy_node = TextNode(text,text_type,url)
    print(dummy_node)

# path to source directory
source_path = 'content'

# path to destination directory
destination_path = 'public'

# main("text test", TextType.BOLD,"https://google.com")

from_path = 'content/index.md'
template_path = 'template.html'
dest_path = 'public/index.html'

# Delete public directory and copy files from static to public
copy_files(source_path,destination_path)

# copy content files to public


# Generate page from content/index.md using template.html and write to public/html


generate_pages_recursively(source_path,template_path,destination_path)
