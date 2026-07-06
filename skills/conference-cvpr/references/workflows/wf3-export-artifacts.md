# WF3 — Export Artifacts

Use this workflow when the user asks to export CVPR papers, create Excel, create SQLite, make Markdown, or produce JSON deliverables.

## Inputs

- Normalized JSON from WF2, or a user-provided `--input-file`.
- `year`: required.

## Rules

- Read normalized JSON.
- Write SQLite, Excel, Markdown, and JSON.
- SQLite table name must be `papers`.
- Excel must include at least `title`, `authors`, `year`, `conference`, `abstract`, `pdf_url`, `paper_page_url`, `code_url`, `project_url`, `doi`, `citation_count`.
- Treat exports as runtime artifacts under `outputs/`, not as source files.
- Back up existing output files before replacement.

Read `../_shared/core/database-schema.md` and `../_shared/core/output-contract.md` when exact fields or paths matter.

## Execution

```bash
python skills/conference-cvpr/scripts/export_cvpr.py --year 2026
```

## Output

```text
outputs/computer_vision/cvpr/{year}/
```
