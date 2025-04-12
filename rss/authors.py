import requests
from bs4 import BeautifulSoup
import sqlite3

DB_PATH = "./rss/articles.db"
TB_AUTHORS = "authors"

#Function to add author to the database GENERAL
def add_author(author):
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
    
#Function to parse authors from the website Not general
def parse_nefes(url,parser):
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

#Function to parse authors from the website Not general
def parse_ekonomim(url, parser):
    session = requests.Session()  # Use session for efficiency
    try:
        response = session.get(url, timeout=10)  # Set timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        cards = soup.find_all('div', class_='col-12 col-md-4 col-lg-3 d-xl-flex d-lg-flex')
        for card in cards:
            link_tag = card.find('a', href=True)
            url = link_tag.get("href", "#") if link_tag else "#"
            link = url.rpartition('/')
            short = link[0].rpartition('/')
            author = card.find('span', class_='name').get_text(strip=True)
            img = card.find('img').get('src')
            entry = (author,short[2],url,parser,img)
            entry_id = add_author(entry)
            if entry_id:
                print(f'Added author {author}')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage: {e}")
    except Exception as e:
        print(f"Unexpected error during parsing: {e}")
if __name__ == "__main__":
    parse_nefes("https://www.nefes.com.tr/yazarlar","nefes")
    parse_ekonomim("https://www.ekonomim.com/yazarlar","ekonomim")