from extractor import *
import re
from textnode import *



def split_nodes_link(old_nodes):
    result = []

    # Loop through list of old_nodes
    for node in old_nodes:
        # if the node's text type is NOT TEXT
        if node.text_type != TextType.TEXT:
            # add node to results list
            result.append(node)
            continue
        # extract image alt text and image links to list of tuples using extractor
        links = extract_markdown_links(node.text)

        # if no images then append node to result list
        if not links:
            result.append(node)
            continue

        # store node's text into current_text    
        current_text = node.text
        # while images is True
        while links:
            # assign alt and img from first tuple in images list
            alt, link = links[0]

            # store markdown image as string e.g. ![alt text for image](url/of/image.jpg)
            markdown_link = f"[{alt}]({link})"

            # split text string into parts, using markdown_image as 'splitter'
            split_parts = current_text.split(markdown_link, maxsplit=1)
            before_link = split_parts[0]
            
            # strip white space
            if before_link.strip():
                # append text TextNode
                result.append(TextNode(before_link, TextType.TEXT))
            # append image Text Node
            result.append(TextNode(alt, TextType.LINK, url=link))

            # this is grabbing the "and" or text after the text before the 
            # image if there was more text i.e. text between the images
            current_text = split_parts[1] if len(split_parts) > 1 else ""
            
            
            links = extract_markdown_links(current_text)

        if current_text.strip():
            result.append(TextNode(current_text, TextType.TEXT))

    return result


def split_nodes_image(old_nodes):
    result = []

    # Loop through list of old_nodes
    for node in old_nodes:
        # if the node's text type is NOT TEXT
        if node.text_type != TextType.TEXT:
            # add node to results list
            result.append(node)
            continue
        # extract image alt text and image links to list of tuples using extractor
        images = extract_markdown_images(node.text)

        # if no images then append node to result list
        if not images:
            result.append(node)
            continue

        # store node's text into current_text    
        current_text = node.text
        # while images is True
        while images:
            # assign alt and img from first tuple in images list
            alt, img = images[0]

            # store markdown image as string e.g. ![alt text for image](url/of/image.jpg)
            markdown_image = f"![{alt}]({img})"
            
            # split text string into parts, using markdown_image as 'splitter'
            split_parts = current_text.split(markdown_image, maxsplit=1)

            before_image = split_parts[0]
            
            # strip white space
            if before_image.strip():
                # append text TextNode
                result.append(TextNode(before_image, TextType.TEXT))
            # append image Text Node
            result.append(TextNode(alt, TextType.IMAGE, url=img))

            # this is grabbing the "and" or text after the text before the 
            # image if there was more text i.e. text between the images
            current_text = split_parts[1] if len(split_parts) > 1 else ""
            
            
            images = extract_markdown_images(current_text)

        if current_text.strip():
            result.append(TextNode(current_text, TextType.TEXT))

    return result





