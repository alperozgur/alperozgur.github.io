import requests
from bs4 import BeautifulSoup

def fetch_authors(url):
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
            print(link[0])
            short = link[0].rpartition('/')
            print(short[2])
            author = card.find('span').get_text(strip=True)
            print(author)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage: {e}")
    except Exception as e:
        print(f"Unexpected error during parsing: {e}")

fetch_authors("https://www.nefes.com.tr/yazarlar")