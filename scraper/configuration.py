"""Configuration loading for publishers, taxonomy, weights and thresholds."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .models import Publisher

CONFIG_DIR = Path(__file__).parent / "config"


@lru_cache(maxsize=1)
def load_publishers(path: str | Path | None = None) -> list[Publisher]:
    data = json.loads(Path(path or CONFIG_DIR / "publishers.json").read_text(encoding="utf-8"))
    return [Publisher(**item) for item in data if item.get("enabled", True)]


@lru_cache(maxsize=1)
def load_taxonomy(path: str | Path | None = None) -> dict:
    return json.loads(Path(path or CONFIG_DIR / "taxonomy.json").read_text(encoding="utf-8"))
