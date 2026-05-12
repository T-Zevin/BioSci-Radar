<div align="center">

# BioSci-Radar

<p>
  <a href="README.zh.md">
    <img src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87%E8%AF%B4%E6%98%8E-README-0f172a?style=for-the-badge&logo=readme&logoColor=white" alt="Chinese README">
  </a>
  <img src="https://img.shields.io/badge/English-README-2563eb?style=for-the-badge&logo=readme&logoColor=white" alt="English README">
</p>

<p>
  <img src="https://img.shields.io/badge/Local--First-Workspace-16a34a?style=flat-square" alt="Local-first workspace">
  <img src="https://img.shields.io/badge/Bilingual-ZH%20%2F%20EN-7c3aed?style=flat-square" alt="Bilingual">
  <img src="https://img.shields.io/badge/Python-3.11%2B-2563eb?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Notion-Optional-111827?style=flat-square&logo=notion&logoColor=white" alt="Notion optional">
</p>

<p><strong>A local-first literature workspace for bioinformatics, multi-omics, and transferable ML/DL methods.</strong></p>

<p>
  Start from sample keywords or your own query, then move into a bilingual workspace for focused paper discovery,
  frequency insights, and paginated browsing.
</p>

<p>
  <a href="#quick-start">Quick Start</a> ·
  <a href="#tutorial">Tutorial</a> ·
  <a href="#common-commands">Commands</a> ·
  <a href="#notion-sync">Notion Sync</a>
</p>

</div>

![docs/images/homepage-overview.png](image.png)


## What It Does

BioSci-Radar is built as a research-facing local web app rather than a command-only fetch script.

- Fetches papers from `PubMed`, `bioRxiv`, `medRxiv`, and `arXiv`
- Supports temporary keyword-focused runs such as `LUAD`, `spatial transcriptomics`, or `graph neural network`
- Classifies papers into `Bio Study`, `Bioinformatics Method`, `ML Algorithm`, `Dataset`, and `Review`
- Summarizes frequency signals for keywords, topics, omics types, diseases, and ML tags
- Exports bilingual Markdown reports
- Optionally syncs selected results into a Notion database

![BioSci-Radar Architecture](docs/images/architecture.svg)

## Workflow

1. Open the homepage.
2. Click a sample keyword or enter your own focus.
3. Scroll into the workspace and run a fetch from the page or CLI.
4. Review the summary cards for keyword and tag frequencies.
5. Read the paginated paper list and open source links.
6. Export Markdown or sync to Notion if needed.

![docs/images/workspace-results.png](image-1.png)

## Quick Start

```bash
cd "/Users/xzw/Documents/New project 3/BioSci-Radar"
cp config.example.toml config.toml
python3 -m pip install -e .
```

Run the local web app:

```bash
PYTHONPATH=src python3 -m biosci_radar serve --port 8765
```

Then open:

`http://127.0.0.1:8765`

## Tutorial

### Option A: Use the Local Web UI

1. Open `http://127.0.0.1:8765`
2. Start from the welcome screen:
   - click a sample keyword to run a focused fetch immediately, or
   - click `Start Exploring` and type your own focus
3. In the workspace input box, use keywords such as:
   `LUAD, spatial transcriptomics, graph neural network`
4. Set the time window and per-source fetch limit
5. Click `Fetch papers`
6. Review:
   - keyword frequency
   - source counts
   - topic / omics / disease / ML tag counts
   - paginated paper list
7. Switch `中文 / English` in the top-right corner if needed

### Option B: Use the CLI

Default profile fetch:

```bash
biosci-radar fetch --days 14 --limit 80
```

Focused fetch:

```bash
biosci-radar fetch --focus "LUAD, spatial transcriptomics, graph neural network" --days 14 --limit 40
```

Module form also works:

```bash
PYTHONPATH=src python3 -m biosci_radar fetch --focus "LUAD, spatial transcriptomics" --days 7 --limit 20
PYTHONPATH=src python3 -m biosci_radar serve --port 8765
```

## Common Commands

```bash
biosci-radar fetch
biosci-radar fetch --focus "single-cell multiomics, survival prediction"
biosci-radar serve
biosci-radar export-md --lang both
biosci-radar notion-sync --min-score 0.45
biosci-radar show-config
```

## Output Files

- `data/papers/latest.json`: latest normalized paper list and summary
- `data/papers/YYYY-MM-DD.json`: dated fetch snapshots
- `data/exports/recommendations.zh.md`: Chinese Markdown export
- `data/exports/recommendations.en.md`: English Markdown export
- `data/notion_sync.json`: local Notion sync state

## Notion Sync

1. Create a Notion integration.
2. Create a papers database and share it with the integration.
3. Export environment variables:

```bash
export NOTION_TOKEN="secret_..."
export NOTION_PAPERS_DATABASE_ID="..."
```

4. Sync results:

```bash
biosci-radar notion-sync --min-score 0.45
```

Schema reference: [docs/notion_schema.md](docs/notion_schema.md)

## Current Scope

- Python standard library only
- No required database
- No required LLM API key
- Rule-based fetch, classification, scoring, and summary
- Designed for local review first, then GitHub or Notion export
