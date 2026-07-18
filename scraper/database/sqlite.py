"""SQLite persistence for articles, story snapshots and trend history."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from scraper.models import Article, Story, utc_now_iso

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (canonical_url TEXT PRIMARY KEY, title TEXT NOT NULL, source TEXT NOT NULL, published_at TEXT, payload TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS stories (id TEXT PRIMARY KEY, title TEXT NOT NULL, trend_score INTEGER NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS trend_history (story_id TEXT NOT NULL, sampled_at TEXT NOT NULL, trend_score INTEGER NOT NULL, status TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS idx_stories_score ON stories(trend_score DESC);
"""


class SQLiteStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.executescript(SCHEMA)

    def save_articles(self, articles: list[Article]) -> None:
        self.conn.executemany("INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?, ?)", [(a.canonical_url or a.url, a.title, a.source, a.published_at, json.dumps(a.to_dict(), ensure_ascii=False)) for a in articles])
        self.conn.commit()

    def save_stories(self, stories: list[Story]) -> None:
        now = utc_now_iso()
        self.conn.executemany("INSERT OR REPLACE INTO stories VALUES (?, ?, ?, ?, ?, ?)", [(s.id, s.title, s.trend_score, s.status, json.dumps(s.to_dict(), ensure_ascii=False), now) for s in stories])
        self.conn.executemany("INSERT INTO trend_history VALUES (?, ?, ?, ?)", [(s.id, now, s.trend_score, s.status) for s in stories])
        self.conn.commit()
