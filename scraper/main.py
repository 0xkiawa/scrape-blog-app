"""Run the News Intelligence Platform headline collection and story clustering."""
from __future__ import annotations

import asyncio
import logging

from scraper.clustering.semantic import cluster_articles
from scraper.configuration import load_publishers, load_taxonomy
from scraper.database.sqlite import SQLiteStore
from scraper.nlp.pipeline import enrich_articles
from scraper.ranking.trends import build_stories
from scraper.sources.manager import fetch_all
from scraper.storage import save_headlines, save_trending

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


async def run_async() -> list[dict]:
    publishers = load_publishers()
    print(f"📡 Fetching headlines from {len(publishers)} configured publishers...\n")
    articles = await fetch_all(publishers)
    if not articles:
        print("\n⚠️  No headlines fetched. Check network access or feed availability.")
        return []
    enrich_articles(articles)
    save_headlines(articles)
    taxonomy = load_taxonomy()
    clusters = cluster_articles(articles, similarity_threshold=taxonomy["thresholds"]["cluster_similarity"], min_cluster_size=taxonomy["thresholds"]["min_cluster_size"])
    stories = build_stories(clusters)
    save_trending(stories)
    store = SQLiteStore("data/news_intelligence.sqlite3")
    store.save_articles(articles); store.save_stories(stories)
    print(f"\nFound {len(stories)} story cluster(s):\n")
    for story in stories[:15]:
        print(f"🔥 {story.title} — score {story.trend_score} ({story.status}), {story.coverage_count} articles")
    return [s.to_dict() for s in stories]


def run() -> list[dict]:
    return asyncio.run(run_async())


if __name__ == "__main__":
    run()
