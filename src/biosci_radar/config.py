from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import tomllib

from .models import Topic


@dataclass
class AppConfig:
    language: str
    timezone: str
    default_days: int
    max_results_per_source: int
    sources: dict[str, bool]
    topics: list[Topic]
    arxiv_categories: list[str]
    excluded_keywords: list[str]
    min_dashboard_score: float
    notion_token_env: str
    notion_papers_database_id_env: str


def load_config(path: str | Path = "config.toml") -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        config_path = Path("config.example.toml")
    raw = tomllib.loads(config_path.read_text(encoding="utf-8"))

    topics = [
        Topic(
            id=str(item["id"]),
            name=str(item["name"]),
            priority=int(item.get("priority", 3)),
            keywords=[str(k) for k in item.get("keywords", [])],
        )
        for item in raw.get("topics", [])
    ]

    general = raw.get("general", {})
    scoring = raw.get("scoring", {})
    notion = raw.get("notion", {})

    return AppConfig(
        language=str(general.get("language", "zh")),
        timezone=str(general.get("timezone", "Asia/Shanghai")),
        default_days=int(general.get("default_days", 14)),
        max_results_per_source=int(general.get("max_results_per_source", 60)),
        sources={str(k): bool(v) for k, v in raw.get("sources", {}).items()},
        topics=topics,
        arxiv_categories=[str(c) for c in raw.get("arxiv", {}).get("categories", [])],
        excluded_keywords=[
            str(k).lower() for k in raw.get("filters", {}).get("excluded_keywords", [])
        ],
        min_dashboard_score=float(scoring.get("min_dashboard_score", 0.25)),
        notion_token_env=str(notion.get("token_env", "NOTION_TOKEN")),
        notion_papers_database_id_env=str(
            notion.get("papers_database_id_env", "NOTION_PAPERS_DATABASE_ID")
        ),
    )


def keyword_pool(config: AppConfig, per_topic: int = 8) -> list[str]:
    seen: set[str] = set()
    keywords: list[str] = []
    for topic in sorted(config.topics, key=lambda t: t.priority, reverse=True):
        for keyword in topic.keywords[:per_topic]:
            key = keyword.lower()
            if key not in seen:
                seen.add(key)
                keywords.append(keyword)
    return keywords


def with_focus_terms(config: AppConfig, focus_terms: list[str]) -> AppConfig:
    active_terms = [term.strip() for term in focus_terms if term.strip()]
    if not active_terms:
        return config
    return replace(
        config,
        topics=[
            Topic(
                id="custom_focus",
                name="Custom Focus",
                priority=8,
                keywords=active_terms,
            ),
            *config.topics,
        ],
    )
