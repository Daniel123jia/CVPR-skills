# WF4 — Completeness Check

Use this workflow when the user asks to audit, verify, inspect completeness, or validate CVPR outputs.

## Inputs

- Normalized JSON from WF2, or a user-provided `--input-file`.
- `year`: required.

## Checks

Coverage summary:

- `total_papers`
- `abstract_coverage`
- `pdf_url_coverage`
- `supplementary_url_coverage`
- `paper_page_url_coverage`

Errors:

- Missing `title`
- Missing `authors`
- Missing `paper_page_url`
- Duplicate `title`

Warnings:

- Missing `abstract`
- Missing `pdf_url`
- Missing `supplementary_url`

Read `../_shared/core/dedup-rules.md` when duplicate behavior needs clarification.

## Execution

```bash
python skills/conference-cvpr/scripts/check_completeness.py --year 2026
```

## Output

```text
outputs/computer_vision/cvpr/{year}/completeness_report.md
outputs/computer_vision/cvpr/{year}/failed_items.json
```
