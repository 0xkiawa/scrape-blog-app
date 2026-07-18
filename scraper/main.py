"""
Daily headline pull + trend detection.

Run with:  python main.py

What it does:
  1. Fetches headline listings from 6 major outlets (titles + links only -
     never full article text).
  2. Saves the raw day's headlines to data/headlines_<date>.json.
  3. Finds words/phrases that show up across multiple outlets - that
     cross-source overlap is your trending-topic signal.
  4. Saves the ranked trend report to data/trending_<date>.json and
     prints a clean summary to the console so you can pick today's angle.
"""

from sites_config import SITES
from headline_scraper import fetch_headlines
from trend_analyzer import find_trending
from storage import save_headlines, save_trending


def run():
    all_headlines = []

    print("📡 Fetching headlines from 6 sources...\n")
    for site in SITES:
        headlines = fetch_headlines(site["url"], site["name"])
        print(f"  {site['name']:<18} -> {len(headlines)} headlines")
        all_headlines.extend(headlines)

    if not all_headlines:
        print("\n⚠️  No headlines fetched. Check network access or site markup changes.")
        return

    save_headlines(all_headlines)

    print("\n🔎 Detecting cross-source trending topics (min. 2 outlets)...\n")
    trending = find_trending(all_headlines, min_sources=2)
    save_trending(trending)

    if not trending:
        print("No overlapping topics today - every outlet went a different direction.")
        return

    print(f"Found {len(trending)} trending phrase(s):\n")
    for t in trending[:15]:
        sources_str = ", ".join(t["sources"])
        print(f"🔥 \"{t['phrase']}\"  —  {t['num_sources']} outlets ({sources_str})")
        for ex in t["examples"][:3]:
            print(f"     • [{ex['source']}] {ex['title']}")
        print()


if __name__ == "__main__":
    run()