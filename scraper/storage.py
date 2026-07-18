"""
Storage for the headline-only pipeline.

We save one dated JSON file per day containing all scraped headlines,
plus a separate dated "trending" file with the cross-source overlap report.
Nothing here ever stores full article body text.
"""

import json
import os
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def save_headlines(headlines: list[dict], day: str = None) -> str:
    """Save the day's raw headlines. Returns the file path written."""
    _ensure_data_dir()
    day = day or date.today().isoformat()
    path = os.path.join(DATA_DIR, f"headlines_{day}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"date": day, "headlines": headlines}, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(headlines)} headlines to '{path}'")
    return path


def save_trending(trending: list[dict], day: str = None) -> str:
    """Save the day's trending-topic report. Returns the file path written."""
    _ensure_data_dir()
    day = day or date.today().isoformat()
    path = os.path.join(DATA_DIR, f"trending_{day}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"date": day, "trending": trending}, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(trending)} trending phrases to '{path}'")
    return path