# CVPR Tool Inventory

This file is always loaded by the `conference-cvpr` router.

## Deterministic Scripts

Run scripts from the repository root or from the working directory where runtime artifacts should be written.

| Task | Script | Purpose |
| --- | --- | --- |
| collect-cvf | `scripts/collect_cvpr.py` | Collect raw CVPR main-conference metadata from CVF Open Access |
| normalize-metadata | `scripts/normalize_cvpr.py` | Normalize raw CVF records into the shared paper schema |
| export-artifacts | `scripts/export_cvpr.py` | Export normalized JSON to SQLite, Excel, Markdown, and JSON |
| completeness-check | `scripts/check_completeness.py` | Generate completeness report and failed item list |

## Command Pattern

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026
python skills/conference-cvpr/scripts/normalize_cvpr.py --year 2026
python skills/conference-cvpr/scripts/export_cvpr.py --year 2026
python skills/conference-cvpr/scripts/check_completeness.py --year 2026
```

Every script supports `--year`, `--output-dir`, and `--help`. Normalization, export, and checking also support `--input-file`.

`collect_cvpr.py` defaults to fast listing-page collection. This keeps full-conference runs quick but may leave many abstracts empty because CVF listing pages do not always expose abstracts.

Per-paper enrichment options:

- `--enrich-pages`: disabled by default; visits each `paper_page_url` to fill missing abstracts and related links.
- `--limit`: limits records written and per-paper enrichment attempts; useful for samples and staged enrichment.
- `--sleep`: waits between individual paper-page enrichment requests.
- `--resume`: reuses an existing raw JSON output when present, then optionally enriches and writes it again with backup.

For abstract-level analysis, prefer a staged command such as:

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

## Runtime Artifacts

The scripts write `data/`, `outputs/`, and `logs/` under the current working directory. These are runtime artifacts, not skill source files.
