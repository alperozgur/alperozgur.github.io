import os
import xml.etree.ElementTree as ET
import sqlite3
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

DB_PATH = "./rss/articles.db"
TB_ARTICLES = "articles"
TB_AUTHORS = "authors"
rss_path = "rss/xml"
domain = "https://alperozgur.github.io/rss/xml/"  # Change to your domain

def fetch_authors():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT short,author FROM {TB_AUTHORS}")
            authors = cur.fetchall()

        if not authors:
            print("No authors found in the database.")
            return
            # Create the OPML structure
        opml = ET.Element("opml", version="2.0")
        head = ET.SubElement(opml, "head")
        ET.SubElement(head, "title").text = "Köşe Yazarları RSS Listesi"
        body = ET.SubElement(opml, "body")
        
        for short, author in authors:
            ET.SubElement(body, "outline", text=author, type="link", url=domain+short+".xml")
        # Convert tree to a string and write to file
        tree = ET.ElementTree(opml)
        with open(output_file, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)
        
        print(f"OPML file created: {output_file}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


# Example usage
directory = "rss/xml"  # Change to your XML folder
output_file = "rss/xml/authors.opml"
fetch_authors()

