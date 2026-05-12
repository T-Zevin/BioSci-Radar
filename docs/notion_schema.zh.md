# Notion 字段建议

创建一个名为 `Papers` 的 Notion 数据库，并把它分享给你的 Notion integration。

推荐字段如下：

| 字段 | 类型 | 用途 |
|---|---|---|
| Title | Title | 论文标题 |
| Status | Select | New, To Read, Reading, Read, Useful, Ignore |
| Priority | Select | High, Medium, Low |
| Score | Number | 综合推荐分 |
| Paper Type | Select | Bio Study, Bioinformatics Method, ML Algorithm, Review, Dataset |
| Source | Select | PubMed, bioRxiv, medRxiv, arXiv |
| Year | Number | 发表年份 |
| Published | Date | 发表日期 |
| URL | URL | 来源链接 |
| DOI | Rich text | DOI |
| PMID | Rich text | PubMed ID |
| Omics Type | Multi-select | scRNA, scATAC, spatial, proteomics, metabolomics, microbiome 等 |
| Disease | Multi-select | LUAD, cancer, tumor, immune 等 |
| ML Area | Multi-select | GNN, Transformer, VAE, SSL, Contrastive, Survival, Causal, Foundation Model |
| Topics | Multi-select | 命中的研究方向 |
| Code Available | Checkbox | 是否提到代码 |
| Data Available | Checkbox | 是否提到公开数据 |
| Transfer Potential | Select | High, Medium, Low |
| Reproducibility | Select | High, Medium, Low, Unknown |
| Why Relevant | Rich text | 推荐理由 |
| Abstract | Rich text | 来源摘要 |

同步命令会按这些字段创建 Notion 页面。第一版建议字段名保持英文且完全一致，因为 Notion API 会按字段名匹配。
