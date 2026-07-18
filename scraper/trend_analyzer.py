"""
Trend detector.

Takes the day's headlines from all 6 sources and finds words/phrases that
show up across MULTIPLE distinct outlets - that cross-source repetition is
the actual trending-topic signal (one outlet obsessing over something is
just that outlet; three outlets independently covering it is a trend).
"""

import re
from collections import defaultdict

from sites_config import STOPWORDS

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]+")


def _clean_words(title: str) -> list[str]:
    words = WORD_RE.findall(title)
    return [w for w in words if w.lower() not in STOPWORDS and len(w) > 2]


def _bigrams(words: list[str]) -> list[str]:
    return [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]


def find_trending(headlines: list[dict], min_sources: int = 2) -> list[dict]:
    """
    headlines: list of {"title", "url", "source"}
    Returns a ranked list of:
      {"phrase": str, "num_sources": int, "sources": [...], "examples": [...]}
    sorted by number of distinct sources (desc), then total mentions (desc).
    """
    # phrase -> set of sources, phrase -> list of (title, url, source)
    phrase_sources: dict[str, set] = defaultdict(set)
    phrase_examples: dict[str, list] = defaultdict(list)

    for h in headlines:
        words = _clean_words(h["title"])
        # Track both single keywords and 2-word phrases (better for names/topics)
        candidates = set(w.lower() for w in words) | set(
            bg.lower() for bg in _bigrams(words)
        )
        for phrase in candidates:
            phrase_sources[phrase].add(h["source"])
            if len(phrase_examples[phrase]) < 5:
                phrase_examples[phrase].append(
                    {"title": h["title"], "url": h["url"], "source": h["source"]}
                )

    results = []
    for phrase, sources in phrase_sources.items():
        if len(sources) >= min_sources:
            results.append(
                {
                    "phrase": phrase,
                    "num_sources": len(sources),
                    "sources": sorted(sources),
                    "examples": phrase_examples[phrase],
                }
            )

    results.sort(key=lambda r: (r["num_sources"], len(r["examples"])), reverse=True)
    return results