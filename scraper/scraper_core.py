"""HTML extraction helpers retained for tests and downstream compatibility."""
from __future__ import annotations

from bs4 import BeautifulSoup


def extract_title_from_html(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    meta = soup.find("meta", property="og:title") or soup.find("meta", attrs={"name": "twitter:title"})
    if meta and meta.get("content"):
        return meta["content"].strip()
    return soup.title.get_text(strip=True) if soup.title else None


def extract_author_from_html(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    meta = soup.find("meta", attrs={"name": "author"}) or soup.find("meta", property="article:author")
    return meta.get("content", "").strip() if meta and meta.get("content") else None


def extract_date_from_html(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    meta = soup.find("meta", property="article:published_time") or soup.find("meta", attrs={"name": "date"}) or soup.find("time")
    if meta and meta.get("content"):
        return meta["content"].strip()
    if meta and meta.get("datetime"):
        return meta["datetime"].strip()
    return None


def extract_article_body(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("article") or soup.body or soup
    return "\n".join(p.get_text(" ", strip=True) for p in container.find_all("p"))
