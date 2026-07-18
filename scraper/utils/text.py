"""Text and URL normalization helpers."""
from __future__ import annotations

import hashlib
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_PREFIXES = ("utm_",)
TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid", "cmpid"}
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9&'’.-]*")


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=False) if k not in TRACKING_KEYS and not k.startswith(TRACKING_PREFIXES)]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower().removeprefix("www."), path, urlencode(query), ""))


def normalize_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title or "").strip()
    title = re.sub(r"\s+[-|–—]\s+[^-|–—]{2,40}$", "", title)
    return title


def title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", normalize_title(title).lower()).strip()


def stable_id(*parts: str) -> str:
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:16]


def tokenize(text: str, stopwords: set[str] | None = None) -> list[str]:
    stopwords = stopwords or set()
    return [w.lower().strip("'’.-") for w in WORD_RE.findall(text) if len(w) > 2 and w.lower() not in stopwords]
