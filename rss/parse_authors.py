import requests
from bs4 import BeautifulSoup
import sqlite3

DB_PATH = "./rss/articles.db"
TB_ARTICLES = "articles"
TB_AUTHORS = "authors"

def add_author(author):
    """Insert author details into the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            sql = f'''INSERT INTO {TB_AUTHORS}(author, short, link, parser, img) VALUES (?, ?, ?, ?, ?)'''
            cur = conn.cursor()
            cur.execute(sql, author)
            conn.commit()
            return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    

def fetch_authors(url,parser):
    """Fetch articles from the given URL and store them in the database."""
    session = requests.Session()  # Use session for efficiency
    try:
        response = session.get(url, timeout=10)  # Set timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        cards = soup.find_all('article', class_='card-author')
        for card in cards:
            link_tag = card.find('a', href=True)
            link = link_tag.get("href", "#") if link_tag else "#"
            link = link.rpartition('/')
            short = link[0].rpartition('/')
            author = card.find('span').get_text(strip=True)
            img = card.find('img').get('src')
            entry = (author,short[2],link[0],parser,img)
            entry_id = add_author(entry)
            if entry_id:
                print(f'Added author {author}')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage: {e}")
    except Exception as e:
        print(f"Unexpected error during parsing: {e}")

fetch_authors("https://www.nefes.com.tr/yazarlar","nefes")