import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

DB_PATH = "./rss/articles.db"
TB_ARTICLES = "articles"
TB_AUTHORS = "authors"


# Function to convert date from Turkish to yyyy-mm-dd format
def convert_turkish_date(turkish_date):

    # Mapping of Turkish month names to month numberss
    turkish_months = {
        "Ocak": "01",
        "Şubat": "02",
        "Mart": "03",
        "Nisan": "04",
        "Mayıs": "05",
        "Haziran": "06",
        "Temmuz": "07",
        "Ağustos": "08",
        "Eylül": "09",
        "Ekim": "10",
        "Kasım": "11",
        "Aralık": "12"
    }
    # Split the date string
    day, month, year = turkish_date.split()
    
    # Get the month number from the dictionary
    month_number = turkish_months[month]
    
    # Format the date in yyyy-mm-dd
    formatted_date = f"{year}-{month_number}-{day.zfill(2)}"
    
    return formatted_date

#Function to add article to the database GENERAL
def add_article(article):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            sql = f'''INSERT INTO {TB_ARTICLES}(author, date, title, desc, link) VALUES (?, ?, ?, ?, ?)'''
            cur = conn.cursor()
            cur.execute(sql, article)
            conn.commit()
            return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    
#Function to fetch articles from the cumhuriyet website UNIQUE
def fetch_articles3(url):
    """Fetch articles from the given URL and store them in the database."""
    session = requests.Session()  # Use session for efficiency
    try:
        response = session.get(url, timeout=10)  # Set timeout
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        author = soup.find('div', class_='adi').get_text(strip=True)
        container = soup.find('ul', class_='yazilar')
        articles = container.find_all('li')
        for article in articles:
            baseurl = "https://www.cumhuriyet.com.tr"
            link_tag = article.find('a', href=True)
            link = link_tag.get("href", "#") if link_tag else "#"
            link = baseurl + link
            date_tag = article.find('span', class_='tarih')
            date = date_tag.get_text(strip=True) if date_tag else "Unknown Date"
            title = article.find("span", class_="baslik").get_text(strip=True) if link_tag else "No Title"
            date = date.split(" ")
            date = date[0] + " " + date[1] + " " + date[2]
            date = convert_turkish_date(date)
            entry = (author, date, title, "", link)
            entry_id = add_article(entry)
            if entry_id:
                print(f'Added article {author}:{entry_id}')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage: {e}")
    except Exception as e:
        print(f"Unexpected error during parsing: {e}")

for i in range(1, 7):
    fetch_articles3("https://www.cumhuriyet.com.tr/yazarlar/altan-oymen/"+str(i))