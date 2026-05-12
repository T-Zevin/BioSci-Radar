from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from .config import AppConfig
from .models import Paper
from .storage import read_json, write_json
from .text import truncate


SYNC_PATH = Path("data/notion_sync.json")
NOTION_VERSION = "2022-06-28"


def sync_to_notion(config: AppConfig, papers: list[Paper], min_score: float) -> dict[str, int]:
    token = os.getenv(config.notion_token_env)
    database_id = os.getenv(config.notion_papers_database_id_env)
    if not token:
        raise RuntimeError(f"Missing {config.notion_token_env}.")
    if not database_id:
        raise RuntimeError(f"Missing {config.notion_papers_database_id_env}.")

    state = read_json(SYNC_PATH, {"synced": {}})
    synced: dict[str, str] = state.setdefault("synced", {})
    stats = {"created": 0, "skipped": 0, "failed": 0}

    for paper in papers:
        if paper.score < min_score:
            stats["skipped"] += 1
            continue
        sync_key = paper.doi or paper.pmid or paper.arxiv_id or paper.id
        if sync_key in synced:
            stats["skipped"] += 1
            continue
        try:
            page_id = create_paper_page(token, database_id, paper)
        except Exception as exc:
            stats["failed"] += 1
            print(f"[warn] Notion sync failed for {paper.title[:80]}: {exc}")
            continue
        synced[sync_key] = page_id
        stats["created"] += 1

    write_json(SYNC_PATH, state)
    return stats


def create_paper_page(token: str, database_id: str, paper: Paper) -> str:
    payload = {
        "parent": {"database_id": database_id},
        "properties": paper_properties(paper),
        "children": paper_children(paper),
    }
    data = notion_request(token, "POST", "https://api.notion.com/v1/pages", payload)
    return data["id"]


def paper_properties(paper: Paper) -> dict:
    return {
        "Title": {"title": [{"text": {"content": truncate(paper.title, 180)}}]},
        "Status": {"select": {"name": "New"}},
        "Priority": {"select": {"name": priority_from_score(paper.score)}},
        "Score": {"number": round(paper.score, 4)},
        "Paper Type": {"select": {"name": paper.paper_type}},
        "Source": {"select": {"name": paper.source}},
        "Year": {"number": paper.year} if paper.year else {"number": None},
        "Published": {"date": {"start": paper.published}} if is_iso_date(paper.published) else {"date": None},
        "URL": {"url": paper.url or None},
        "DOI": rich_text(paper.doi),
        "PMID": rich_text(paper.pmid),
        "Omics Type": multi_select(paper.omics_types),
        "Disease": multi_select(paper.diseases),
        "ML Area": multi_select(paper.ml_areas),
        "Topics": multi_select(paper.topics),
        "Code Available": {"checkbox": paper.code_available},
        "Data Available": {"checkbox": paper.data_available},
        "Transfer Potential": {"select": {"name": paper.transfer_potential}},
        "Reproducibility": {"select": {"name": paper.reproducibility}},
        "Why Relevant": rich_text(paper.why_relevant),
        "Abstract": rich_text(truncate(paper.abstract, 1900)),
    }


def paper_children(paper: Paper) -> list[dict]:
    blocks: list[dict] = [
        heading("Why this matters"),
        paragraph(paper.why_relevant or "No relevance reason generated."),
        heading("Structured Tags"),
        bulleted(f"Paper type: {paper.paper_type}"),
        bulleted(f"Topics: {', '.join(paper.topics) or 'None'}"),
        bulleted(f"Omics: {', '.join(paper.omics_types) or 'None'}"),
        bulleted(f"ML areas: {', '.join(paper.ml_areas) or 'None'}"),
        bulleted(f"Transfer potential: {paper.transfer_potential}"),
        heading("Abstract"),
        paragraph(truncate(paper.abstract or "No abstract available.", 1900)),
    ]
    if paper.url:
        blocks.append(paragraph(f"Source: {paper.url}"))
    return blocks


def notion_request(token: str, method: str, url: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        },
    )
    try:
        with urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {details}") from exc


def priority_from_score(score: float) -> str:
    if score >= 0.7:
        return "High"
    if score >= 0.45:
        return "Medium"
    return "Low"


def rich_text(value: str) -> dict:
    if not value:
        return {"rich_text": []}
    return {"rich_text": [{"text": {"content": truncate(value, 1900)}}]}


def multi_select(values: list[str]) -> dict:
    return {"multi_select": [{"name": truncate(v, 90)} for v in values[:20] if v]}


def is_iso_date(value: str) -> bool:
    if len(value) != 10:
        return False
    try:
        year, month, day = value.split("-")
        return len(year) == 4 and len(month) == 2 and len(day) == 2
    except ValueError:
        return False


def heading(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": truncate(text, 1900)}}]},
    }


def bulleted(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": truncate(text, 1900)}}]},
    }
