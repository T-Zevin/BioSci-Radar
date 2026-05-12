from __future__ import annotations

import argparse
from datetime import datetime
import json
import sys

from .collectors import collect_all
from .config import load_config, with_focus_terms
from .dashboard import serve as serve_dashboard
from .markdown_export import export_markdown
from .models import FetchResult
from .notion import sync_to_notion
from .scoring import enrich_and_score
from .summary import build_summary
from .storage import load_latest, save_result


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="biosci-radar")
    parser.add_argument("--config", default="config.toml", help="Path to config TOML.")
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="Fetch, classify, score, and cache papers.")
    fetch.add_argument("--days", type=int, default=None)
    fetch.add_argument("--limit", type=int, default=None)
    fetch.add_argument("--focus", default="", help="Comma-separated temporary keywords for this fetch.")

    serve = sub.add_parser("serve", help="Serve the local dashboard.")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)

    notion = sub.add_parser("notion-sync", help="Sync cached papers into Notion.")
    notion.add_argument("--min-score", type=float, default=0.45)

    export = sub.add_parser("export-md", help="Export cached papers to bilingual Markdown.")
    export.add_argument("--lang", choices=["zh", "en", "both"], default="both")

    sub.add_parser("show-config", help="Print resolved config.")

    args = parser.parse_args(argv)
    config = load_config(args.config)

    if args.command == "fetch":
        days = args.days or config.default_days
        limit = args.limit or config.max_results_per_source
        focus_terms = [item.strip() for item in args.focus.split(",") if item.strip()]
        active_config = with_focus_terms(config, focus_terms)
        papers, stats = collect_all(active_config, days=days, limit=limit, focus_terms=focus_terms or None)
        papers = enrich_and_score(papers, active_config)
        result = FetchResult(
            generated_at=datetime.now().isoformat(timespec="seconds"),
            days=days,
            papers=papers,
            stats=stats,
            focus_terms=focus_terms,
            summary=build_summary(papers),
        )
        path = save_result(result)
        print(f"Saved {len(papers)} papers to {path}")
        print("Top papers:")
        for idx, paper in enumerate(papers[:10], start=1):
            print(f"{idx:>2}. {paper.score:.2f} [{paper.paper_type}] {paper.title[:110]}")
        return

    if args.command == "serve":
        serve_dashboard(host=args.host, port=args.port)
        return

    if args.command == "notion-sync":
        latest = load_latest()
        stats = sync_to_notion(config, latest.papers, min_score=args.min_score)
        print(f"Notion sync: {stats}")
        return

    if args.command == "export-md":
        latest = load_latest()
        paths = export_markdown(latest, lang=args.lang)
        for path in paths:
            print(f"Exported {path}")
        return

    if args.command == "show-config":
        print(json.dumps(_config_to_jsonable(config), ensure_ascii=False, indent=2))
        return

    parser.print_help()
    sys.exit(2)


def _config_to_jsonable(config):
    return {
        "language": config.language,
        "timezone": config.timezone,
        "default_days": config.default_days,
        "max_results_per_source": config.max_results_per_source,
        "sources": config.sources,
        "topics": [topic.__dict__ for topic in config.topics],
        "arxiv_categories": config.arxiv_categories,
        "excluded_keywords": config.excluded_keywords,
        "min_dashboard_score": config.min_dashboard_score,
        "notion_token_env": config.notion_token_env,
        "notion_papers_database_id_env": config.notion_papers_database_id_env,
    }
