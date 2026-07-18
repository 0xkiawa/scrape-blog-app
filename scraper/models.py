"""Typed data models for the News Intelligence Platform."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class Publisher:
    name: str
    url: str
    feed_url: str | None = None
    category: str = "World"
    country: str | None = None
    authority: float = 0.7
    adapter: str = "rss"
    enabled: bool = True
    rate_limit_seconds: float = 0.2


@dataclass(slots=True)
class Article:
    title: str
    url: str
    source: str
    published_at: str | None = None
    summary: str | None = None
    category_hint: str | None = None
    country: str | None = None
    canonical_url: str | None = None
    entities: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Story:
    id: str
    title: str
    summary: str
    trend_score: int
    status: str
    category: list[str]
    entities: list[str]
    sources: list[dict[str, Any]]
    related_keywords: list[str]
    coverage_count: int
    article_angles: list[str]
    timeline: dict[str, Any]
    assistance: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
