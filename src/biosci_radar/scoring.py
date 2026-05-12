from __future__ import annotations

from datetime import datetime
import re

from .config import AppConfig
from .models import Paper
from .text import contains_any, truncate


OMICS_KEYWORDS = {
    "bulk RNA-seq": ["RNA-seq", "transcriptomics", "gene expression"],
    "scRNA-seq": ["scRNA-seq", "single-cell RNA", "single cell RNA", "single-cell transcript"],
    "scATAC-seq": ["scATAC-seq", "single-cell ATAC", "chromatin accessibility"],
    "spatial": ["spatial transcriptomics", "spatial proteomics", "Visium", "Xenium", "CosMx"],
    "proteomics": ["proteomics", "proteome", "mass spectrometry", "phosphoproteomics"],
    "metabolomics": ["metabolomics", "metabolome", "lipidomics"],
    "epigenomics": ["epigenomics", "methylation", "ATAC-seq", "ChIP-seq"],
    "microbiome": ["microbiome", "metagenomics", "16S"],
}

DISEASE_KEYWORDS = {
    "cancer": ["cancer", "tumor", "tumour", "carcinoma", "oncology"],
    "LUAD": ["LUAD", "lung adenocarcinoma"],
    "lung cancer": ["lung cancer", "NSCLC"],
    "colorectal cancer": ["colorectal", "colon cancer", "CRC"],
    "breast cancer": ["breast cancer"],
    "glioma": ["glioma", "glioblastoma"],
    "immune": ["immune", "immunotherapy", "T cell", "macrophage"],
}

ML_KEYWORDS = {
    "Transformer": ["transformer", "attention", "language model"],
    "Foundation Model": ["foundation model", "pretrained model", "pre-trained model"],
    "GNN": ["graph neural network", "GNN", "graph learning"],
    "VAE": ["variational autoencoder", "VAE", "scVI"],
    "Contrastive": ["contrastive learning"],
    "Self-supervised": ["self-supervised", "self supervised", "masked modeling"],
    "Diffusion": ["diffusion model", "score-based"],
    "Survival": ["survival prediction", "Cox", "time-to-event"],
    "Causal": ["causal inference", "causal discovery"],
    "Multimodal": ["multimodal", "multi-modal", "vision-language"],
}

CODE_TERMS = ["github", "code is available", "source code", "implementation is available"]
DATA_TERMS = [
    "GEO",
    "SRA",
    "ArrayExpress",
    "TCGA",
    "CPTAC",
    "PRIDE",
    "MetaboLights",
    "data are available",
    "publicly available",
]


def enrich_and_score(papers: list[Paper], config: AppConfig) -> list[Paper]:
    for paper in papers:
        classify_and_score(paper, config)
    papers.sort(key=lambda p: p.score, reverse=True)
    return papers


def classify_and_score(paper: Paper, config: AppConfig) -> None:
    text = f"{paper.title}. {paper.abstract}"
    lower = text.lower()

    matched_topics: list[str] = []
    matched_keywords: list[str] = []
    weighted_topic_score = 0.0
    max_topic_score = sum(max(t.priority, 1) for t in config.topics) or 1
    for topic in config.topics:
        hits = contains_any(text, topic.keywords)
        if hits:
            matched_topics.append(topic.name)
            matched_keywords.extend(hits)
            weighted_topic_score += min(len(hits), 4) / 4 * max(topic.priority, 1)

    paper.topics = matched_topics
    paper.matched_keywords = sorted(set(matched_keywords), key=str.lower)
    paper.omics_types = _detect_bucket(text, OMICS_KEYWORDS)
    paper.diseases = _detect_bucket(text, DISEASE_KEYWORDS)
    paper.ml_areas = _detect_bucket(text, ML_KEYWORDS)
    paper.code_available = any(term.lower() in lower for term in CODE_TERMS)
    paper.data_available = any(term.lower() in lower for term in DATA_TERMS)
    paper.paper_type = detect_paper_type(paper, lower)
    paper.transfer_potential = detect_transfer_potential(paper)
    paper.reproducibility = detect_reproducibility(paper)

    relevance = min(weighted_topic_score / max_topic_score * 1.8, 1.0)
    method_value = min((len(paper.ml_areas) * 0.22) + ("method" in lower) * 0.15, 1.0)
    data_value = min((len(paper.omics_types) * 0.18) + (0.25 if paper.data_available else 0.0), 1.0)
    bio_value = min((len(paper.diseases) * 0.16) + ("patient" in lower) * 0.1 + ("clinical" in lower) * 0.1, 1.0)
    reproducibility = (0.45 if paper.code_available else 0.0) + (0.35 if paper.data_available else 0.0)
    reproducibility = min(reproducibility, 1.0)
    recency = recency_score(paper.published)

    if paper.paper_type == "ML Algorithm":
        score = (
            relevance * 0.10
            + method_value * 0.25
            + transfer_score(paper.transfer_potential) * 0.25
            + reproducibility * 0.15
            + data_value * 0.10
            + recency * 0.15
        )
    else:
        score = (
            relevance * 0.25
            + data_value * 0.20
            + bio_value * 0.15
            + method_value * 0.15
            + reproducibility * 0.15
            + recency * 0.10
        )

    paper.score = round(float(score), 4)
    paper.score_breakdown = {
        "relevance": round(relevance, 3),
        "method_value": round(method_value, 3),
        "data_value": round(data_value, 3),
        "bio_value": round(bio_value, 3),
        "reproducibility": round(reproducibility, 3),
        "recency": round(recency, 3),
    }
    paper.why_relevant = build_reason(paper)


def detect_paper_type(paper: Paper, lower: str) -> str:
    if "review" in lower or "survey" in lower:
        return "Review"
    if "dataset" in lower or "resource" in lower or "atlas" in lower:
        return "Dataset"
    if paper.ml_areas and not paper.omics_types and paper.source == "arXiv":
        return "ML Algorithm"
    if paper.ml_areas and ("algorithm" in lower or "model" in lower or "framework" in lower):
        return "ML Algorithm"
    if "method" in lower or "pipeline" in lower or "tool" in lower or "benchmark" in lower:
        return "Bioinformatics Method"
    return "Bio Study"


def detect_transfer_potential(paper: Paper) -> str:
    if paper.ml_areas and (paper.omics_types or any(t in paper.topics for t in ["Deep Learning for Omics", "Foundation Models for Biology"])):
        return "High"
    if paper.ml_areas:
        return "Medium"
    if len(paper.omics_types) >= 2:
        return "Medium"
    return "Low"


def detect_reproducibility(paper: Paper) -> str:
    if paper.code_available and paper.data_available:
        return "High"
    if paper.code_available or paper.data_available:
        return "Medium"
    return "Unknown"


def recency_score(published: str) -> float:
    if not published:
        return 0.4
    match = re.search(r"(20\d{2})(?:-(\d{2})-(\d{2}))?", published)
    if not match:
        return 0.4
    try:
        if match.group(2):
            date = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            days = max((datetime.now() - date).days, 0)
            if days <= 30:
                return 1.0
            if days <= 90:
                return 0.75
            if days <= 365:
                return 0.45
            return 0.2
        return 0.5
    except ValueError:
        return 0.4


def transfer_score(value: str) -> float:
    return {"High": 1.0, "Medium": 0.65, "Low": 0.25}.get(value, 0.3)


def build_reason(paper: Paper) -> str:
    parts: list[str] = []
    if paper.topics:
        parts.append("matches " + ", ".join(paper.topics[:2]))
    if paper.omics_types:
        parts.append("covers " + ", ".join(paper.omics_types[:3]))
    if paper.ml_areas:
        parts.append("uses " + ", ".join(paper.ml_areas[:3]))
    if paper.data_available:
        parts.append("mentions public data")
    if paper.code_available:
        parts.append("mentions code")
    if not parts:
        parts.append("weak but potentially relevant keyword match")
    return truncate("; ".join(parts), 260)


def _detect_bucket(text: str, mapping: dict[str, list[str]]) -> list[str]:
    found: list[str] = []
    for label, keywords in mapping.items():
        if contains_any(text, keywords):
            found.append(label)
    return found
