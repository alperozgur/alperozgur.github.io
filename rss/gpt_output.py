import sqlite3
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

DB_PATH = "articles.db"

def generate_rss(output_file, author, link):
    table_name = "articles"
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Use parameterized query to prevent SQL injection
            cursor.execute(f"SELECT title, link, desc, date FROM {table_name} WHERE author = ?", (author,))
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
        fg.rss_file(f"{output_file}.xml")
        print(f"RSS feed generated successfully: '{output_file}.xml'")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def fetch_authors():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT short, author, link FROM authors")
            authors = cur.fetchall()

        if not authors:
            print("No authors found in the database.")
            return
        
        for short, author, link in authors:
            generate_rss(short, author, link)

    except sqlite3.Error as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    fetch_authors()
