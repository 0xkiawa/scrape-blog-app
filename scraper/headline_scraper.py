"""
Generic headline scraper.

Strategy: rather than hand-writing brittle CSS selectors per outlet (which
break every time a site redesigns), we fetch a section/homepage listing
page and pull every <a> tag whose visible text "looks like a headline"
(length, capitalization, not nav/boilerplate). This is intentionally
resilient over precise - we'd rather get a few junk rows than break
entirely when a site changes its markup.

We NEVER fetch the individual article pages or their body text here.
"""

import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

MIN_TITLE_LEN = 25
MAX_TITLE_LEN = 160
MAX_HEADLINES_PER_SITE = 15

# Boilerplate/nav link text we don't want polluting results.
JUNK_PATTERNS = re.compile(
    r"^(subscribe|sign in|log in|log out|newsletter|advertisement|"
    r"skip to|manage account|privacy|terms|cookie|follow us|share|"
    r"see all|read more|continue reading)",
    re.IGNORECASE,
)


def _looks_like_headline(text: str) -> bool:
    text = text.strip()
    if not (MIN_TITLE_LEN <= len(text) <= MAX_TITLE_LEN):
        return False
    if JUNK_PATTERNS.match(text):
        return False
    # Headlines usually have a handful of words, not a single blob of nav text.
    if len(text.split()) < 4:
        return False
    return True


def fetch_headlines(site_url: str, source_name: str) -> list[dict]:
    """
    Fetch a section/homepage page and return a de-duplicated list of
    {"title": str, "url": str, "source": str} dicts.
    """
    headlines = []
    seen_titles = set()

    try:
        resp = requests.get(
            site_url,
            timeout=12,
            headers={"User-Agent": "Mozilla/5.0 (compatible; KiawaNotesBot/1.0)"},
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️  Failed to fetch {source_name} ({site_url}): {e}")
        return headlines

    soup = BeautifulSoup(resp.text, "html.parser")

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if not _looks_like_headline(text):
            continue

        title_key = text.lower()
        if title_key in seen_titles:
            continue

        href = urljoin(site_url, a["href"])
        headlines.append({"title": text, "url": href, "source": source_name})
        seen_titles.add(title_key)

        if len(headlines) >= MAX_HEADLINES_PER_SITE:
            break

    return headlines