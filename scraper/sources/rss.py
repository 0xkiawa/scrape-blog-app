"""Async RSS/Atom source adapter with aiohttp and stdlib fallbacks."""
from __future__ import annotations

import asyncio
import email.utils
import logging
from datetime import timezone
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

try:
    import aiohttp
except ModuleNotFoundError:  # pragma: no cover - environment fallback
    aiohttp = None
try:
    import feedparser
except ModuleNotFoundError:  # pragma: no cover - environment fallback
    feedparser = None

from scraper.models import Article, Publisher
from scraper.sources.base import BaseSourceAdapter
from scraper.utils.text import canonicalize_url, normalize_title

LOG = logging.getLogger(__name__)
USER_AGENT = "NewsIntelligencePlatform/1.0 (+headline-only; open-source)"


class RSSSourceAdapter(BaseSourceAdapter):
    def __init__(self, publisher: Publisher, session=None, max_items: int = 30, retries: int = 2) -> None:
        super().__init__(publisher, max_items)
        self.session = session
        self.retries = retries

    async def fetch(self) -> list[Article]:
        url = self.publisher.feed_url or self.publisher.url
        for attempt in range(self.retries + 1):
            try:
                text = await self._download(url)
                return self._parse(text)
            except Exception as exc:
                if attempt >= self.retries:
                    LOG.warning("Failed to fetch %s: %s", self.publisher.name, exc)
                    return []
                await asyncio.sleep(0.5 * (attempt + 1))
        return []

    async def _download(self, url: str) -> str:
        if aiohttp is not None and self.session is not None:
            async with self.session.get(url, headers={"User-Agent": USER_AGENT}, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                resp.raise_for_status()
                return await resp.text()
        return await asyncio.to_thread(_download_stdlib, url)

    def _parse(self, feed_text: str) -> list[Article]:
        if feedparser is not None:
            parsed = feedparser.parse(feed_text)
            entries = [(getattr(e, "title", ""), getattr(e, "link", ""), getattr(e, "published", None) or getattr(e, "updated", None), getattr(e, "summary", None)) for e in parsed.entries[: self.max_items]]
        else:
            entries = _parse_xml_entries(feed_text, self.max_items)
        articles: list[Article] = []
        for title_raw, link, published, summary in entries:
            title = normalize_title(title_raw)
            if len(title.split()) < 4 or not link:
                continue
            articles.append(Article(title=title, url=link, canonical_url=canonicalize_url(link), source=self.publisher.name, published_at=_parse_date(published), summary=summary, category_hint=self.publisher.category, country=self.publisher.country))
        return articles


def _download_stdlib(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _parse_xml_entries(feed_text: str, limit: int) -> list[tuple[str, str, str | None, str | None]]:
    root = ET.fromstring(feed_text)
    rows = []
    for item in root.findall(".//item")[:limit]:
        rows.append((_text(item, "title"), _text(item, "link"), _text(item, "pubDate"), _text(item, "description")))
    if rows:
        return rows
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall(".//atom:entry", ns)[:limit]:
        link_el = entry.find("atom:link", ns)
        rows.append((_text(entry, "atom:title", ns), link_el.get("href", "") if link_el is not None else "", _text(entry, "atom:updated", ns), _text(entry, "atom:summary", ns)))
    return rows


def _text(node: ET.Element, path: str, ns: dict[str, str] | None = None) -> str | None:
    child = node.find(path, ns or {})
    return child.text.strip() if child is not None and child.text else None


def _parse_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return email.utils.parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except Exception:
        return value
