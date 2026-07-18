"""JSON and SQLite storage for the headline/story pipeline."""
from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from typing import Any

DATA_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "data"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(exist_ok=True)


def save_headlines(headlines: list[Any], day: str | None = None) -> str:
    _ensure_data_dir(); day = day or date.today().isoformat(); path = DATA_DIR / f"headlines_{day}.json"
    rows = [h.to_dict() if hasattr(h, "to_dict") else h for h in headlines]
    path.write_text(json.dumps({"date": day, "headlines": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Saved {len(rows)} headlines to '{path}'")
    return str(path)


def save_trending(trending: list[Any], day: str | None = None) -> str:
    _ensure_data_dir(); day = day or date.today().isoformat(); path = DATA_DIR / f"trending_{day}.json"
    rows = [t.to_dict() if hasattr(t, "to_dict") else t for t in trending]
    path.write_text(json.dumps({"date": day, "stories": rows, "trending": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Saved {len(rows)} story clusters to '{path}'")
    return str(path)
