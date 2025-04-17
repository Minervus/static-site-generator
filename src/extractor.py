import re


def extract_markdown_images(text):
    # Create tuple for results
    result = []
    # Find instance of alt text between [ ]
    alt_text = re.findall(r"!\[(.*?)\]",text)
    
    # Find url between ( )
    urls = re.findall(r"!\[.*?\]\((.*?)\)",text)
    # add to tuple
    for i in range(len(alt_text)):
        image_tuple = (alt_text[i],urls[i])
        result.append(image_tuple)
    # return tuple
    return result

def extract_markdown_links(text):
    # Create tuple for results
    result = []
    # Find instance of alt text between [ ]
    alt_text = re.findall(r"\[(.*?)\]",text)
    
    # Find url between ( )
    urls = re.findall(r"\((.*?)\)",text)
    # add to tuple
    for i in range(len(alt_text)):
        image_tuple = (alt_text[i],urls[i])
        result.append(image_tuple)
    # return tuple
    return result