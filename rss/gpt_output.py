import os
import xml.etree.ElementTree as ET
import sqlite3
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

DB_PATH = "./rss/articles.db"
TB_ARTICLES = "articles"
TB_AUTHORS = "authors"

domain = "https://alperozgur.github.io/" 
rss_path = "rss"


def generate_rss(output_file, author, link, parser):    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Use parameterized query to prevent SQL injection
            cursor.execute(f"SELECT title, link, desc, date FROM {TB_ARTICLES} WHERE author = ? ORDER BY date ASC", (author,))
            rows = cursor.fetchall()
        
        if not rows:
            print(f"No articles found for author: {author}")
            return

        # Create an RSS feed
        fg = FeedGenerator()
        fg.title(author)
        fg.link(href=link, rel='self')
        fg.description(f"{author} tarafından yazılan tüm köşe yazıları")

        # Add entries to the RSS feed
        for title, url, description, date_str in rows:
            fe = fg.add_entry()
            fe.title(title)
            fe.link(href=url)
            fe.description(description)
            
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                fe.pubDate(pytz.utc.localize(date_obj))  # Convert to UTC
            except ValueError:
                print(f"Invalid date format for {title}: {date_str}")

        # Write to file
        fg.rss_file(f"{rss_path}/{parser}/{output_file}.xml")
        print(f"RSS feed generated successfully: '{output_file}.xml'")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def fetch_authors():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT short, author, link, parser FROM {TB_AUTHORS}")
            authors = cur.fetchall()

        if not authors:
            print("No authors found in the database.")
            return
        # Create the OPML structure
        opml = ET.Element("opml", version="2.0")
        head = ET.SubElement(opml, "head")
        ET.SubElement(head, "title").text = "Köşe Yazarları RSS Listesi"
        body = ET.SubElement(opml, "body")

        for short, author, link, parser in authors:
            generate_rss(short, author, link, parser)
            ET.SubElement(body, "outline", text=author, type="link", xmlUrl=domain+rss_path+"/"+parser+"/"+short+".xml")
        # Convert tree to a string and write to file
        tree = ET.ElementTree(opml)
        output_file = rss_path+"/index.opml"
        with open(output_file, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)
        print(f"OPML file created: {output_file}")


    except sqlite3.Error as e:
        print(f"Database error: {e}")

# OPML to HTML
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
            html += " " * indent + f"<li class='list-group-item bg-white shadow-sm p-2 opml-item'><a href='{xml_url}' class='text-decoration-none text-primary'>{text}</a></li>\n"
        else:
            html += " " * indent + f"<li class='list-group-item bg-white shadow-sm p-2 opml-item'>{text}</li>\n"
        
        children = outline.findall("outline")
        if children:
            html += " " * indent + "<ul class='list-group ms-3'>\n"
            html += opml_to_html(children, indent + 2)
            html += " " * indent + "</ul>\n"
    return html

def generate_html(opml_path, output_path):
    body = parse_opml(opml_path)
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OPML Viewer</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f0f8ff; color: #002147; }
            .navbar { background-color: #002147; }
            .navbar-brand, .nav-link { color: #ffffff !important; }
            .container { margin-top: 30px; }
            .opml-container { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
            .footer { background-color: #002147; color: white; text-align: center; padding: 20px 0; margin-top: 30px; }
            .btn-custom { background-color: #002147; color: white; }
            .btn-custom:hover { background-color: #003366; color: white; }
            .opml-item:hover { background-color: #dfefff; transition: background-color 0.3s ease-in-out; }
        </style>
        <script>
            function searchOPML() {
                let input = document.getElementById('searchInput').value.toLowerCase();
                let items = document.getElementsByClassName('opml-item');
                for (let item of items) {
                    let text = item.textContent.toLowerCase();
                    if (text.includes(input)) {
                        item.style.display = '';
                    } else {
                        item.style.display = 'none';
                    }
                }
            }
        </script>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
                <a class="navbar-brand" href="#">OPML Viewer</a>
            </div>
        </nav>
        <div class="container">
            <div class="opml-container">
                <div class="mb-3">
                    <input type="text" id="searchInput" class="form-control" placeholder="Search..." onkeyup="searchOPML()">
                </div>
                <ul class="list-group">
    """ + opml_to_html(body.findall("outline")) + "</ul>\n</div>\n</div>\n<footer class='footer'><p>&copy; 2025 OPML Viewer. All rights reserved.</p></footer>\n</body>\n</html>"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"HTML file generated: {output_path}")

# Main function    
if __name__ == "__main__":
    fetch_authors()
    generate_html("rss/index.opml", "rss/index.html")
