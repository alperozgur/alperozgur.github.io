import os
import requests
from bs4 import BeautifulSoup

# URL of Barış Terkoğlu's columns page
url = "https://www.cumhuriyet.com.tr/yazarlar/baris-terkoglu"

# Function to fetch and parse the web page
def fetch_columns(url):
    print(f"Fetching columns from {url}")
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Function to extract article links
def get_article_links(soup):
    links = []
    # Updated CSS selector for article links
    for article in soup.find_all('a', href=True):
        href = article.get('href')
        if '/yazarlar/baris-terkoglu/' in href:
            full_link = "https://www.cumhuriyet.com.tr" + href
            if full_link not in links:
                links.append(full_link)
    print(f"Found {len(links)} articles")
    return links[:15]  # Return latest 15 links

# Function to extract article content
def get_article_content(url):
    print(f"Fetching article content from {url}")
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract title
    title_tag = soup.find('h1', class_='baslik')
    if title_tag:
        title = title_tag.text.strip()
    else:
        print(f"Title not found for {url}")
        return None, None
    
    # Extract publishing date
    date_tag = soup.find('meta', {'name': 'dateModified'})
    if date_tag and 'content' in date_tag.attrs:
        publishing_date = date_tag['content']
    else:
        print(f"Publishing date not found for {url}")
        return None, None
    
    # Extract main article content
    content_div = soup.find('div', class_='haberMetni')
    if content_div:
        # Find all paragraphs and h3 tags
        paragraphs = content_div.find_all(['p', 'h3'])
        content = ""
        for tag in paragraphs:
            # Check if it's a subheader
            if tag.name == 'h3':
                # Add subheader with appropriate Markdown formatting
                content += f"\n## {tag.text.strip()}\n\n"
            else:
                # Add paragraph content
                content += f"{tag.text.strip()}\n\n"
    else:
        print(f"Content not found for {url}")
        return None, None
    
    return title, content, publishing_date

# Function to save content to markdown file
def save_article_to_md(title, content, publishing_date):
    # Format filename with publishing date
    filename = f"{publishing_date.split('T')[0]}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n{content}")
    print(f"Saved article to {filename}")

# Main function
def main():
    soup = fetch_columns(url)
    article_links = get_article_links(soup)

    for index, link in enumerate(article_links):
        title, content, publishing_date = get_article_content(link)
        if title and content and publishing_date:
            save_article_to_md(title, content, publishing_date)
            print(f"Processed {index + 1}/{len(article_links)}: {title}")
        else:
            print(f"Skipped article {index + 1}/{len(article_links)}: {link}")

if __name__ == "__main__":
    main()
