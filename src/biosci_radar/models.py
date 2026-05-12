from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Topic:
    id: str
    name: str
    priority: int
    keywords: list[str]


@dataclass
class Paper:
    id: str
    source: str
    title: str
    abstract: str = ""
    authors: list[str] = field(default_factory=list)
    published: str = ""
    year: int | None = None
    url: str = ""
    doi: str = ""
    pmid: str = ""
    arxiv_id: str = ""
    journal: str = ""
    categories: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    matched_keywords: list[str] = field(default_factory=list)
    paper_type: str = "Unknown"
    omics_types: list[str] = field(default_factory=list)
    diseases: list[str] = field(default_factory=list)
    ml_areas: list[str] = field(default_factory=list)
    code_available: bool = False
    data_available: bool = False
    transfer_potential: str = "Unknown"
    reproducibility: str = "Unknown"
    score: float = 0.0
    score_breakdown: dict[str, float] = field(default_factory=dict)
    why_relevant: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Paper":
        return cls(**data)


@dataclass
class FetchResult:
    generated_at: str
    days: int
    papers: list[Paper]
    stats: dict[str, int]
    focus_terms: list[str] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "days": self.days,
            "stats": self.stats,
            "focus_terms": self.focus_terms,
            "summary": self.summary,
            "papers": [p.to_dict() for p in self.papers],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FetchResult":
        return cls(
            generated_at=data.get("generated_at", ""),
            days=int(data.get("days", 0)),
            stats=dict(data.get("stats", {})),
            focus_terms=list(data.get("focus_terms", [])),
            summary=dict(data.get("summary", {})),
            papers=[Paper.from_dict(p) for p in data.get("papers", [])],
        )
