---
name: cvpr-paper-reader
description: Use when the user asks to read, summarize, deeply analyze, extract methods, extract experiments, find limitations, generate ideas, or create Chinese reading notes for a single or small number of CVPR papers from paper text, local PDF, CVF paper page, pasted content, or conference-cvpr metadata. Triggers include 精读这篇 CVPR 论文, 帮我读这篇 CVPR paper, 总结这篇 CVPR 论文, 提取这篇论文的方法, 整理实验设置和结果, 生成论文阅读笔记, 从这篇 CVPR 论文找研究灵感, CVPR paper reader, and read CVPR paper.
---

# CVPR Paper Reader — Router

This is a router for single-paper or small-batch CVPR reading workflows. It is not a conference-level collector.

Use `conference-cvpr` for whole-year CVPR collection, export, completeness checks, and conference-level preliminary analysis. Use this skill for paper-level reading artifacts only.

## Routing Protocol

Follow these steps every time this skill is invoked.

### 1. Load The Manifest And Core Layer

Read `manifest.yaml`.

Read every file listed under `always_load`.

### 2. Determine Evidence Level

Apply `static/core/evidence-policy.md` before analyzing content.

Do not invent methods, experiments, datasets, results, or conclusions when the paper body or abstract is unavailable. If the user provides only a title, produce a scope warning and title-level orientation only.

### 3. Detect The Workflow

Detect one or more workflow values from `manifest.yaml`:

- `paper-summary`
- `method-extraction`
- `experiment-table`
- `limitations-and-ideas`
- `reading-note`

Combined requests can require multiple workflows. A complete "精读/生成完整阅读笔记" request defaults to:

```text
paper-summary -> method-extraction -> experiment-table -> limitations-and-ideas -> reading-note
```

State the detected workflow(s) in one short line before running them.

### 4. Load Only Needed Workflow Fragments

Load only the matching workflow fragments from `references/workflows/` using the mapping in `manifest.yaml`.

Do not read every workflow by default.

### 5. Produce Files

Output must be a directly usable Markdown file, or a small set of Markdown files, under the output path defined in `static/core/output-contract.md`. Do not answer with only an oral explanation when the user asks for reading, extraction, summaries, tables, notes, or ideas.

### 6. Respect Scope

Only handle CVPR papers. Do not add other conferences. Do not run whole-conference collection. Do not call OpenAlex, Semantic Scholar, DBLP, Papers With Code, GitHub Search, or similar external enrichment APIs. Do not batch download PDFs. Do not do OCR.

## Optional Script

For local PDFs, use the optional helper only when the user provides a local PDF path:

```bash
python skills/cvpr-paper-reader/scripts/extract_pdf_text.py --pdf path/to/paper.pdf --output outputs/computer_vision/cvpr/reader/{paper_id}/paper_text.md
```

The script extracts text only. It does not perform OCR.

## Completion Check

Before reporting success after modifying this skill, run:

```bash
python -m unittest discover -s tests
python skills/cvpr-paper-reader/scripts/extract_pdf_text.py --help
python skills/conference-cvpr/scripts/run_pipeline.py --help
```
