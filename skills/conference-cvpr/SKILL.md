---
name: conference-cvpr
description: CVPR Agent Skill for collecting, normalizing, exporting, checking, reading, analyzing, and generating research ideas from CVPR main-conference papers. Use when the user asks 获取 CVPR 2026 论文, 采集 CVPR 论文, 构建 CVPR 数据库, 导出 CVPR 论文 Excel, 分析 CVPR 研究方向, read CVPR papers, summarize CVPR trends, or generate CVPR research ideas. First version only supports CVPR main conference papers from CVF Open Access; it excludes workshops, external APIs, and PDF downloading.
---

# Conference CVPR — Router

This skill is split into two layers:

- A static core layer under `static/core/` for tool inventory, routing, source policy, output policy, and quality rules.
- A workflow layer under `references/workflows/` for concrete task procedures.

Do not apply CVPR collection or analysis logic from memory. Use this router to load the right fragments.

## Routing Protocol

Follow these steps every time the skill is invoked.

### 1. Load The Manifest And Core Layer

Read `manifest.yaml`.

Read every file listed under `always_load`:

- `static/core/tools.md`
- `static/core/routing-and-ops.md`

### 2. Detect the workflow

Map the user request to one or more workflow values from `manifest.yaml`:

- `collect-cvf`
- `normalize-metadata`
- `export-artifacts`
- `completeness-check`
- `research-analysis`

Combined requests can require multiple workflows. A full "获取/采集/构建 CVPR 数据库" request defaults to:

```text
collect-cvf -> normalize-metadata -> export-artifacts -> completeness-check
```

State the detected workflow(s) in one short line before running them.

### 3. Load the matching workflow fragment

Load only the workflow files mapped in `manifest.yaml` under `axes.workflow.values`. The workflow files live in `references/workflows/`.

Do not read every workflow by default.

### 4. Run The Workflow

Apply loaded material in this order:

1. Core tools and routing from `static/core/tools.md` and `static/core/routing-and-ops.md`.
2. The selected workflow fragment(s) from `references/workflows/`.
3. Shared schema, taxonomy, templates, or references on demand from the manifest.
4. Deterministic scripts in `scripts/` when collection, normalization, export, or checking is required.

Produce directly usable files. Do not answer with only explanations when the user asks for collection, export, checking, reading notes, conference reports, or idea cards.

### 5. Respect V1 Scope

Support CVPR main conference papers only. Do not collect CVPR workshops or tutorials. Do not support ICCV, ECCV, NeurIPS, ICML, ACL, AAAI, IJCAI, or other conferences in v1.

Use CVF Open Access as the only live source. Do not call OpenAlex, DBLP, Semantic Scholar, Papers With Code, GitHub Search, or other external enrichment APIs in v1.

Do not bulk download PDFs. Store `pdf_url` only.

## Completion Check

Before reporting success after modifying this skill, run:

```bash
python -m unittest discover -s tests
python skills/conference-cvpr/scripts/collect_cvpr.py --help
python skills/conference-cvpr/scripts/normalize_cvpr.py --help
python skills/conference-cvpr/scripts/export_cvpr.py --help
python skills/conference-cvpr/scripts/check_completeness.py --help
```
