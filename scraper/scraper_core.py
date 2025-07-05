import requests
from bs4 import BeautifulSoup
import json

def fetch_article_html(url: str) -> str:
    # NASA-safe HTTP fetch
    assert isinstance(url, str), "URL must be a string."
    assert url.startswith("http"), "URL must start with http or https."

    response = requests.get(url, timeout=10)
    assert response.status_code == 200, f"Failed to fetch URL: {url}"

    return response.text

def extract_title_from_html(html: str) -> str:
    # NASA-safe HTML title extraction
    assert isinstance(html, str), "HTML must be a string."
    assert len(html) > 0, "HTML must not be empty."

    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('h1') or soup.find('title')
    assert title_tag is not None, "Title tag not found in HTML."

    return title_tag.get_text(strip=True)

def extract_author_from_html(html: str) -> str:
    assert isinstance(html, str), "HTML must be a string."  # Assertion 1
    assert len(html) > 0, "HTML must not be empty."         # Assertion 2

    soup = BeautifulSoup(html, 'html.parser')

    author = None

    # Try a few likely patterns
    author_tag = soup.find(attrs={"class": "author"}) or \
                 soup.find("meta", attrs={"name": "author"}) or \
                 soup.find("a", rel="author")

    if author_tag:
        if author_tag.name == "meta":
            author = author_tag.get("content", None)
        else:
            author = author_tag.get_text(strip=True)

    if not author:
        author = "Unknown"

    assert isinstance(author, str), "Author must be returned as a string."  # Assertion 3

    return author

def extract_date_from_html(html: str) -> str:
    assert isinstance(html, str), "HTML must be a string."
    assert len(html) > 0, "HTML must not be empty."

    soup = BeautifulSoup(html, 'html.parser')
    date = None

    # First attempt: <time datetime="...">
    time_tag = soup.find("time")

    # Fallback: <meta property="article:published_time">
    meta_tag = soup.find("meta", attrs={"property": "article:published_time"}) or \
               soup.find("meta", attrs={"name": "date"})

    # Fallback: <span class="date">...</span>
    date_class = soup.find(attrs={"class": "date"})

    if time_tag and time_tag.has_attr("datetime"):
        date = time_tag["datetime"]
    elif meta_tag and meta_tag.has_attr("content"):
        date = meta_tag["content"]
    elif date_class:
        date = date_class.get_text(strip=True)

    if not date:
        date = "Unknown"

    assert isinstance(date, str), "Date must be returned as a string."

    return date


def extract_article_body(html: str) -> str:
    assert isinstance(html, str), "HTML must be a string."   # Assertion 1
    assert len(html) > 0, "HTML must not be empty."          # Assertion 2

    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('article')

    if not article:
        # Try common content divs
        article = soup.find('div', class_='article-content') or \
                  soup.find('div', class_='post-content') or \
                  soup.find('div', class_='entry-content') or \
                  soup.find('div', class_='main-content')

    if article:
        paragraphs = article.find_all('p')
        body = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    else:
        body = "Content not found"

    assert isinstance(body, str), "Article body must be a string."   # Assertion 3

    return body
