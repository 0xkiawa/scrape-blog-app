"""Headline NLP enrichment: keywords, entities and categories."""
from __future__ import annotations

from collections import Counter

from scraper.configuration import load_taxonomy
from scraper.models import Article
from scraper.utils.text import tokenize

CATEGORY_TERMS = {
    "Politics": {"election","senate","president","minister","government","congress","trump","biden","policy"},
    "Business": {"company","ceo","market","sales","business","deal","earnings"},
    "Finance": {"stocks","inflation","fed","rates","bank","crypto","tariff","oil"},
    "Technology": {"ai","software","apple","google","microsoft","openai","tesla","chip","data"},
    "Science": {"research","space","nasa","study","scientists","climate"},
    "Health": {"health","virus","drug","vaccine","hospital","disease"},
    "Entertainment": {"movie","film","actor","music","hollywood","show","album"},
    "Sports": {"nba","nfl","world cup","olympics","coach","team","match"},
    "Climate": {"climate","emissions","warming","flood","wildfire","carbon"},
    "Crime": {"police","court","trial","charged","murder","arrested"},
    "Africa": {"africa","nairobi","kenya","nigeria","south africa"},
    "Middle East": {"israel","gaza","iran","syria","lebanon","qatar"},
    "Asia": {"china","india","japan","korea","taiwan"},
    "Europe": {"europe","ukraine","france","germany","britain","eu"},
    "Americas": {"mexico","canada","brazil","argentina"},
}

KNOWN_ENTITIES = {"OpenAI","Microsoft","Apple","Google","Tesla","Donald Trump","Joe Biden","NATO","EU","UN","Olympics","World Cup","Christopher Nolan"}


def enrich_articles(articles: list[Article]) -> list[Article]:
    taxonomy = load_taxonomy()
    stopwords = set(taxonomy["stopwords"])
    for article in articles:
        article.keywords = extract_keywords(article.title, stopwords)
        article.entities = extract_entities(article.title)
    return articles


def extract_keywords(text: str, stopwords: set[str] | None = None, limit: int = 8) -> list[str]:
    counts = Counter(tokenize(text, stopwords))
    return [_stem(word) for word, _ in counts.most_common(limit)]


def extract_entities(text: str) -> list[str]:
    found = {entity for entity in KNOWN_ENTITIES if entity.lower() in text.lower()}
    words = text.replace("’", "'").split()
    current: list[str] = []
    for raw in words:
        word = raw.strip(".,:;!?()[]{}\"'")
        if word[:1].isupper() and len(word) > 1:
            current.append(word)
        else:
            if len(current) >= 1:
                found.add(" ".join(current[:4]))
            current = []
    if current:
        found.add(" ".join(current[:4]))
    return sorted(e for e in found if len(e) > 2)


def classify_categories(articles: list[Article], limit: int = 3) -> list[str]:
    haystack = " ".join(a.title for a in articles).lower()
    scores: Counter[str] = Counter()
    for article in articles:
        if article.category_hint:
            scores[article.category_hint] += 2
    for category, terms in CATEGORY_TERMS.items():
        for term in terms:
            if term in haystack:
                scores[category] += 3
    if not scores:
        return ["World"]
    return [cat for cat, _ in scores.most_common(limit)]


def _stem(word: str) -> str:
    return word[:-1] if len(word) > 4 and word.endswith("s") else word
