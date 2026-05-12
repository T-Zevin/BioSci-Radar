from __future__ import annotations

import hashlib
import html
import re
from datetime import datetime


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = TAG_RE.sub(" ", value)
    return SPACE_RE.sub(" ", value).strip()


def stable_id(*parts: str) -> str:
    joined = "|".join(p.strip().lower() for p in parts if p)
    return hashlib.sha1(joined.encode("utf-8")).hexdigest()[:16]


def year_from_date(value: str) -> int | None:
    match = re.search(r"(19|20)\d{2}", value or "")
    return int(match.group(0)) if match else None


def today_iso() -> str:
    return datetime.now().date().isoformat()


def contains_any(text: str, keywords: list[str]) -> list[str]:
    haystack = text.lower()
    found: list[str] = []
    for keyword in keywords:
        key = keyword.lower().strip()
        if not key:
            continue
        if re.search(rf"(?<![a-z0-9]){re.escape(key)}(?![a-z0-9])", haystack):
            found.append(keyword)
    return found


def truncate(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"
