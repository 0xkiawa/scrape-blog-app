"""Concurrent source orchestration and deduplication."""
from __future__ import annotations

import asyncio

try:
    import aiohttp
except ModuleNotFoundError:  # pragma: no cover
    aiohttp = None

from scraper.models import Article, Publisher
from scraper.sources.rss import RSSSourceAdapter
from scraper.utils.text import title_key


async def fetch_all(publishers: list[Publisher], max_items_per_source: int = 30) -> list[Article]:
    if aiohttp is not None:
        connector = aiohttp.TCPConnector(limit_per_host=4, limit=40)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [RSSSourceAdapter(p, session, max_items=max_items_per_source).fetch() for p in publishers]
            batches = await asyncio.gather(*tasks, return_exceptions=True)
    else:
        semaphore = asyncio.Semaphore(20)
        async def guarded(p: Publisher):
            async with semaphore:
                return await RSSSourceAdapter(p, None, max_items=max_items_per_source).fetch()
        batches = await asyncio.gather(*(guarded(p) for p in publishers), return_exceptions=True)
    articles = [a for batch in batches if isinstance(batch, list) for a in batch]
    return deduplicate_articles(articles)


def deduplicate_articles(articles: list[Article]) -> list[Article]:
    seen_urls: set[str] = set(); seen_titles: set[str] = set(); unique: list[Article] = []
    for article in articles:
        url_key = article.canonical_url or article.url; t_key = title_key(article.title)
        if not t_key or url_key in seen_urls or t_key in seen_titles:
            continue
        seen_urls.add(url_key); seen_titles.add(t_key); unique.append(article)
    return unique
