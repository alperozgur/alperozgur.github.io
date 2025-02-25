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
            cursor.execute(f"SELECT title, link, desc, date FROM {TB_ARTICLES} WHERE author = ?", (author,))
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
            ET.SubElement(body, "outline", text=author, type="link", xmlUrl=domain+rss_path+parser+short+".xml")
        # Convert tree to a string and write to file
        tree = ET.ElementTree(opml)
        output_file = rss_path+"/"+parser+"/"+parser+".opml"
        with open(output_file, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)
        print(f"OPML file created: {output_file}")


    except sqlite3.Error as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    fetch_authors()
