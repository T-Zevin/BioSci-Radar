from __future__ import annotations

from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import html
import io
import json
from urllib.parse import parse_qs, urlparse
import zipfile

from .collectors import collect_all
from .config import load_config, with_focus_terms
from .models import FetchResult, Paper
from .scoring import enrich_and_score
from .storage import load_latest, save_result
from .summary import build_summary


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Dashboard: http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self) -> None:
        route = urlparse(self.path).path
        if route in {"/", "/index.html", "/api/papers", "/api/fetch", "/api/export"}:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            return
        self.send_error(404)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path
        if route == "/api/papers":
            self.handle_load_latest()
            return
        if route == "/api/export":
            self.handle_export(parsed.query)
            return
        if route in {"/", "/index.html"}:
            self.html_response(render_dashboard())
            return
        self.send_error(404)

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        if route == "/api/fetch":
            self.handle_fetch()
            return
        self.send_error(404)

    def log_message(self, fmt: str, *args) -> None:
        return

    def handle_load_latest(self) -> None:
        try:
            self.json_response(load_latest().to_dict(), status=200)
        except Exception as exc:
            self.json_response({"error": str(exc)}, status=404)

    def handle_fetch(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length) if length else b"{}"
            payload = json.loads(body.decode("utf-8"))
            config = load_config()
            days = max(1, int(payload.get("days") or config.default_days))
            limit = max(5, int(payload.get("limit") or config.max_results_per_source))
            focus_text = str(payload.get("focus") or "").strip()
            focus_terms = [item.strip() for item in focus_text.split(",") if item.strip()]
            active_config = with_focus_terms(config, focus_terms)
            papers, stats = collect_all(
                active_config,
                days=days,
                limit=limit,
                focus_terms=focus_terms or None,
            )
            papers = enrich_and_score(papers, active_config)
            result = FetchResult(
                generated_at=datetime.now().isoformat(timespec="seconds"),
                days=days,
                papers=papers,
                stats=stats,
                focus_terms=focus_terms,
                summary=build_summary(papers),
            )
            save_result(result)
            self.json_response(result.to_dict(), status=200)
        except Exception as exc:
            self.json_response({"error": str(exc)}, status=500)

    def handle_export(self, query: str) -> None:
        try:
            from .markdown_export import export_markdown

            params = parse_qs(query or "")
            lang = (params.get("lang") or ["both"])[0].strip().lower() or "both"
            if lang not in {"zh", "en", "both"}:
                raise ValueError("lang must be zh, en, or both")
            latest = load_latest()
            paths = export_markdown(latest, lang=lang)
            if lang == "both":
                archive = io.BytesIO()
                with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                    for path in paths:
                        zf.write(path, arcname=path.name)
                filename = export_filename(latest, "both", "zip")
                self.binary_response(
                    archive.getvalue(),
                    content_type="application/zip",
                    filename=filename,
                )
                return

            path = paths[0]
            filename = export_filename(latest, lang, "md")
            self.binary_response(
                path.read_bytes(),
                content_type="text/markdown; charset=utf-8",
                filename=filename,
            )
        except FileNotFoundError as exc:
            self.json_response({"error": str(exc)}, status=404)
        except Exception as exc:
            self.json_response({"error": str(exc)}, status=400)

    def html_response(self, body: str) -> None:
        payload = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def json_response(self, data, status: int = 200) -> None:
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def binary_response(self, payload: bytes, content_type: str, filename: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(payload)


def export_filename(result: FetchResult, lang: str, suffix: str) -> str:
    stamp = result.generated_at.replace(":", "").replace("-", "").replace("T", "-")
    label = "both" if lang == "both" else lang
    return f"biosci-radar-{stamp}-{label}.{suffix}"


def render_dashboard() -> str:
    return f"""<!doctype html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BioSci-Radar</title>
  <style>{CSS}</style>
</head>
<body>
  <header class="site-header">
    <div class="brand-block">
      <h1>BioSci-Radar</h1>
      <p id="subtitleLine" data-i18n="subtitle.empty">暂无本地数据</p>
    </div>
    <div class="toolbar">
      <div class="language-toggle" aria-label="Language">
        <button data-lang="zh" class="active">中文</button>
        <button data-lang="en">English</button>
      </div>
    </div>
  </header>
  <main>
    <section class="hero-band">
      <div class="hero-copy">
        <h2 class="hero-title" data-i18n="hero.title">BioSci-Radar</h2>
        <p class="hero-subtitle" data-i18n="hero.subtitle">面向生物信息学、多组学与可迁移 AI 方法的本地文献雷达</p>
        <div class="hero-actions">
          <button id="heroStartButton" class="primary" data-i18n="hero.start">开始检索</button>
          <button id="heroWorkspaceButton" data-i18n="hero.workspace">查看工作台</button>
        </div>
      </div>
      <div class="hero-seeds">
        <div class="section-label" data-i18n="hero.examples">示例关键词</div>
        <div class="seed-grid">
          <button class="seed-button" data-focus="LUAD, spatial transcriptomics">LUAD, spatial transcriptomics</button>
          <button class="seed-button" data-focus="single-cell multiomics, tumor microenvironment">single-cell multiomics, tumor microenvironment</button>
          <button class="seed-button" data-focus="graph neural network, omics integration">graph neural network, omics integration</button>
          <button class="seed-button" data-focus="foundation model, computational biology">foundation model, computational biology</button>
        </div>
      </div>
    </section>
    <section class="hero-info">
      <div class="capability-grid">
        <article class="capability-block">
          <div class="section-label" data-i18n="capability.sources.title">多源抓取</div>
          <p data-i18n="capability.sources.body">PubMed / bioRxiv / medRxiv / arXiv</p>
        </article>
        <article class="capability-block">
          <div class="section-label" data-i18n="capability.summary.title">频数可视化</div>
          <p data-i18n="capability.summary.body">关键词、主题、组学、疾病、算法标签</p>
        </article>
        <article class="capability-block">
          <div class="section-label" data-i18n="capability.workflow.title">本地工作流</div>
          <p data-i18n="capability.workflow.body">分页浏览、双语切换、Markdown 导出、Notion 同步</p>
        </article>
      </div>
      <div class="scenario-strip">
        <div class="section-label" data-i18n="scenario.title">适合场景</div>
        <div class="chips scenario-chips">
          <span data-i18n="scenario.multiomics">多组学应用</span>
          <span data-i18n="scenario.singlecell">单细胞/空间组学</span>
          <span data-i18n="scenario.methods">生信方法</span>
          <span data-i18n="scenario.ml">ML/DL 算法迁移</span>
        </div>
      </div>
      <button id="heroScrollCue" class="scroll-cue" data-i18n="hero.scrollCue">下滑进入工作台</button>
    </section>
    <section id="workspace" class="workspace-shell">
      <div class="workspace-head">
        <div>
          <div class="section-label" data-i18n="workspace.eyebrow">Workspace</div>
          <h2 class="workspace-title" data-i18n="workspace.title">Focused Fetch and Review</h2>
        </div>
        <nav>
          <button data-filter="all" class="active" data-i18n="filter.all">全部</button>
          <button data-filter="Bio Study" data-i18n="type.Bio Study">生物研究</button>
          <button data-filter="Bioinformatics Method" data-i18n="type.Bioinformatics Method">生信方法</button>
          <button data-filter="ML Algorithm" data-i18n="type.ML Algorithm">算法论文</button>
          <button data-filter="Dataset" data-i18n="type.Dataset">数据集</button>
        </nav>
      </div>
      <section class="panel controls">
        <div class="control-grid">
          <label class="field wide">
            <span data-i18n="field.focus">关键词</span>
            <input id="focusInput" type="text" data-placeholder-i18n="placeholder.focus" placeholder="spatial transcriptomics, LUAD, graph neural network">
          </label>
          <label class="field small">
            <span data-i18n="field.days">时间范围</span>
            <input id="daysInput" type="number" min="1" max="365" value="14">
          </label>
          <label class="field small">
            <span data-i18n="field.limit">每源数量</span>
            <input id="limitInput" type="number" min="5" max="200" value="60">
          </label>
          <button id="fetchButton" class="primary" data-i18n="action.fetch">抓取文献</button>
        </div>
        <div class="control-actions">
          <div class="export-group">
            <span class="export-label" data-i18n="action.exportLabel">导出汇总</span>
            <button id="exportZhButton" data-export-lang="zh" data-i18n="action.exportZh">导出中文</button>
            <button id="exportEnButton" data-export-lang="en" data-i18n="action.exportEn">Export English</button>
            <button id="exportBothButton" data-export-lang="both" data-i18n="action.exportBoth">双语 ZIP</button>
          </div>
          <span class="export-hint" data-i18n="action.exportHint">会同时写入 data/exports，并下载到浏览器。</span>
        </div>
        <p id="statusLine" class="status" data-i18n="status.ready">输入关键词后开始抓取，留空则按默认配置运行。</p>
      </section>
    </section>
    <section class="panel summary-panel">
      <div class="summary-header">
        <h2 data-i18n="summary.title">关键词与频数概览</h2>
        <div id="focusChips" class="chips"></div>
      </div>
      <div id="summaryGrid" class="summary-grid"></div>
    </section>
    <section class="panel list-panel">
      <div class="list-header">
        <h2 data-i18n="list.title">文献列表</h2>
        <div id="pagination" class="pagination"></div>
      </div>
      <div id="papersContainer" class="grid"></div>
    </section>
  </main>
  <script>{JS}</script>
</body>
</html>"""


ZH_LABELS = {
    "Bio Study": "生物研究",
    "Bioinformatics Method": "生信方法",
    "ML Algorithm": "算法论文",
    "Dataset": "数据集",
    "Review": "综述",
    "Unknown": "未知",
    "Custom Focus": "自定义关键词",
    "Bioinformatics Multi-omics": "生物信息学多组学",
    "Single-cell and Spatial Omics": "单细胞与空间组学",
    "Cancer Multi-omics": "肿瘤多组学",
    "Deep Learning for Omics": "组学深度学习",
    "Graph Learning for Biology": "生物图学习",
    "Foundation Models for Biology": "生物基础模型",
    "Multimodal Biomedical AI": "多模态医学 AI",
    "Survival and Clinical Prediction": "生存与临床预测",
    "bulk RNA-seq": "bulk RNA-seq",
    "scRNA-seq": "scRNA-seq",
    "scATAC-seq": "scATAC-seq",
    "spatial": "空间组学",
    "proteomics": "蛋白组学",
    "metabolomics": "代谢组学",
    "epigenomics": "表观组学",
    "microbiome": "微生物组",
    "cancer": "癌症",
    "lung cancer": "肺癌",
    "colorectal cancer": "结直肠癌",
    "breast cancer": "乳腺癌",
    "glioma": "胶质瘤",
    "immune": "免疫",
    "Transformer": "Transformer",
    "Foundation Model": "基础模型",
    "GNN": "图神经网络",
    "VAE": "VAE",
    "Contrastive": "对比学习",
    "Self-supervised": "自监督学习",
    "Diffusion": "扩散模型",
    "Survival": "生存模型",
    "Causal": "因果推断",
    "Multimodal": "多模态",
}


def zh_label(value: str) -> str:
    return ZH_LABELS.get(value, value)


def zh_reason(paper: Paper) -> str:
    parts: list[str] = []
    if paper.topics:
        parts.append("匹配方向：" + "、".join(zh_label(v) for v in paper.topics[:2]))
    if paper.omics_types:
        parts.append("涉及组学：" + "、".join(zh_label(v) for v in paper.omics_types[:3]))
    if paper.ml_areas:
        parts.append("算法相关：" + "、".join(zh_label(v) for v in paper.ml_areas[:3]))
    if paper.data_available:
        parts.append("提到公开数据")
    if paper.code_available:
        parts.append("提到代码")
    if not parts:
        parts.append("关键词弱匹配，可能仍值得快速浏览")
    return "；".join(parts)


CSS = """
:root {
  color-scheme: light;
  --bg: #f6f7f9;
  --panel: #ffffff;
  --text: #17202a;
  --muted: #64707d;
  --border: #dfe4ea;
  --accent: #1264a3;
  --green: #0c7a5b;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--text);
}
.site-header {
  position: sticky;
  top: 0;
  z-index: 4;
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 24px;
  padding: 22px 28px;
  background: rgba(246, 247, 249, 0.94);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(8px);
}
h1 { margin: 0 0 6px; font-size: 24px; letter-spacing: 0; }
.brand-block p { margin: 0; color: var(--muted); font-size: 13px; }
nav { display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
}
.language-toggle {
  display: flex;
  gap: 6px;
}
button {
  border: 1px solid var(--border);
  background: var(--panel);
  color: var(--text);
  border-radius: 6px;
  padding: 8px 10px;
  cursor: pointer;
}
button.active { border-color: var(--accent); color: var(--accent); }
button.primary {
  background: var(--accent);
  border-color: var(--accent);
  color: white;
}
button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}
input {
  width: 100%;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 10px 12px;
  font: inherit;
}
main {
  max-width: 1320px;
  margin: 0 auto;
  padding: 24px 28px 56px;
}
.hero-band {
  min-height: clamp(420px, 62vh, 620px);
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(320px, 0.95fr);
  gap: 28px;
  align-items: center;
  padding: 12px 0 16px;
}
.hero-copy {
  max-width: 720px;
}
.hero-title {
  margin: 0 0 14px;
  font-size: clamp(40px, 5.8vw, 64px);
  line-height: 1.02;
}
.hero-subtitle {
  margin: 0;
  max-width: 640px;
  font-size: 18px;
  line-height: 1.55;
  color: var(--muted);
}
.hero-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 28px;
}
.hero-seeds {
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--panel);
  padding: 18px;
}
.section-label {
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 12px;
}
.seed-grid {
  display: grid;
  gap: 10px;
}
.seed-button {
  width: 100%;
  text-align: left;
  min-height: 52px;
  padding: 12px 14px;
}
.hero-info {
  padding: 0 0 28px;
}
.capability-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}
.capability-block {
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--panel);
  padding: 16px;
}
.capability-block p {
  margin: 0;
  line-height: 1.5;
  color: var(--muted);
}
.scenario-strip {
  margin-top: 16px;
}
.scroll-cue {
  display: inline-flex;
  margin-top: 18px;
}
.workspace-shell {
  scroll-margin-top: 112px;
  padding-top: 22px;
}
.workspace-head {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: end;
  margin-bottom: 14px;
}
.workspace-title {
  margin: 0;
  font-size: 24px;
}
.panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 18px;
  margin-bottom: 16px;
}
.controls {
  position: sticky;
  top: 88px;
  z-index: 3;
}
.control-grid {
  display: grid;
  grid-template-columns: minmax(320px, 1.8fr) 120px 140px 140px;
  gap: 12px;
  align-items: end;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.field span,
.status,
.meta,
.authors,
.metric-label,
.metric-count,
details {
  color: var(--muted);
}
.status {
  margin: 12px 0 0;
  font-size: 13px;
}
.control-actions {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-top: 12px;
  flex-wrap: wrap;
}
.export-group {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.export-label,
.export-hint {
  color: var(--muted);
  font-size: 13px;
}
.summary-header,
.list-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: start;
  margin-bottom: 14px;
}
.summary-header h2,
.list-header h2 {
  margin: 0;
  font-size: 18px;
}
.summary-placeholder,
.empty-state {
  border: 1px dashed var(--border);
  border-radius: 8px;
  padding: 22px;
  color: var(--muted);
}
.summary-placeholder strong,
.empty-state strong {
  display: block;
  color: var(--text);
  margin-bottom: 8px;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}
.metric-card {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px;
}
.metric-list {
  display: grid;
  gap: 8px;
  margin-top: 10px;
}
.metric-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  align-items: center;
}
.metric-bar-wrap {
  grid-column: 1 / span 2;
  background: #eef2f5;
  border-radius: 999px;
  overflow: hidden;
}
.metric-bar {
  height: 6px;
  border-radius: 999px;
  background: linear-gradient(90deg, #1264a3, #47a89b);
}
.chips,
.tags,
.pagination {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}
.chips span,
.tags span {
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 3px 8px;
  font-size: 12px;
  color: var(--muted);
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 16px;
}
.card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 18px;
  min-height: 260px;
}
.paper-title {
  font-size: 18px;
  line-height: 1.3;
  margin: 0 0 8px;
}
.meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
  font-size: 12px;
}
.meta strong { color: var(--green); }
a { color: var(--text); text-decoration: none; }
a:hover { color: var(--accent); }
.authors { margin: 0 0 12px; font-size: 13px; }
.reason { margin: 0 0 14px; line-height: 1.45; }
details { font-size: 13px; }
details p { line-height: 1.5; }
@media (max-width: 760px) {
  .site-header { align-items: stretch; flex-direction: column; padding: 18px; }
  .toolbar { align-items: stretch; }
  nav { justify-content: flex-start; }
  main { padding: 18px; }
  .hero-band { min-height: unset; grid-template-columns: 1fr; padding-top: 8px; }
  .hero-title { font-size: 40px; }
  .capability-grid { grid-template-columns: 1fr; }
  .workspace-head { flex-direction: column; align-items: stretch; }
  .controls { position: static; }
  .control-grid { grid-template-columns: 1fr; }
  .control-actions { align-items: stretch; }
  .export-group { align-items: stretch; }
  .summary-header, .list-header { flex-direction: column; }
  .grid { grid-template-columns: 1fr; }
}
"""


JS = """
const translations = {
  zh: {
    'hero.title': 'BioSci-Radar',
    'hero.subtitle': '面向生物信息学、多组学与可迁移 AI 方法的本地文献雷达',
    'hero.start': '开始检索',
    'hero.workspace': '查看工作台',
    'hero.examples': '示例关键词',
    'hero.scrollCue': '下滑进入工作台',
    'workspace.eyebrow': '工作台',
    'workspace.title': '聚焦抓取与结果浏览',
    'filter.all': '全部',
    'type.Bio Study': '生物研究',
    'type.Bioinformatics Method': '生信方法',
    'type.ML Algorithm': '算法论文',
    'type.Dataset': '数据集',
    'type.Review': '综述',
    'capability.sources.title': '多源抓取',
    'capability.sources.body': 'PubMed / bioRxiv / medRxiv / arXiv',
    'capability.summary.title': '频数可视化',
    'capability.summary.body': '关键词、主题、组学、疾病、算法标签',
    'capability.workflow.title': '本地工作流',
    'capability.workflow.body': '分页浏览、双语切换、Markdown 导出、Notion 同步',
    'scenario.title': '适合场景',
    'scenario.multiomics': '多组学应用',
    'scenario.singlecell': '单细胞/空间组学',
    'scenario.methods': '生信方法',
    'scenario.ml': 'ML/DL 算法迁移',
    'label.score': '评分',
    'label.abstract': '摘要',
    'label.authors': '作者',
    'label.page': '页',
    'label.focusTerms': '当前关键词',
    'label.noFocus': '默认配置',
    'field.focus': '关键词',
    'field.days': '时间范围',
    'field.limit': '每源数量',
    'placeholder.focus': 'spatial transcriptomics, LUAD, graph neural network',
    'action.fetch': '抓取文献',
    'action.exportLabel': '导出汇总',
    'action.exportZh': '导出中文',
    'action.exportEn': '导出英文',
    'action.exportBoth': '双语 ZIP',
    'action.exportHint': '会同时写入 data/exports，并下载到浏览器。',
    'action.prev': '上一页',
    'action.next': '下一页',
    'status.ready': '输入关键词后开始抓取，留空则按默认配置运行。',
    'status.guided': '已跳转到工作台，可以直接输入或选择示例关键词。',
    'status.seed': '已使用示例关键词并开始抓取。',
    'status.loading': '正在抓取并汇总，请稍候。',
    'status.loaded': '已完成抓取与汇总。',
    'status.error': '抓取失败',
    'status.exporting': '正在导出 Markdown，请稍候。',
    'status.exported': '导出完成，已开始下载。',
    'status.exportError': '导出失败',
    'summary.title': '关键词与频数概览',
    'summary.sources': '来源频数',
    'summary.paper_types': '论文类型',
    'summary.topics': '方向频数',
    'summary.matched_keywords': '主要关键词',
    'summary.omics_types': '组学频数',
    'summary.ml_areas': '算法标签',
    'summary.diseases': '疾病标签',
    'list.title': '文献列表',
    'empty.noPapers': '当前配置下没有匹配论文。',
    'empty.fetchFirst': '请先点击示例关键词，或在工作台里输入关键词后抓取。',
    'empty.summaryTitle': '从欢迎页开始一次聚焦检索',
    'empty.summaryBody': '点击上方示例关键词，或切换到工作台输入你自己的主题。抓取完成后，这里会显示关键词、主题、组学、疾病和算法标签频数。',
    'empty.listTitle': '等待第一批结果',
    'empty.listBody': '本地工作台会在抓取完成后展示分页论文列表、摘要和标签。',
    'subtitle.empty': '暂无本地数据',
  },
  en: {
    'hero.title': 'BioSci-Radar',
    'hero.subtitle': 'A local literature radar for bioinformatics, multi-omics, and transferable AI methods',
    'hero.start': 'Start Exploring',
    'hero.workspace': 'Open Workspace',
    'hero.examples': 'Sample Keywords',
    'hero.scrollCue': 'Scroll to Workspace',
    'workspace.eyebrow': 'Workspace',
    'workspace.title': 'Focused Fetch and Review',
    'filter.all': 'All',
    'type.Bio Study': 'Bio Study',
    'type.Bioinformatics Method': 'Bioinformatics Method',
    'type.ML Algorithm': 'ML Algorithm',
    'type.Dataset': 'Dataset',
    'type.Review': 'Review',
    'capability.sources.title': 'Multi-source Fetch',
    'capability.sources.body': 'PubMed / bioRxiv / medRxiv / arXiv',
    'capability.summary.title': 'Frequency Views',
    'capability.summary.body': 'Keywords, topics, omics, disease, and ML tags',
    'capability.workflow.title': 'Local Workflow',
    'capability.workflow.body': 'Pagination, bilingual UI, Markdown export, and Notion sync',
    'scenario.title': 'Good For',
    'scenario.multiomics': 'Multi-omics studies',
    'scenario.singlecell': 'Single-cell / spatial omics',
    'scenario.methods': 'Bioinformatics methods',
    'scenario.ml': 'ML/DL transfer ideas',
    'label.score': 'score',
    'label.abstract': 'Abstract',
    'label.authors': 'Authors',
    'label.page': 'Page',
    'label.focusTerms': 'Current focus',
    'label.noFocus': 'Default profile',
    'field.focus': 'Keywords',
    'field.days': 'Window',
    'field.limit': 'Per source',
    'placeholder.focus': 'spatial transcriptomics, LUAD, graph neural network',
    'action.fetch': 'Fetch papers',
    'action.exportLabel': 'Export summary',
    'action.exportZh': 'Export Chinese',
    'action.exportEn': 'Export English',
    'action.exportBoth': 'Bilingual ZIP',
    'action.exportHint': 'This writes to data/exports and downloads the file in your browser.',
    'action.prev': 'Prev',
    'action.next': 'Next',
    'status.ready': 'Enter keywords to fetch, or leave blank to use the default profile.',
    'status.guided': 'You are in the workspace now. Enter your own focus or use a sample keyword.',
    'status.seed': 'Sample keywords selected. Fetching papers now.',
    'status.loading': 'Fetching papers and building summaries.',
    'status.loaded': 'Fetch completed.',
    'status.error': 'Fetch failed',
    'status.exporting': 'Exporting Markdown now.',
    'status.exported': 'Export completed. Download started.',
    'status.exportError': 'Export failed',
    'summary.title': 'Keyword and Frequency Overview',
    'summary.sources': 'Source Counts',
    'summary.paper_types': 'Paper Types',
    'summary.topics': 'Topic Counts',
    'summary.matched_keywords': 'Top Keywords',
    'summary.omics_types': 'Omics Tags',
    'summary.ml_areas': 'ML Tags',
    'summary.diseases': 'Disease Tags',
    'list.title': 'Paper List',
    'empty.noPapers': 'No papers matched your current configuration.',
    'empty.fetchFirst': 'Use a sample keyword above, or enter your own focus in the workspace.',
    'empty.summaryTitle': 'Start with a focused search',
    'empty.summaryBody': 'Click a sample keyword above, or move into the workspace and run your own fetch. Summary panels will appear here after the first run.',
    'empty.listTitle': 'Waiting for the first result set',
    'empty.listBody': 'The local workspace will show paginated papers, abstracts, and tags after a fetch completes.',
    'subtitle.empty': 'No local data yet',
  }
};

const zhLabels = {
  'Bio Study': '生物研究',
  'Bioinformatics Method': '生信方法',
  'ML Algorithm': '算法论文',
  'Dataset': '数据集',
  'Review': '综述',
  'Unknown': '未知',
  'Custom Focus': '自定义关键词',
  'Bioinformatics Multi-omics': '生物信息学多组学',
  'Single-cell and Spatial Omics': '单细胞与空间组学',
  'Cancer Multi-omics': '肿瘤多组学',
  'Deep Learning for Omics': '组学深度学习',
  'Graph Learning for Biology': '生物图学习',
  'Foundation Models for Biology': '生物基础模型',
  'Multimodal Biomedical AI': '多模态医学 AI',
  'Survival and Clinical Prediction': '生存与临床预测',
  'bulk RNA-seq': 'bulk RNA-seq',
  'scRNA-seq': 'scRNA-seq',
  'scATAC-seq': 'scATAC-seq',
  'spatial': '空间组学',
  'proteomics': '蛋白组学',
  'metabolomics': '代谢组学',
  'epigenomics': '表观组学',
  'microbiome': '微生物组',
  'cancer': '癌症',
  'lung cancer': '肺癌',
  'colorectal cancer': '结直肠癌',
  'breast cancer': '乳腺癌',
  'glioma': '胶质瘤',
  'immune': '免疫',
  'Foundation Model': '基础模型',
  'GNN': '图神经网络',
  'Contrastive': '对比学习',
  'Self-supervised': '自监督学习',
  'Diffusion': '扩散模型',
  'Survival': '生存模型',
  'Causal': '因果推断',
  'Multimodal': '多模态',
};

const filterButtons = document.querySelectorAll('button[data-filter]');
const langButtons = document.querySelectorAll('button[data-lang]');
const placeholderNodes = document.querySelectorAll('[data-placeholder-i18n]');
const seedButtons = document.querySelectorAll('.seed-button');
const focusInput = document.getElementById('focusInput');
const daysInput = document.getElementById('daysInput');
const limitInput = document.getElementById('limitInput');
const fetchButton = document.getElementById('fetchButton');
const exportButtons = document.querySelectorAll('[data-export-lang]');
const statusLine = document.getElementById('statusLine');
const subtitleLine = document.getElementById('subtitleLine');
const summaryGrid = document.getElementById('summaryGrid');
const focusChips = document.getElementById('focusChips');
const papersContainer = document.getElementById('papersContainer');
const pagination = document.getElementById('pagination');
const workspace = document.getElementById('workspace');
const heroStartButton = document.getElementById('heroStartButton');
const heroWorkspaceButton = document.getElementById('heroWorkspaceButton');
const heroScrollCue = document.getElementById('heroScrollCue');
const PAGE_SIZE = 10;

let currentLang = 'zh';
let activeFilter = 'all';
let currentPage = 1;
let currentData = null;

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    filterButtons.forEach((item) => item.classList.remove('active'));
    button.classList.add('active');
    activeFilter = button.dataset.filter;
    currentPage = 1;
    renderAll();
  });
});

langButtons.forEach((button) => {
  button.addEventListener('click', () => applyLanguage(button.dataset.lang));
});

fetchButton.addEventListener('click', async () => {
  await runFetch();
});

exportButtons.forEach((button) => {
  button.addEventListener('click', async () => {
    await runExport(button.dataset.exportLang || 'both');
  });
});

heroStartButton.addEventListener('click', () => {
  setStatus(translations[currentLang]['status.guided']);
  scrollToWorkspace(true);
});

heroWorkspaceButton.addEventListener('click', () => {
  scrollToWorkspace(false);
});

heroScrollCue.addEventListener('click', () => {
  scrollToWorkspace(false);
});

seedButtons.forEach((button) => {
  button.addEventListener('click', async () => {
    focusInput.value = button.dataset.focus || '';
    setStatus(translations[currentLang]['status.seed']);
    scrollToWorkspace(false);
    await runFetch();
  });
});

async function runFetch() {
  setStatus(translations[currentLang]['status.loading']);
  fetchButton.disabled = true;
  try {
    const response = await fetch('/api/fetch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        focus: focusInput.value,
        days: Number(daysInput.value || 14),
        limit: Number(limitInput.value || 60),
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Fetch failed');
    currentData = data;
    currentPage = 1;
    renderAll();
    setStatus(translations[currentLang]['status.loaded']);
  } catch (error) {
    setStatus(`${translations[currentLang]['status.error']}: ${error.message}`);
  } finally {
    fetchButton.disabled = false;
  }
}

async function runExport(lang) {
  setStatus(translations[currentLang]['status.exporting']);
  exportButtons.forEach((button) => { button.disabled = true; });
  try {
    const response = await fetch(`/api/export?lang=${encodeURIComponent(lang)}`);
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.error || 'Export failed');
    }
    const blob = await response.blob();
    const disposition = response.headers.get('Content-Disposition') || '';
    const match = disposition.match(/filename="([^"]+)"/);
    const filename = match ? match[1] : `biosci-radar-export.${lang === 'both' ? 'zip' : 'md'}`;
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    setStatus(translations[currentLang]['status.exported']);
  } catch (error) {
    setStatus(`${translations[currentLang]['status.exportError']}: ${error.message}`);
  } finally {
    exportButtons.forEach((button) => { button.disabled = false; });
  }
}

function scrollToWorkspace(shouldFocus) {
  workspace.scrollIntoView({ behavior: 'smooth', block: 'start' });
  if (shouldFocus) {
    window.setTimeout(() => focusInput.focus(), 420);
  }
}

function applyLanguage(lang) {
  currentLang = lang === 'en' ? 'en' : 'zh';
  document.documentElement.lang = currentLang;
  localStorage.setItem('biosciRadarLang', currentLang);
  langButtons.forEach((button) => button.classList.toggle('active', button.dataset.lang === currentLang));
  document.querySelectorAll('[data-i18n]').forEach((node) => {
    const key = node.dataset.i18n;
    node.textContent = translations[currentLang][key] || node.textContent;
  });
  placeholderNodes.forEach((node) => {
    const key = node.dataset.placeholderI18n;
    node.placeholder = translations[currentLang][key] || node.placeholder;
  });
  renderAll();
}

function setStatus(text) {
  statusLine.textContent = text;
}

function localLabel(value) {
  return currentLang === 'en' ? value : (zhLabels[value] || value);
}

function localReason(paper) {
  if (currentLang === 'en') return paper.why_relevant || '';
  const parts = [];
  if (paper.topics?.length) parts.push(`匹配方向：${paper.topics.slice(0, 2).map(localLabel).join('、')}`);
  if (paper.omics_types?.length) parts.push(`涉及组学：${paper.omics_types.slice(0, 3).map(localLabel).join('、')}`);
  if (paper.ml_areas?.length) parts.push(`算法相关：${paper.ml_areas.slice(0, 3).map(localLabel).join('、')}`);
  if (paper.data_available) parts.push('提到公开数据');
  if (paper.code_available) parts.push('提到代码');
  if (!parts.length) parts.push('关键词弱匹配，可能仍值得快速浏览');
  return parts.join('；');
}

function filteredPapers() {
  const papers = currentData?.papers || [];
  if (activeFilter === 'all') return papers;
  return papers.filter((paper) => paper.paper_type === activeFilter);
}

function renderAll() {
  renderSubtitle();
  renderSummary();
  renderPapers();
  renderPagination();
}

function renderSubtitle() {
  if (!currentData) {
    subtitleLine.textContent = translations[currentLang]['subtitle.empty'];
    return;
  }
  const sourceSummary = Object.entries(currentData.stats || {})
    .map(([name, count]) => `${name} ${count}`)
    .join(' · ');
  subtitleLine.textContent = currentLang === 'en'
    ? `Updated ${currentData.generated_at} · ${currentData.papers.length} papers · ${sourceSummary}`
    : `更新于 ${currentData.generated_at} · ${currentData.papers.length} 篇论文 · ${sourceSummary}`;
}

function renderSummary() {
  if (!currentData) {
    summaryGrid.innerHTML = `
      <section class="summary-placeholder">
        <strong>${translations[currentLang]['empty.summaryTitle']}</strong>
        <div>${translations[currentLang]['empty.summaryBody']}</div>
      </section>
    `;
    focusChips.innerHTML = `<span>${translations[currentLang]['label.noFocus']}</span>`;
    return;
  }
  const summary = currentData?.summary || {};
  const sections = [
    ['sources', 'summary.sources'],
    ['paper_types', 'summary.paper_types'],
    ['topics', 'summary.topics'],
    ['matched_keywords', 'summary.matched_keywords'],
    ['omics_types', 'summary.omics_types'],
    ['ml_areas', 'summary.ml_areas'],
    ['diseases', 'summary.diseases'],
  ];
  summaryGrid.innerHTML = sections.map(([key, titleKey]) => renderMetricCard(titleKey, summary[key] || [])).join('');
  const focusTerms = currentData?.focus_terms || [];
  if (!focusTerms.length) {
    focusChips.innerHTML = `<span>${translations[currentLang]['label.noFocus']}</span>`;
  } else {
    focusChips.innerHTML = `<span>${translations[currentLang]['label.focusTerms']}</span>` +
      focusTerms.map((term) => `<span>${escapeHtml(term)}</span>`).join('');
  }
}

function renderMetricCard(titleKey, items) {
  const title = translations[currentLang][titleKey];
  if (!items.length) {
    return `<article class="metric-card"><div class="metric-label">${title}</div><div class="metric-list"><div class="metric-label">${translations[currentLang]['empty.noPapers']}</div></div></article>`;
  }
  const max = items[0].count || 1;
  return `
    <article class="metric-card">
      <div class="metric-label">${title}</div>
      <div class="metric-list">
        ${items.map((item) => renderMetricRow(item, max)).join('')}
      </div>
    </article>
  `;
}

function renderMetricRow(item, max) {
  const width = Math.max(8, Math.round((item.count / max) * 100));
  return `
    <div class="metric-row">
      <div class="metric-label">${escapeHtml(localLabel(item.label))}</div>
      <div class="metric-count">${item.count}</div>
      <div class="metric-bar-wrap"><div class="metric-bar" style="width:${width}%"></div></div>
    </div>
  `;
}

function renderPapers() {
  if (!currentData) {
    papersContainer.innerHTML = `
      <section class="empty-state">
        <strong>${translations[currentLang]['empty.listTitle']}</strong>
        <div>${translations[currentLang]['empty.listBody']}</div>
      </section>
    `;
    return;
  }
  const papers = filteredPapers();
  if (!papers.length) {
    papersContainer.innerHTML = `<section class="empty-state">${translations[currentLang]['empty.noPapers']}</section>`;
    return;
  }
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageItems = papers.slice(start, start + PAGE_SIZE);
  papersContainer.innerHTML = pageItems.map(renderCard).join('');
}

function renderCard(paper) {
  const authors = (paper.authors || []).slice(0, 4).join(', ') + ((paper.authors || []).length > 4 ? ' et al.' : '');
  const tags = [...(paper.topics || []), ...(paper.omics_types || []), ...(paper.ml_areas || [])].slice(0, 8);
  return `
    <article class="card">
      <div class="meta">
        <strong>${escapeHtml(localLabel(paper.paper_type || 'Unknown'))}</strong>
        <span>${escapeHtml(paper.source || '')}</span>
        <span>${translations[currentLang]['label.score']} ${Number(paper.score || 0).toFixed(2)}</span>
      </div>
      <h3 class="paper-title"><a href="${escapeAttr(paper.url || '#')}" target="_blank" rel="noreferrer">${escapeHtml(paper.title || '')}</a></h3>
      <p class="authors">${translations[currentLang]['label.authors']}: ${escapeHtml(authors)}</p>
      <p class="reason">${escapeHtml(localReason(paper))}</p>
      <div class="tags">${tags.map((tag) => `<span>${escapeHtml(localLabel(tag))}</span>`).join('')}</div>
      <details>
        <summary>${translations[currentLang]['label.abstract']}</summary>
        <p>${escapeHtml(paper.abstract || 'No abstract available.')}</p>
      </details>
    </article>
  `;
}

function renderPagination() {
  if (!currentData) {
    pagination.innerHTML = '';
    return;
  }
  const total = filteredPapers().length;
  const pageCount = Math.max(1, Math.ceil(total / PAGE_SIZE));
  currentPage = Math.min(currentPage, pageCount);
  pagination.innerHTML = `
    <button id="prevPage" ${currentPage <= 1 ? 'disabled' : ''}>${translations[currentLang]['action.prev']}</button>
    <span>${translations[currentLang]['label.page']} ${currentPage} / ${pageCount}</span>
    <button id="nextPage" ${currentPage >= pageCount ? 'disabled' : ''}>${translations[currentLang]['action.next']}</button>
  `;
  document.getElementById('prevPage')?.addEventListener('click', () => {
    currentPage = Math.max(1, currentPage - 1);
    renderPapers();
    renderPagination();
  });
  document.getElementById('nextPage')?.addEventListener('click', () => {
    currentPage = Math.min(pageCount, currentPage + 1);
    renderPapers();
    renderPagination();
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll("'", '&#39;');
}

async function loadInitialData() {
  try {
    const response = await fetch('/api/papers');
    if (!response.ok) throw new Error('No local data');
    currentData = await response.json();
    if (currentData.days) daysInput.value = currentData.days;
    if (currentData.focus_terms?.length) focusInput.value = currentData.focus_terms.join(', ');
    renderAll();
  } catch {
    renderAll();
  }
}

applyLanguage(localStorage.getItem('biosciRadarLang') || 'zh');
loadInitialData();
"""
