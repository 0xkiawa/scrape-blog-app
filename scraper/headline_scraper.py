"""Backward-compatible synchronous wrapper around the async source system."""
from __future__ import annotations

import asyncio

from scraper.models import Publisher
from scraper.sources.manager import fetch_all


def fetch_headlines(site_url: str, source_name: str) -> list[dict]:
    publisher = Publisher(name=source_name, url=site_url, feed_url=site_url)
    try:
        articles = asyncio.run(fetch_all([publisher], max_items_per_source=30))
    except RuntimeError:
        loop = asyncio.get_event_loop(); articles = loop.run_until_complete(fetch_all([publisher], max_items_per_source=30))
    return [a.to_dict() for a in articles]
