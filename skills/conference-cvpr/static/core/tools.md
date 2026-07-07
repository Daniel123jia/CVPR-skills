# CVPR Tool Inventory

This file is always loaded by the `conference-cvpr` router.

## Deterministic Scripts

Run scripts from the repository root or from the working directory where runtime artifacts should be written.

| Task | Script | Purpose |
| --- | --- | --- |
| full-pipeline | `scripts/run_pipeline.py` | Run collect, normalize, export, and completeness check in order |
| collect-cvf | `scripts/collect_cvpr.py` | Collect raw CVPR main-conference metadata from CVF Open Access |
| normalize-metadata | `scripts/normalize_cvpr.py` | Normalize raw CVF records into the shared paper schema |
| export-artifacts | `scripts/export_cvpr.py` | Export normalized JSON to SQLite, Excel, Markdown, and JSON |
| completeness-check | `scripts/check_completeness.py` | Generate completeness report and failed item list |
| download-cvf-pdf | `scripts/download_cvf_pdf.py` | Explicitly download selected CVF PDFs from local metadata |

普通用户优先使用 `run_pipeline.py`。高级用户需要重跑局部步骤、指定输入文件或调试单步问题时，再分别运行 `collect_cvpr.py`、`normalize_cvpr.py`、`export_cvpr.py`、`check_completeness.py`。

## Tool Selection

| User need | Workflow / script |
| --- | --- |
| 一键采集、清洗、导出、检查 | `full-pipeline` / `run_pipeline.py` |
| 采集 CVPR 论文 | `collect-cvf` / `collect_cvpr.py` |
| 补充摘要 | `collect_cvpr.py --enrich-pages` |
| 清洗字段 | `normalize-metadata` / `normalize_cvpr.py` |
| 导出 Excel/SQLite/Markdown/JSON | `export-artifacts` / `export_cvpr.py` |
| 检查缺失字段和重复论文 | `completeness-check` / `check_completeness.py` |
| 研究方向分析 | `research-analysis`; default does not call external APIs |
| 下载一篇指定 CVPR PDF | `download-cvf-pdf` / `download_cvf_pdf.py`; recommend `--dry-run` first |

## Command Pattern

Recommended full pipeline:

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

Advanced per-step commands:

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026
python skills/conference-cvpr/scripts/normalize_cvpr.py --year 2026
python skills/conference-cvpr/scripts/export_cvpr.py --year 2026
python skills/conference-cvpr/scripts/check_completeness.py --year 2026
```

The collection pipeline scripts support `--year`, `--output-dir`, and `--help`. Normalization, export, and checking also support `--input-file`.

Optional explicit single-paper download:

```bash
python skills/conference-cvpr/scripts/download_cvf_pdf.py \
  --metadata data/normalized/computer_vision/cvpr/2026/cvpr_2026_normalized.json \
  --paper-id CVPR2026_000002 \
  --output-dir outputs/computer_vision/cvpr/pdfs/2026 \
  --dry-run
```

Only exact `https://openaccess.thecvf.com/...pdf` URLs are allowed. Repeated `--paper-id` values require `--allow-batch`, explicit `--limit`, and explicit `--sleep`; never use batch mode by default.

`collect_cvpr.py` defaults to fast listing-page collection. This keeps full-conference runs quick but may leave many abstracts empty because CVF listing pages do not always expose abstracts.

Per-paper enrichment options:

- `--enrich-pages`: disabled by default; visits each `paper_page_url` to fill missing abstracts and related links.
- `--limit`: limits records written and per-paper enrichment attempts; useful for samples and staged enrichment.
- `--sleep`: waits between individual paper-page enrichment requests.
- `--resume`: reuses an existing raw JSON output when present, then optionally enriches and writes it again with backup.

Current `--limit` semantics: it limits both output record count and per-paper enrichment attempts. A future version may split this into `--limit-records` and `--enrich-limit`, but keep the current flag unchanged in v1 to avoid breaking the verified workflow.

For abstract-level analysis, prefer a staged command such as:

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

## Runtime Artifacts

The scripts write `data/`, `outputs/`, and `logs/` under the current working directory. These are runtime artifacts, not skill source files. PDF download results are runtime artifacts and must not be committed.
