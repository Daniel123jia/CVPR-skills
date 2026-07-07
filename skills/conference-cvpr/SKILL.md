---
name: conference-cvpr
description: Use when a user asks to collect CVPR metadata, normalize metadata, export artifacts, check completeness, run metadata-level research analysis, or perform optional explicit CVF PDF download for selected CVPR main-conference papers from CVF Open Access.
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
- `download-cvf-pdf`

Download routing examples include: "download CVPR PDF", "download CVF PDF", "download this CVPR paper", "get PDF from CVF metadata", "paper_id to PDF", and "title to PDF".

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

Produce directly usable metadata files, exports, completeness reports, metadata-level analysis reports, or explicit PDF download plans/results. Do not answer with only explanations when the user asks for collection, export, checking, metadata reports, or selected-paper CVF PDF download.

### 4.1 Handoff Boundaries

Do not treat fulltext paper reading, method extraction, experiment extraction, or paper-level idea generation as direct `conference-cvpr` responsibilities.

If the user asks to read a CVPR paper, summarize a full paper, extract methods or experiments, or create paper-level reading notes from PDF text, hand off to `cvpr-paper-reader`.

If the user asks to generate idea cards, gap analysis, topic maps, or experiment plans from reader notes or fulltext-derived notes, hand off to `cvpr-idea-miner`.

### 5. Respect V1 Scope

Support CVPR main conference papers only. Do not collect CVPR workshops or tutorials. Do not support ICCV, ECCV, NeurIPS, ICML, ACL, AAAI, IJCAI, or other conferences in v1.

Use CVF Open Access as the only live source. Do not call OpenAlex, DBLP, Semantic Scholar, Papers With Code, GitHub Search, or other external enrichment APIs in v1.

Default collection stores `pdf_url` only. PDF download is optional and explicit. Do not automatically or bulk download PDFs, and do not run automatic full-conference PDF download. Run `download-cvf-pdf` only after an explicit user request identifies selected papers by `paper_id`, title, or an allowed CVF Open Access PDF URL.

Recommend `--dry-run` before any real download. Downloaded PDFs, sidecar JSON, checksums, and logs are runtime artifacts and must not be committed.

## Completion Check

Before reporting success after modifying this skill, run:

```bash
python -m unittest discover -s tests
python skills/conference-cvpr/scripts/collect_cvpr.py --help
python skills/conference-cvpr/scripts/normalize_cvpr.py --help
python skills/conference-cvpr/scripts/export_cvpr.py --help
python skills/conference-cvpr/scripts/check_completeness.py --help
python skills/conference-cvpr/scripts/run_pipeline.py --help
python skills/conference-cvpr/scripts/download_cvf_pdf.py --help
```
