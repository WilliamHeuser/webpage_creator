import json

# Function that takes a replacing dict, a string to replace in and returns the replaces string
def change_string(replacement_dict, content):       
    for key, value in replacement_dict.items():
        content = content.replace(key, value)

    # Printing Text replaced
    print("Text replaced")
    
    return content

def build_navbar_content(block_list):
    content = ""
    for el in block_list:
        header = el['content']['%header%']
        content += f"        <a href=\"#{header}\">{header}</a>" + "\n"
    return content

def build_SoMe_content(SoMe_list):
    content = ""
    for el in SoMe_list:
        content += f"            <a href=\"%{el}_link%\">%{el}_tag%</a>" + "\n"
    return content

def parse_SoMe_content(content):
    SoMe_list = []
    for keys, values in content.items():
        if keys.endswith('_link%') and values != "":
            sm = keys[keys.index("%") + 1: keys.index("_link%")]
            SoMe_list.append(sm)
    return SoMe_list

def build_html(block_list):
    is_primary = True
    html = ''

    # Start the document
    with open ('building_blocks\\html\\' + "document_start" + r'.txt') as b:
        html += b.read() + "\n"

    # Add the navbar and the start of body tag
    with open ('building_blocks\\html\\' + "navbar" + r'.txt') as b:
        navbar_dict = {"%content%": build_navbar_content(block_list)}
        html += html + change_string(navbar_dict, b.read()) + "\n"   
    

    # Add every block and replaces it with the content
    for block in block_list:
        if block["type"] == "start_section":
            SoMe_list = parse_SoMe_content(block["content"])
            SoMe_dict = {"%content%": build_SoMe_content(SoMe_list)}
            with open ('building_blocks\\html\\' + block['type'] + r'.txt') as b:
                SoMe_content = change_string(SoMe_dict, b.read())
                html += change_string(block['content'], SoMe_content) + "\n"
        elif block['type'] == "text_image" or block['type'] == "image_text":
            with open ('building_blocks\\html\\' + block['type'] + r'.txt') as b:
                block_content = b.read()

                # give the block the proper class, switching between primary and secondary (for styling)
                if is_primary:
                    block_content = block_content.format(class_type = "primary")
                    is_primary = not is_primary
                else:
                    block_content = block_content.format(class_type = "secondary")
                    is_primary = not is_primary
                block_html = change_string(block['content'], block_content)
                html += block_html + "\n"
        else:
            with open ('building_blocks\\html\\' + block['type'] + r'.txt') as b:
                block_html = change_string(block['content'], b.read())
                html += block_html + "\n"
    
    # End the document
    with open ('building_blocks\\html\\' + "document_end" + r'.txt') as b:
        html += b.read() + "\n"
    return html

def main():
    print("Starting creation")

    # Load user content
    with open("content.json") as json_file:
        block_dict = json.load(json_file)
    

    # Build the html     
    site_html = build_html(list(block_dict.values()))

    # Load html parameters
    with open("params_html.json") as json_file:
        html_params = json.load(json_file)
    
    # Insert the params into html file
    site_html = change_string(html_params, site_html)

    # Write html to given location
    with open("results\\index.html", "w") as file:
        file.write(site_html)


    # read in css parameters   
    with open("params_css.json") as json_file:
        css_params = json.load(json_file)
    
    # Open css template and replace keywords with parameters
    with open("style.css", 'r') as file:
        site_css = file.read()
        site_css = change_string(css_params, site_css)
    
    # Write to given location
    with open("results\\style.css", 'w') as file:
       file.write(site_css)
    

if __name__ == "__main__":
    main()