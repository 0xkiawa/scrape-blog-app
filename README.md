# 🛰️ News Intelligence Platform

An open-source headline intelligence system for journalists, editors, researchers and analysts. The project now detects **story clusters** instead of isolated repeated words, using modular source adapters, asynchronous RSS collection, NLP enrichment, semantic clustering, trend scoring and persistent story history.

## What changed

- **Story-first output:** JSON now contains story clusters with title, summary, score, status, entities, related keywords, source coverage, article angles, timeline and article-assistance fields.
- **30+ configurable publishers:** RSS-first configuration covers world news, politics, business, finance, technology, science, sports, entertainment, culture, education, Africa, Europe and more.
- **Async ingestion:** `aiohttp` fetches publishers concurrently with retry handling and per-source isolation.
- **Deduplication:** URLs are canonicalized and normalized headlines are deduplicated before NLP processing.
- **NLP pipeline:** Headlines are normalized, keyword-enriched, entity-enriched and category-classified. The architecture is ready for spaCy and sentence-transformer upgrades.
- **Semantic clustering:** scikit-learn TF-IDF n-grams + agglomerative clustering groups related headlines; a token-overlap fallback keeps the app functional in minimal environments.
- **Trend scoring:** weighted scoring considers publisher breadth, publisher authority, cluster size, freshness, entity strength and cross-category relevance.
- **Persistence:** Dated JSON outputs remain for backwards compatibility, while SQLite stores articles, current stories and trend history.

## Project structure

```text
scraper/
  config/              # publisher, taxonomy, weights and threshold JSON
  sources/             # source adapter interface, RSS adapter, async manager
  nlp/                 # entity, keyword and category enrichment
  clustering/          # semantic story clustering
  ranking/             # trend scoring and article assistance
  database/            # SQLite persistence; PostgreSQL can be added behind same interface
  cache/ api/ dashboard/ utils/
  main.py              # orchestration entrypoint
```

## Run

```bash
cd /workspace/scrape-blog-app
python -m pip install -r scraper/requirements.txt
python -m scraper.main
```

Outputs are written to `data/headlines_<date>.json`, `data/trending_<date>.json` and `data/news_intelligence.sqlite3`.

## Extend with another publisher

Add one object to `scraper/config/publishers.json`:

```json
{"name":"Example News","url":"https://example.com/news","feed_url":"https://example.com/rss","category":"World","country":"Global","authority":0.7}
```

No Python code is required for RSS/Atom sources. Custom sites can add a new adapter implementing `BaseSourceAdapter`.

## Migration notes

- `scraper.trend_analyzer.find_trending()` and `scraper.headline_scraper.fetch_headlines()` are retained for compatibility, but they now return story-cluster-oriented data.
- The old `trending` JSON key is still written as an alias of `stories` for readers that have not migrated yet.
- Install new dependencies: `aiohttp`, `feedparser`, and `scikit-learn`.
