from __future__ import annotations

from datetime import datetime, timedelta
import re
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

from .config import AppConfig, keyword_pool
from .http_client import get_json, get_text
from .models import Paper
from .text import clean_text, stable_id, year_from_date


def collect_all(
    config: AppConfig,
    days: int,
    limit: int,
    focus_terms: list[str] | None = None,
) -> tuple[list[Paper], dict[str, int]]:
    active_keywords = focus_terms or keyword_pool(config, per_topic=8)
    collectors = []
    if config.sources.get("pubmed", True):
        collectors.append(("PubMed", lambda cfg, d, l: collect_pubmed(cfg, d, l, active_keywords)))
    if config.sources.get("biorxiv", True):
        collectors.append(("bioRxiv", lambda cfg, d, l: collect_preprint("biorxiv", cfg, d, l, active_keywords)))
    if config.sources.get("medrxiv", True):
        collectors.append(("medRxiv", lambda cfg, d, l: collect_preprint("medrxiv", cfg, d, l, active_keywords)))
    if config.sources.get("arxiv", True):
        collectors.append(("arXiv", lambda cfg, d, l: collect_arxiv(cfg, d, l, active_keywords)))

    papers: list[Paper] = []
    stats: dict[str, int] = {}
    for name, fn in collectors:
        try:
            items = fn(config, days, limit)
        except Exception as exc:
            print(f"[warn] {name} collector failed: {exc}")
            items = []
        stats[name] = len(items)
        papers.extend(items)

    return dedupe_papers(papers, config), stats


def collect_pubmed(
    config: AppConfig,
    days: int,
    limit: int,
    keywords: list[str] | None = None,
) -> list[Paper]:
    keywords = keywords or keyword_pool(config, per_topic=5)
    query = " OR ".join(f'"{kw}"[Title/Abstract]' for kw in keywords[:40])
    if not query:
        return []

    search = get_json(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": limit,
            "sort": "pub date",
            "reldate": days,
            "datetype": "pdat",
        },
    )
    ids = search.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []

    summary = get_json(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        {"db": "pubmed", "id": ",".join(ids), "retmode": "json"},
    )
    result = summary.get("result", {})
    papers: list[Paper] = []
    for pmid in ids:
        item = result.get(pmid, {})
        title = clean_text(item.get("title", ""))
        if not title:
            continue
        authors = [a.get("name", "") for a in item.get("authors", []) if a.get("name")]
        article_ids = item.get("articleids", [])
        doi = ""
        for article_id in article_ids:
            if article_id.get("idtype") == "doi":
                doi = article_id.get("value", "")
                break
        published = item.get("pubdate", "")
        source = item.get("source", "")
        papers.append(
            Paper(
                id=f"pmid:{pmid}",
                source="PubMed",
                title=title,
                authors=authors,
                published=published,
                year=year_from_date(published),
                url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                doi=doi,
                pmid=pmid,
                journal=source,
                abstract=clean_text(item.get("sorttitle", "")),
            )
        )

    enrich_pubmed_abstracts(papers)
    return papers


def enrich_pubmed_abstracts(papers: list[Paper]) -> None:
    pmids = [p.pmid for p in papers if p.pmid]
    if not pmids:
        return
    try:
        xml = get_text(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
            {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"},
            timeout=60,
        )
    except Exception:
        return
    root = ET.fromstring(xml)
    by_pmid = {p.pmid: p for p in papers}
    for article in root.findall(".//PubmedArticle"):
        pmid_node = article.find(".//PMID")
        if pmid_node is None or not pmid_node.text:
            continue
        paper = by_pmid.get(pmid_node.text)
        if not paper:
            continue
        parts = []
        for abstract_node in article.findall(".//AbstractText"):
            label = abstract_node.attrib.get("Label")
            text = clean_text(" ".join(abstract_node.itertext()))
            if text:
                parts.append(f"{label}: {text}" if label else text)
        if parts:
            paper.abstract = " ".join(parts)


def collect_preprint(
    server: str,
    config: AppConfig,
    days: int,
    limit: int,
    keywords: list[str] | None = None,
) -> list[Paper]:
    end = datetime.now().date()
    start = end - timedelta(days=days)
    cursor = 0
    papers: list[Paper] = []
    keywords = keywords or keyword_pool(config, per_topic=8)
    while len(papers) < limit:
        url = f"https://api.biorxiv.org/details/{server}/{start.isoformat()}/{end.isoformat()}/{cursor}"
        data = get_json(url, timeout=60)
        collection = data.get("collection", [])
        if not collection:
            break
        for item in collection:
            title = clean_text(item.get("title", ""))
            abstract = clean_text(item.get("abstract", ""))
            haystack = f"{title} {abstract}"
            if not any(k.lower() in haystack.lower() for k in keywords):
                continue
            doi = item.get("doi", "")
            source_name = "bioRxiv" if server == "biorxiv" else "medRxiv"
            papers.append(
                Paper(
                    id=f"{server}:{doi or stable_id(title)}",
                    source=source_name,
                    title=title,
                    abstract=abstract,
                    authors=_split_authors(item.get("authors", "")),
                    published=item.get("date", ""),
                    year=year_from_date(item.get("date", "")),
                    doi=doi,
                    url=item.get("url") or f"https://doi.org/{doi}" if doi else "",
                    journal=source_name,
                )
            )
            if len(papers) >= limit:
                break
        messages = data.get("messages", [{}])
        total = int(messages[0].get("total", 0) or 0)
        cursor += len(collection)
        if cursor >= total or cursor == 0:
            break
    return papers


def collect_arxiv(
    config: AppConfig,
    days: int,
    limit: int,
    keywords: list[str] | None = None,
) -> list[Paper]:
    end = datetime.now()
    start = end - timedelta(days=days)
    categories = config.arxiv_categories[:]
    cat_query = " OR ".join(f"cat:{cat}" for cat in categories)
    date_query = f"submittedDate:[{start:%Y%m%d}0000 TO {end:%Y%m%d}2359]"
    query = f"({cat_query}) AND {date_query}"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max(limit * 5, limit),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    xml = get_text(f"https://export.arxiv.org/api/query?{urlencode(params)}", timeout=60)
    papers = parse_arxiv(xml)
    keywords = keywords or keyword_pool(config, per_topic=8)
    filtered: list[Paper] = []
    for paper in papers:
        haystack = f"{paper.title} {paper.abstract}".lower()
        if any(keyword.lower() in haystack for keyword in keywords):
            filtered.append(paper)
        if len(filtered) >= limit:
            break
    return filtered


def parse_arxiv(xml: str) -> list[Paper]:
    root = ET.fromstring(xml)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    papers: list[Paper] = []
    for entry in root.findall("atom:entry", ns):
        entry_id = clean_text(_find_text(entry, "atom:id", ns))
        arxiv_id = entry_id.rsplit("/", 1)[-1] if entry_id else ""
        title = clean_text(_find_text(entry, "atom:title", ns))
        abstract = clean_text(_find_text(entry, "atom:summary", ns))
        published = clean_text(_find_text(entry, "atom:published", ns))[:10]
        authors = [
            clean_text(a.findtext("atom:name", default="", namespaces=ns))
            for a in entry.findall("atom:author", ns)
        ]
        categories = [
            c.attrib.get("term", "")
            for c in entry.findall("atom:category", ns)
            if c.attrib.get("term")
        ]
        doi = clean_text(_find_text(entry, "arxiv:doi", ns))
        papers.append(
            Paper(
                id=f"arxiv:{arxiv_id}",
                source="arXiv",
                title=title,
                abstract=abstract,
                authors=authors,
                published=published,
                year=year_from_date(published),
                url=f"https://arxiv.org/abs/{arxiv_id}",
                doi=doi,
                arxiv_id=arxiv_id,
                categories=categories,
            )
        )
    return papers


def dedupe_papers(papers: list[Paper], config: AppConfig) -> list[Paper]:
    seen: set[str] = set()
    result: list[Paper] = []
    for paper in papers:
        haystack = f"{paper.title} {paper.abstract}".lower()
        if any(excluded in haystack for excluded in config.excluded_keywords):
            continue
        key = paper.doi.lower() or paper.pmid or paper.arxiv_id or re.sub(r"\W+", "", paper.title.lower())[:120]
        if key in seen:
            continue
        seen.add(key)
        result.append(paper)
    return result


def _find_text(node: ET.Element, path: str, ns: dict[str, str]) -> str:
    found = node.find(path, ns)
    return found.text if found is not None and found.text else ""


def _split_authors(value: str) -> list[str]:
    if not value:
        return []
    return [clean_text(a) for a in re.split(r";|, and | and ", value) if clean_text(a)]
