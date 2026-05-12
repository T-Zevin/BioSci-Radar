from __future__ import annotations

from collections import Counter

from .models import Paper


def build_summary(papers: list[Paper]) -> dict:
    return {
        "total_papers": len(papers),
        "sources": top_counts(p.source for p in papers),
        "paper_types": top_counts(p.paper_type for p in papers),
        "topics": top_counts(item for p in papers for item in p.topics),
        "matched_keywords": top_counts(item for p in papers for item in p.matched_keywords),
        "omics_types": top_counts(item for p in papers for item in p.omics_types),
        "ml_areas": top_counts(item for p in papers for item in p.ml_areas),
        "diseases": top_counts(item for p in papers for item in p.diseases),
    }


def top_counts(values, limit: int = 10) -> list[dict[str, int | str]]:
    counter = Counter(value for value in values if value)
    return [{"label": label, "count": count} for label, count in counter.most_common(limit)]
