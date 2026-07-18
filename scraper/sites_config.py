"""Backward-compatible access to publisher and stopword configuration."""
from __future__ import annotations

from scraper.configuration import load_publishers, load_taxonomy

SITES = [{"name": p.name, "url": p.feed_url or p.url} for p in load_publishers()]
STOPWORDS = set(load_taxonomy()["stopwords"])
