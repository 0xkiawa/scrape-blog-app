"""Trend scoring and story generation."""
from __future__ import annotations

from collections import Counter

from scraper.configuration import load_publishers, load_taxonomy
from scraper.models import Article, Story
from scraper.nlp.pipeline import classify_categories
from scraper.utils.text import stable_id


def build_stories(clusters: list[list[Article]]) -> list[Story]:
    authority = {p.name: p.authority for p in load_publishers()}
    stories = [_build_story(c, authority) for c in clusters if c]
    return sorted(stories, key=lambda s: s.trend_score, reverse=True)


def _build_story(articles: list[Article], authority: dict[str, float]) -> Story:
    entities = Counter(e for a in articles for e in a.entities)
    keywords = Counter(k for a in articles for k in a.keywords)
    sources = sorted({a.source for a in articles})
    score = _score(articles, sources, authority, entities)
    title = _story_title(articles, entities, keywords)
    categories = classify_categories(articles)
    source_rows = [{"title": a.title, "url": a.url, "source": a.source, "published_at": a.published_at} for a in articles]
    return Story(
        id=stable_id(title, *sources),
        title=title,
        summary=f"{len(sources)} publisher(s) are covering this story from {len(articles)} headline angle(s).",
        trend_score=score,
        status=_status(score),
        category=categories,
        entities=[e for e, _ in entities.most_common(12)],
        sources=source_rows,
        related_keywords=[k for k, _ in keywords.most_common(12)],
        coverage_count=len(articles),
        article_angles=[a.title for a in articles[:8]],
        timeline={"state":"Emerging","sparkline":[score],"samples":1},
        assistance=_assistance(title, categories, [k for k, _ in keywords.most_common(8)], [e for e, _ in entities.most_common(8)]),
    )


def _score(articles: list[Article], sources: list[str], authority: dict[str, float], entities: Counter[str]) -> int:
    weights = load_taxonomy()["weights"]
    publisher_component = min(1.0, len(sources) / 8)
    authority_component = sum(authority.get(s, 0.6) for s in sources) / max(1, len(sources))
    similarity_component = min(1.0, len(articles) / 6)
    entity_component = min(1.0, len(entities) / 6)
    raw = (publisher_component * weights["publisher_count"] + authority_component * weights["authority"] + similarity_component * weights["similarity"] + 0.75 * weights["freshness"] + 0.4 * weights["velocity"] + entity_component * weights["entity_importance"] + min(1.0, len({a.category_hint for a in articles if a.category_hint}) / 3) * weights["cross_category"])
    return max(0, min(100, round(raw * 100)))


def _status(score: int) -> str:
    if score >= 85: return "Hot"
    if score >= 70: return "Growing"
    if score >= 45: return "Emerging"
    if score >= 25: return "Cooling"
    return "Archived"


def _story_title(articles: list[Article], entities: Counter[str], keywords: Counter[str]) -> str:
    if entities:
        lead = entities.most_common(1)[0][0]
        tail = " ".join(k for k, _ in keywords.most_common(3))
        return f"{lead} coverage builds around {tail}".strip()
    return articles[0].title


def _assistance(title: str, categories: list[str], keywords: list[str], entities: list[str]) -> dict:
    return {"possible_headlines":[title, f"What to know about {title}", f"Why {title} matters now"], "seo_title": title[:60], "meta_description": f"A concise briefing on {title}, including context, key players and next developments.", "suggested_outline":["What happened", "Why it matters", "Key people and organizations", "What happens next"], "reader_questions":["What changed?", "Who is affected?", "What should we watch next?"], "related_keywords": keywords, "possible_interview_subjects": entities[:5], "suggested_follow_up_stories":[f"Local impact of {title}", f"Timeline behind {title}"]}
