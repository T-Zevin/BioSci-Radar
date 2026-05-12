from __future__ import annotations

from pathlib import Path

from .dashboard import zh_label, zh_reason
from .models import FetchResult, Paper


EXPORT_DIR = Path("data/exports")


def export_markdown(result: FetchResult, lang: str = "both") -> list[Path]:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    langs = ["zh", "en"] if lang == "both" else [lang]
    paths: list[Path] = []
    for item in langs:
        if item not in {"zh", "en"}:
            raise ValueError("lang must be zh, en, or both")
        path = EXPORT_DIR / f"recommendations.{item}.md"
        path.write_text(render_markdown(result, item), encoding="utf-8")
        paths.append(path)
    return paths


def render_markdown(result: FetchResult, lang: str) -> str:
    if lang == "zh":
        lines = [
            "# 多组学与 AI 文献推荐",
            "",
            f"- 生成时间：{result.generated_at}",
            f"- 检索窗口：最近 {result.days} 天",
            f"- 论文数量：{len(result.papers)}",
            f"- 来源统计：{result.stats}",
            "",
        ]
        sections = [
            ("ML Algorithm", "机器学习/深度学习算法论文"),
            ("Bioinformatics Method", "生信方法论文"),
            ("Bio Study", "生物医学/多组学应用论文"),
            ("Dataset", "数据集/资源论文"),
            ("Review", "综述论文"),
        ]
    else:
        lines = [
            "# Bio-Omics and AI Literature Recommendations",
            "",
            f"- Generated at: {result.generated_at}",
            f"- Search window: last {result.days} days",
            f"- Paper count: {len(result.papers)}",
            f"- Source stats: {result.stats}",
            "",
        ]
        sections = [
            ("ML Algorithm", "Machine Learning / Deep Learning Methods"),
            ("Bioinformatics Method", "Bioinformatics Methods"),
            ("Bio Study", "Biomedical / Multi-omics Studies"),
            ("Dataset", "Datasets and Resources"),
            ("Review", "Reviews"),
        ]

    for paper_type, heading in sections:
        papers = [p for p in result.papers if p.paper_type == paper_type]
        if not papers:
            continue
        lines.extend([f"## {heading}", ""])
        for idx, paper in enumerate(papers, start=1):
            lines.extend(render_paper(paper, idx, lang))
    return "\n".join(lines).rstrip() + "\n"


def render_paper(paper: Paper, idx: int, lang: str) -> list[str]:
    if lang == "zh":
        reason = zh_reason(paper)
        labels = {
            "score": "评分",
            "source": "来源",
            "authors": "作者",
            "topics": "研究方向",
            "omics": "组学",
            "ml": "算法方向",
            "reason": "推荐理由",
            "abstract": "摘要",
            "url": "链接",
        }
        paper_type = zh_label(paper.paper_type)
        topics = "、".join(zh_label(v) for v in paper.topics) or "无"
        omics = "、".join(zh_label(v) for v in paper.omics_types) or "无"
        ml = "、".join(zh_label(v) for v in paper.ml_areas) or "无"
    else:
        reason = paper.why_relevant
        labels = {
            "score": "Score",
            "source": "Source",
            "authors": "Authors",
            "topics": "Topics",
            "omics": "Omics",
            "ml": "ML areas",
            "reason": "Why relevant",
            "abstract": "Abstract",
            "url": "URL",
        }
        paper_type = paper.paper_type
        topics = ", ".join(paper.topics) or "None"
        omics = ", ".join(paper.omics_types) or "None"
        ml = ", ".join(paper.ml_areas) or "None"

    authors = ", ".join(paper.authors[:8]) or "Unknown"
    title = paper.title.strip()
    url_line = f"- **{labels['url']}**: {paper.url}" if paper.url else ""
    lines = [
        f"### {idx}. {title}",
        "",
        f"- **Type**: {paper_type}" if lang == "en" else f"- **类型**：{paper_type}",
        f"- **{labels['score']}**: {paper.score:.2f}" if lang == "en" else f"- **{labels['score']}**：{paper.score:.2f}",
        f"- **{labels['source']}**: {paper.source}" if lang == "en" else f"- **{labels['source']}**：{paper.source}",
        f"- **{labels['authors']}**: {authors}" if lang == "en" else f"- **{labels['authors']}**：{authors}",
        f"- **{labels['topics']}**: {topics}" if lang == "en" else f"- **{labels['topics']}**：{topics}",
        f"- **{labels['omics']}**: {omics}" if lang == "en" else f"- **{labels['omics']}**：{omics}",
        f"- **{labels['ml']}**: {ml}" if lang == "en" else f"- **{labels['ml']}**：{ml}",
        f"- **{labels['reason']}**: {reason}" if lang == "en" else f"- **{labels['reason']}**：{reason}",
    ]
    if url_line:
        lines.append(url_line)
    if paper.abstract:
        lines.extend(["", f"**{labels['abstract']}**", "", paper.abstract.strip()])
    lines.append("")
    return lines
