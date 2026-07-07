# CVPR Tool Inventory

This file is always loaded by the `conference-cvpr` router.

Run scripts from the repository root. 普通用户优先使用 `run_pipeline.py`; run individual scripts only when rerunning a step, debugging, or using a custom input/output path.

## Deterministic Scripts

### `collect_cvpr.py`

| Field | Contract |
| --- | --- |
| Purpose | Collect raw CVPR main-conference metadata from CVF Open Access. |
| Typical command | `python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026` |
| Input | `--year`; optional `--output-dir`, `--limit`, `--enrich-pages`, `--sleep`, `--resume`. |
| Output | Raw JSON under `data/raw/computer_vision/cvpr/{year}/`. |
| Touches network? | Yes. It reads CVF Open Access HTML pages. |
| Downloads PDF? | No. It stores `pdf_url` only. |
| Runtime artifact policy | Raw JSON is a runtime artifact under ignored `data/`; do not commit it. |

### `normalize_cvpr.py`

| Field | Contract |
| --- | --- |
| Purpose | Normalize raw CVF records into the shared CVPR metadata schema. |
| Typical command | `python skills/conference-cvpr/scripts/normalize_cvpr.py --year 2026` |
| Input | Raw JSON from collection, or explicit `--input-file`. |
| Output | Normalized JSON under `data/normalized/computer_vision/cvpr/{year}/`. |
| Touches network? | No. |
| Downloads PDF? | No. |
| Runtime artifact policy | Normalized JSON is a runtime artifact under ignored `data/`; do not commit it. |

### `export_cvpr.py`

| Field | Contract |
| --- | --- |
| Purpose | Export normalized metadata to JSON, SQLite, Excel, and Markdown artifacts. |
| Typical command | `python skills/conference-cvpr/scripts/export_cvpr.py --year 2026` |
| Input | Normalized JSON, or explicit `--input-file`. |
| Output | `outputs/computer_vision/cvpr/{year}/cvpr_{year}_papers.json`, `.sqlite`, `.xlsx`, and Markdown files. |
| Touches network? | No. |
| Downloads PDF? | No. |
| Runtime artifact policy | Exports are runtime artifacts under ignored `outputs/`; do not commit JSON, SQLite, Excel, or Markdown exports unless explicitly curated as examples. |

### `check_completeness.py`

| Field | Contract |
| --- | --- |
| Purpose | Check missing fields, duplicate titles, URL coverage, and completeness warnings. |
| Typical command | `python skills/conference-cvpr/scripts/check_completeness.py --year 2026` |
| Input | Normalized JSON, or explicit `--input-file`. |
| Output | Completeness report and failed-items JSON under `outputs/computer_vision/cvpr/{year}/`. |
| Touches network? | No. |
| Downloads PDF? | No. |
| Runtime artifact policy | Reports are runtime artifacts under ignored `outputs/`; keep generated reports out of Git unless promoted to fixtures/examples intentionally. |

### `run_pipeline.py`

| Field | Contract |
| --- | --- |
| Purpose | Run collect, normalize, export, and completeness check in order. |
| Typical command | `python skills/conference-cvpr/scripts/run_pipeline.py --year 2026 --limit 5` |
| Input | `--year`; optional collection/enrichment flags such as `--limit`, `--enrich-pages`, `--sleep`, and `--resume`. |
| Output | Raw JSON, normalized JSON, exported artifacts, and completeness reports. |
| Touches network? | Yes, because the collect step reads CVF Open Access. |
| Downloads PDF? | No. The pipeline never downloads PDFs. |
| Runtime artifact policy | Pipeline outputs go to ignored `data/`, `outputs/`, and `logs/`; do not commit them. |

### `download_cvf_pdf.py`

| Field | Contract |
| --- | --- |
| Purpose | Explicitly validate and optionally download selected CVF Open Access PDFs by `paper_id`, title, or direct `pdf_url`. |
| Typical command | `python skills/conference-cvpr/scripts/download_cvf_pdf.py --metadata outputs/computer_vision/cvpr/2026/cvpr_2026_papers.json --paper-id CVPR2026_000002 --output-dir outputs/computer_vision/cvpr/pdfs/2026 --dry-run` |
| Input | Local metadata JSON plus `--paper-id` or `--title`, or direct `--pdf-url` with `--paper-id`. |
| Output | Dry-run plan, or selected PDF plus `.pdf.json` sidecar and checksum metadata under `outputs/computer_vision/cvpr/pdfs/{year}/`. |
| Touches network? | No in `--dry-run`; yes only when a real download is requested. |
| Downloads PDF? | No in `--dry-run`; yes only for explicit selected CVF Open Access PDF URLs. |
| Runtime artifact policy | PDF download results are runtime artifacts and must not be committed. |

## Tool Selection

| User need | Workflow / script |
| --- | --- |
| 一键采集、清洗、导出、检查 | `collect-cvf -> normalize-metadata -> export-artifacts -> completeness-check` / `run_pipeline.py` |
| 采集 CVPR metadata | `collect-cvf` / `collect_cvpr.py` |
| 补充摘要 | `collect_cvpr.py --enrich-pages` with `--limit`, `--sleep`, and `--resume` |
| 清洗字段 | `normalize-metadata` / `normalize_cvpr.py` |
| 导出 Excel/SQLite/Markdown/JSON | `export-artifacts` / `export_cvpr.py` |
| 检查缺失字段和重复论文 | `completeness-check` / `check_completeness.py` |
| metadata-level 研究方向分析 | `research-analysis`; never claim full-paper findings |
| 下载一篇指定 CVPR PDF | `download-cvf-pdf` / `download_cvf_pdf.py`; recommend `--dry-run` first |

## Command Patterns

Recommended sample pipeline:

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026 --limit 5
```

Cautious abstract enrichment:

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

Advanced per-step commands:

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026
python skills/conference-cvpr/scripts/normalize_cvpr.py --year 2026
python skills/conference-cvpr/scripts/export_cvpr.py --year 2026
python skills/conference-cvpr/scripts/check_completeness.py --year 2026
```

Optional explicit single-paper download:

```bash
python skills/conference-cvpr/scripts/download_cvf_pdf.py \
  --metadata outputs/computer_vision/cvpr/2026/cvpr_2026_papers.json \
  --paper-id CVPR2026_000002 \
  --output-dir outputs/computer_vision/cvpr/pdfs/2026 \
  --dry-run
```

Only exact `https://openaccess.thecvf.com/...pdf` URLs are allowed. Repeated `--paper-id` values require `--allow-batch`, explicit `--limit`, and explicit `--sleep`; never use batch mode by default.

Current `--limit` semantics: it limits both output record count and per-paper enrichment attempts. Keep the current flag unchanged in v1 to avoid breaking the verified workflow.

## Handoff Tools

`conference-cvpr` does not own fulltext extraction or reader-note indexing.

- Use `cvpr-paper-reader` when the next step is local PDF text extraction, full-paper reading, method extraction, experiment extraction, or paper reading notes.
- Use `cvpr-idea-miner` when the next step is collecting reader notes, topic maps, gap analysis, idea cards, or experiment plans.

Relevant downstream helper scripts:

```text
skills/cvpr-paper-reader/scripts/extract_pdf_text.py
skills/cvpr-idea-miner/scripts/collect_reader_notes.py
```

## Runtime Artifacts

The scripts write `data/`, `outputs/`, and `logs/` under the current working directory. These are runtime artifacts, not skill source files. PDF download results are runtime artifacts and must not be committed.
