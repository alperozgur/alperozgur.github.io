import sqlite3
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

def generate_rss(output_file,author,link):
    db_path = "articles.db"
    table_name = "articles"
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    

    # Fetch data from the specified table (assumes columns: title, link, description, pub_date)
    cursor.execute(f"SELECT title, link, desc, date FROM {table_name} WHERE author = '{author}'")
    rows = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Create an RSS feed
    fg = FeedGenerator()
    fg.title(author)
    fg.link(href=link, rel='self')
    fg.description(f"{author} tarafından yazılan tüm köşe yazıları")
    
    # Add entries to the RSS feed
    for row in rows:
        fe = fg.add_entry()
        fe.title(row[0])
        fe.link(href=row[1])
        fe.description(row[2])

        date_str = row[3]  # Extract date string (YYYY-MM-DD)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d") # Convert to datetime object
        date_obj_utc = pytz.utc.localize(date_obj) # Add UTC timezone
        fe.pubDate(date_obj_utc)        
    # Write to file
    fg.rss_file(f"{output_file}.xml")
    print(f"RSS feed generated successfully: '{output_file}'.xml")

def fetch_authors():
    try:
        with sqlite3.connect('articles.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT short,author,link FROM authors')
            rows = cur.fetchall()
            for row in rows:
                # Generate separate rss file for the authors in the database
                generate_rss(row[0], row[1],row[2])
    except sqlite3.OperationalError as e:
        print(e)


fetch_authors()