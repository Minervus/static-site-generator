from textnode import *
from split_nodes import *
from htmlnode import *
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Create list of delimiter to type ** is BOLD, * is italic etc.
    result = []

    for node in old_nodes:
        # 1. Identify delimiter indexes
        first_delimiter = node.text.find(delimiter)
        if first_delimiter == -1:
            result.append(node)
            continue
    #     last_delimiter = node.text.rfind(delimiter)
    #     # 4. Grab value from " up to delimiter
    #     first_node_text = node.text[0:first_delimiter]
    #     result.append(TextNode(first_node_text,TextType.TEXT))
    #     # 2. Grab value between delimiter indexes
    #     delimiter_text = node.text[(first_delimiter+len(delimiter)):last_delimiter]
    #     # 3. Create TextNode with (value, text-type)
    #     result.append(TextNode(delimiter_text,text_type))
        
    #     # 5. Put that value into 
    #     second_node_text = node.text[(last_delimiter+len(delimiter))::]
    #     result.append(TextNode(second_node_text,TextType.TEXT))
        text = node.text
        current_text = ""
        i = 0
        while i < len(text):
            # Look ahead for delimiter
            if text[i:i+len(delimiter)] == delimiter:
                # any unmatched text before delimiter will be plain text node
                if current_text:
                    result.append(TextNode(current_text, TextType.TEXT))
                    current_text = ""

                # Find next matching delimiter
                end_index = text.find(delimiter, i + len(delimiter))
                if end_index != -1:
                    # Extract text between delimiters and create a node
                    delimited_content = text[i + len(delimiter):end_index]
                    result.append(TextNode(delimited_content, text_type))

                    i = end_index + len(delimiter)
                else:
                    current_text += text[i]
                    i += len(delimiter)
            else:
                current_text += text[i]
                i += 1
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))
    
    return result

def text_to_textnodes(text):
    

    node = TextNode(text, TextType.TEXT)

    nodes = [node]

    first_list = split_nodes_image(nodes)
    second_list = split_nodes_link(first_list)
    third_list = split_nodes_delimiter(second_list,"**",TextType.BOLD)
    ##fourth_list = split_nodes_delimiter(third_list,"*", TextType.ITALIC)
    fourth_list = split_nodes_delimiter(third_list,"_",TextType.ITALIC)
    fifth_list = split_nodes_delimiter(fourth_list,"`",TextType.CODE)

    return fifth_list

def markdown_to_blocks(markdown):
    result = []
    blocked = markdown.split('\n\n')

    for block in blocked:
        new = block.strip()
        if new != '':
            result.append(new)

    return result

def block_to_block_type(text):

    if text.startswith("#"):
        heading_number = text.count("#")
        match heading_number:
            case 1:
                return "heading 1"
            case 2:
                return "heading 2"
            case 3:
                return "heading 3"
            case 4:
                return "heading 4"
            case 5:
                return "heading 5"
            case 6:
                return "heading 6"
    elif text.startswith("```"):
        return "code"
    elif text.startswith(">"):
        return "quote"
    elif text.startswith("*") or text.startswith("-"):
        return "unordered_list"
    elif text[:1].isdigit():
        return "ordered_list"
    else:
        return "paragraph"



def markdown_to_html_node(markdown):
    div_node = HTMLNode(tag="div",value=None,children=[],props=None)
    # Convert markdown into blocks - create a list
    blocked = markdown_to_blocks(markdown)
    # print(f'Blocked list before cleaning: {blocked}')

    # loop through blocks of markdown
    for block in blocked:
        # find the type of block it is e.g. paragraph, heading etc.
        block_type = block_to_block_type(block)
        
        # block_node = HTMLNode(tag=get_html_tag(block_type),value=None,props=None)
        
        # Special case for code
        if block_type == "code":
            # Remove ``` from the beginning and end 
            block = block.lstrip('```').rstrip('```').strip()

            # Create the pre node
            pre_node = HTMLNode(tag="pre",value=None,children=[],props=None)
            
            # Create the code node
            code_node = HTMLNode(tag="code", value=None,children=[],props=None)

            # Convert the code contents to text nodes
            text_nodes = text_to_textnodes(block)

            # convert each text node into HTML nodes and add to code node
            
            for node in text_nodes:
                html_node = text_node_to_html_node(node)
                code_node.children.append(html_node)
            
            #add code node to pre node
            pre_node.children.append(code_node)

            # add pre node to the main div
            div_node.children.append(pre_node)
        
        elif block_type == 'ordered_list' or block_type == 'unordered_list':
            tag = "ol" if block_type == "ordered_list" else "ul"
            cleaned_block = clean_block(block, block_type)
            list_node = HTMLNode(tag=tag, value=None, children=[], props=None)
            list_split = cleaned_block.split('\n')
        
            list_children = []
            for item in list_split:
                # if item.strip():
                #     # Extract item text and process code tags specifically
                #     item_text = item.strip()
                #     if block_type == "ordered_list":
                #         # Remove the number prefix (e.g., "1. ")
                #         item_text = re.sub(r'^\d+\.\s*', '', item_text)
                #     else:
                #         # Remove bullet prefix (e.g., "* " or "- ")
                #         item_text = re.sub(r'^[\*\-]\s*', '', item_text)
                        
                #     # Process code tags first, separately
                #     item_text = re.sub(r'`([^`]+)`', r'<code>\1</code>', item_text)
                    
                #     # Then apply other markdown styles
                #     item_text = parse_markdown_styles(item_text)
                    
                #     # Create list item node with the processed text
                #     child = HTMLNode(tag="li", value=item_text, children=[], props=None)
                #     list_children.append(child)
                # if item.strip():
                # Extract item text and process
                item_text = item.strip()
                if block_type == "ordered_list":
                    # Remove the number prefix (e.g., "1. ")
                    item_text = re.sub(r'^\d+\.\s*', '', item_text)
                else:
                    # Remove bullet prefix (e.g., "* " or "- ")
                    item_text = re.sub(r'^[\*\-]\s*', '', item_text)
                    
                # Create list item node
                item_value = parse_markdown_styles(item_text)
                text_node = HTMLNode(tag=None, value=item_value, children=None, props=None)
                item_node = HTMLNode(tag="li", value=None, children=[text_node], props=None)
                
                # Convert the item text to text nodes, then to HTML nodes
                # Use your text parsing function here
                # text_nodes = parse_markdown_styles(item_text)  
                # html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                
                # # Add HTML nodes as children to the list item
                # item_node.children.extend(html_nodes)
                
                # Add the list item to the list
                list_children.append(item_node)
          
                    
            list_node.children = list_children
            div_node.children.append(list_node)
 

        else:
            cleaned_block = clean_block(block,block_type)
            
            block_node = HTMLNode(tag=get_html_tag(block_type),value=None,children=[],props=None)
            # print(f"Created {block_node.tag} node")
            children = text_to_children(cleaned_block)
            # print(f"Children count: {len(children)}")
            # add the list to the list
            # print(f"Children: {children}")
            block_node.children.extend(children)
            div_node.children.append(block_node)
            # print(f"Added {block_node.tag} to div_node")
            
    apply_styles_to_node(div_node)

    return div_node

def process_code_tags(text):
    #"""Process code tags in text and return HTML with proper <code> tags."""
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

def parse_markdown_styles(text):
    # Replace **bold** with <b> tags
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    # Replace _italic_ with <i> tags
    text = re.sub(r"_(.*?)_", r"<i>\1</i>", text)
    # Replace inline code with <code>
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Parse for links - don't use an if statement, use regex substitution like the others
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    
    return text

def clean_block(block, block_type):
    if block_type.startswith('heading'):
        return block.strip('#')
    elif block_type == 'quote':
        lines = block.split("\n")
        cleaned_lines = [line.lstrip("> ").strip() for line in lines]
        block = "\n".join(cleaned_lines)
        return block
    elif block_type == 'unordered_list':
        lines = block.split("\n")
        cleaned_lines = []
        for line in lines:
            # Remove any combination of leading spaces, followed by a list marker (-, *, +), followed by spaces
            cleaned_line = re.sub(r'^\s*[-*+]\s+', '', line)
            cleaned_lines.append(cleaned_line)
        block = "\n".join(cleaned_lines)
        return block
    elif block_type == 'ordered_list':
        lines = block.split("\n")
        # Remove the number and period at the start of each line
        cleaned_lines = []
        for line in lines:
            # Use regex to match a number followed by a period and space at the beginning of the line
            cleaned_line = re.sub(r'^\s*\d+\.\s+', '', line)
            cleaned_lines.append(cleaned_line)
        block = "\n".join(cleaned_lines)
        return block
    else:
        # print(f'cleaned block: {block}')
        return block




def text_to_children(text):
    # print(f"RUNNING TEXT TO CHILDREN")
    if text is None:
        print("Warning: Received None text in text_to_children")
        return []
    text = " ".join(text.split())
    # text = parse_markdown_styles(text)
    text_nodes = text_to_textnodes(text)
    nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        nodes.append(html_node)
    return nodes

def get_html_tag(block_type):
    match block_type:
        case "heading 1":
            return "h1"
        case "heading 2":
            return "h2"
        case "heading 3":
            return "h3"
        case "heading 4":
            return "h4"
        case "heading 5":
            return "h5"
        case "heading 6":
            return "h6"
        case "paragraph":
            return "p"
        case "code":
            return "code"
        case "quote":
            return "blockquote"
        case "ordered_list":
            return "ol"
        case "unordered_list":
            return "ul"


def apply_styles_to_node(node):
    if isinstance(node, LeafNode) and node.value:
        node.value = parse_markdown_styles(node.value)
    elif hasattr(node, 'children') and node.children:
        for child in node.children:
            apply_styles_to_node(child)
    return node