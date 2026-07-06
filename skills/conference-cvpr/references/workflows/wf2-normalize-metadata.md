# WF2 — Normalize Metadata

Use this workflow when the user asks to clean, normalize, standardize, or prepare collected CVPR data.

## Inputs

- Raw JSON from WF1, or a user-provided `--input-file`.
- `year`: required.

## Rules

- Read raw JSON.
- Clean title, authors, abstract, and URLs.
- Add `conference=CVPR`, `field=computer_vision`, `source=cvf_openaccess`.
- Generate stable `paper_id` as `CVPR{year}_{index:06d}`.
- Preserve reserved fields with empty values: `doi`, `citation_count`, `code_url`, `project_url`, `openalex_id`, `semantic_scholar_id`, `dblp_key`.

Read `../_shared/core/metadata-schema.md` when field-level details are needed.

## Execution

```bash
python skills/conference-cvpr/scripts/normalize_cvpr.py --year 2026
```

## Output

```text
data/normalized/computer_vision/cvpr/{year}/cvpr_{year}_normalized.json
```

Existing output is backed up before replacement.
