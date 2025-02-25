import os
import xml.etree.ElementTree as ET

def create_opml(directory, output_file):
    # Create the OPML structure
    opml = ET.Element("opml", version="2.0")
    head = ET.SubElement(opml, "head")
    ET.SubElement(head, "title").text = "Köşe Yazarları RSS Listesi"
    body = ET.SubElement(opml, "body")
    
    # Iterate through XML files in the given directory
    for file in os.listdir(directory):
        if file.endswith(".xml"):
            file_path = os.path.join(directory, file)
            ET.SubElement(body, "outline", text=file, type="link", url=file_path)
    
    # Convert tree to a string and write to file
    tree = ET.ElementTree(opml)
    with open(output_file, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
    
    print(f"OPML file created: {output_file}")

# Example usage
directory = "rss/xml"  # Change to your XML folder
output_file = "rss/xml/authors.opml"
create_opml(directory, output_file)
