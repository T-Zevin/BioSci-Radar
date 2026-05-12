from __future__ import annotations

import json
from pathlib import Path

from .models import FetchResult
from .text import today_iso


DATA_DIR = Path("data")
PAPERS_DIR = DATA_DIR / "papers"
LATEST_PATH = PAPERS_DIR / "latest.json"


def save_result(result: FetchResult) -> Path:
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    dated = PAPERS_DIR / f"{today_iso()}.json"
    payload = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
    dated.write_text(payload, encoding="utf-8")
    LATEST_PATH.write_text(payload, encoding="utf-8")
    return dated


def load_latest() -> FetchResult:
    if not LATEST_PATH.exists():
        raise FileNotFoundError("No fetched data found. Run `python3 -m biosci_radar fetch` or `biosci-radar fetch` first.")
    return FetchResult.from_dict(json.loads(LATEST_PATH.read_text(encoding="utf-8")))


def read_json(path: Path, fallback):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
