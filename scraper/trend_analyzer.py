"""Backward-compatible trend analyzer now returning semantic story clusters."""
from __future__ import annotations

from scraper.clustering.semantic import cluster_articles
from scraper.models import Article
from scraper.nlp.pipeline import enrich_articles
from scraper.ranking.trends import build_stories


def find_trending(headlines: list[dict], min_sources: int = 2) -> list[dict]:
    articles = [Article(title=h["title"], url=h["url"], source=h["source"], canonical_url=h.get("canonical_url"), category_hint=h.get("category_hint")) for h in headlines]
    enrich_articles(articles)
    clusters = [c for c in cluster_articles(articles, min_cluster_size=min_sources) if len({a.source for a in c}) >= min_sources or len(c) >= min_sources]
    return [story.to_dict() for story in build_stories(clusters)]
