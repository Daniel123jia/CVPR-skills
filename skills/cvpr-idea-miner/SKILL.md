---
name: cvpr-idea-miner
description: Use when the user asks to generate research ideas, topic maps, research gaps, method recombinations, idea cards, future work, or experiment plans from multiple CVPR papers, CVPR paper metadata, cvpr-paper-reader notes, or CVPR conference reports. Triggers include 从这些 CVPR 论文找研究灵感, 分析 CVPR 研究空白, 根据这些阅读笔记生成 idea, CVPR topic map, 从 CVPR 2026 中找可做的研究方向, research idea from CVPR papers, and CVPR idea miner.
---

# CVPR Idea Miner — Router

This is a Router for multi-paper CVPR research idea mining. It is not a whole-conference collector and not a single-paper PDF reader.

Use `conference-cvpr` for whole-year CVPR collection, cleaning, export, completeness checks, and conference-level entry data. Use `cvpr-paper-reader` for single-paper or small-batch reading artifacts. Use this skill only after multiple CVPR papers, metadata records, reading notes, or conference reports are available.

## Routing Protocol

Follow these steps every time this skill is invoked.

### 1. Load The Manifest And Core Layer

Read `manifest.yaml`.

Read every file listed under `always_load`.

### 2. Determine Evidence Level

Apply `static/core/evidence-policy.md` before generating analysis or ideas.

If the user provides no paper body, abstract, or reading notes, produce only title-level preliminary analysis. Do not invent methods, experiments, datasets, results, or conclusions.

### 3. Detect The Workflow

Detect one or more workflow values from `manifest.yaml`:

- `topic-map`
- `gap-analysis`
- `method-recombination`
- `idea-cards`
- `experiment-plan`

Combined requests can require multiple workflows. A complete "生成研究方向/idea/实验计划" request defaults to:

```text
topic-map -> gap-analysis -> method-recombination -> idea-cards -> experiment-plan
```

State the detected workflow(s) in one short line before running them.

### 4. Load Only Needed Workflow Fragments

Load only the matching workflow fragments from `references/workflows/` using the mapping in `manifest.yaml`.

Do not read every workflow by default.

### 5. Produce Files

Output must be a directly usable Markdown file, or a small set of Markdown files, under the output path defined in `static/core/output-contract.md`. Do not answer with only an oral explanation when the user asks for topic maps, gap analysis, method recombination, idea cards, future work, or experiment plans.

### 6. Respect Scope

Only handle CVPR main conference paper inputs and CVPR-derived reading notes. Do not add other conferences. Do not run whole-conference collection. Do not call OpenAlex, Semantic Scholar, DBLP, Papers With Code, GitHub Search, or similar external enrichment APIs. Do not batch download PDFs. Do not do OCR.

## Optional Script

To collect local `cvpr-paper-reader` note paths into a JSON index:

```bash
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py --input-dir outputs/computer_vision/cvpr/reader --output outputs/computer_vision/cvpr/ideas/reader_notes_index.json
```

The script scans local Markdown notes only. It does not call external APIs, download PDFs, or perform OCR.

If a reader directory contains optional `reproduction_checklist.md`, the index
records it as `files.reproduction_checklist`. Use it only as an evidence source
for feasibility fields and experiment planning; missing code or hyperparameters
remain evidence gaps. Its absence does not block idea mining.

For a single-paper fulltext validation case, prefer filtering to avoid mixing
historical title-only, abstract-only, and fulltext samples:

```bash
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py \
  --selected-root outputs/computer_vision/cvpr/reader/directfisheye_gs_fulltext_test \
  --min-evidence-level fulltext \
  --dedupe-title prefer_highest_evidence \
  --output outputs/computer_vision/cvpr/ideas/directfisheye_gs_fulltext_test/reader_notes_index.json
```

`--selected-root` automatically infers the parent `input_dir`. Use
`--input-dir` for whole-reader-root scans; passing both flags remains supported.

If the same paper appears at multiple evidence levels, prefer
`--dedupe-title prefer_highest_evidence`. If `input_count < 3`, topic maps must
be labeled as single-paper or local topic maps based on selected notes, not as a
CVPR trend.

## Completion Check

Before reporting success after modifying this skill, run:

```bash
python -m unittest discover -s tests
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py --help
python skills/cvpr-paper-reader/scripts/extract_pdf_text.py --help
python skills/conference-cvpr/scripts/run_pipeline.py --help
```
