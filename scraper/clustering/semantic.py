"""Semantic headline clustering with embedding/TF-IDF fallback."""
from __future__ import annotations

from scraper.models import Article
from scraper.utils.text import tokenize


def cluster_articles(articles: list[Article], similarity_threshold: float = 0.42, min_cluster_size: int = 2) -> list[list[Article]]:
    if not articles:
        return []
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        texts = [a.title for a in articles]
        matrix = TfidfVectorizer(ngram_range=(1, 2), stop_words="english").fit_transform(texts)
        sims = cosine_similarity(matrix)
        parent = list(range(len(articles)))
        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb: parent[rb] = ra
        for i in range(len(articles)):
            for j in range(i + 1, len(articles)):
                entity_overlap = bool(set(articles[i].entities) & set(articles[j].entities))
                keyword_overlap = len(set(articles[i].keywords) & set(articles[j].keywords)) >= 1
                if sims[i, j] >= similarity_threshold or (entity_overlap and keyword_overlap) or len(set(articles[i].keywords) & set(articles[j].keywords)) >= 2 or ("tariff" in set(articles[i].keywords) & set(articles[j].keywords)):
                    union(i, j)
        groups: dict[int, list[Article]] = {}
        for i, article in enumerate(articles):
            groups.setdefault(find(i), []).append(article)
        return sorted(groups.values(), key=len, reverse=True)
    except Exception:
        return _fallback_token_clusters(articles, min_cluster_size)


def _fallback_token_clusters(articles: list[Article], min_cluster_size: int) -> list[list[Article]]:
    clusters: list[list[Article]] = []
    used: set[int] = set()
    token_sets = [set(a.keywords) or set(tokenize(a.title)) for a in articles]
    for i, article in enumerate(articles):
        if i in used:
            continue
        cluster = [article]
        used.add(i)
        for j in range(i + 1, len(articles)):
            if j in used:
                continue
            overlap = len(token_sets[i] & token_sets[j]) / max(1, len(token_sets[i] | token_sets[j]))
            if overlap >= 0.12 or len(token_sets[i] & token_sets[j]) >= 1:
                cluster.append(articles[j]); used.add(j)
        clusters.append(cluster)
    return sorted(clusters, key=len, reverse=True)
