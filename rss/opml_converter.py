import xml.etree.ElementTree as ET

rss_path = "rss"

def parse_opml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    if root.tag.lower() != "opml":
        raise ValueError("Not a valid OPML file")
    
    body = root.find("body")
    if body is None:
        raise ValueError("Invalid OPML structure, missing body")
    
    return body

def opml_to_html(outlines, indent=0):
    html = ""
    for outline in outlines:
        text = outline.get("text", "[No Text]")
        xml_url = outline.get("xmlUrl")
        
        if xml_url:
            html += " " * indent + f"<li class='list-group-item'><a href='{xml_url}' class='text-decoration-none'>{text}</a></li>\n"
        else:
            html += " " * indent + f"<li class='list-group-item'>{text}</li>\n"
        
        children = outline.findall("outline")
        if children:
            html += " " * indent + "<ul class='list-group'>\n"
            html += opml_to_html(children, indent + 2)
            html += " " * indent + "</ul>\n"
    return html

def generate_html(opml_path, output_path):
    body = parse_opml(opml_path)
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>OPML Viewer</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="container mt-4">
        <h1 class="mb-4">OPML Viewer</h1>
        <ul class="list-group">
    """ + opml_to_html(body.findall("outline")) + "</ul>\n</body>\n</html>"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"HTML file generated: {output_path}")
# Example usage:
generate_html(rss_path+"/index.opml", rss_path+"/index.html")
