# CVPR Core Workflow

Default full workflow:

1. `collect_cvpr.py`
2. `normalize_cvpr.py`
3. `export_cvpr.py`
4. `check_completeness.py`

## Collect

Input:

- `--year`
- optional `--output-dir`

Behavior:

- Fetch `https://openaccess.thecvf.com/CVPR{year}?day=all`.
- If it fails or yields zero papers, fetch `https://openaccess.thecvf.com/CVPR{year}` and discover day links dynamically.
- Do not hardcode day dates.
- Do not follow workshop or tutorial pages.
- Use `urljoin` for every URL.

## Normalize

Input:

- raw JSON
- `--year`
- optional `--output-dir`

Behavior:

- Clean title, authors, abstract, URLs.
- Add `conference=CVPR`, `field=computer_vision`, `source=cvf_openaccess`.
- Generate `paper_id` as `CVPR{year}_{index:06d}`.
- Keep enrichment fields empty in v1.

## Export

Output formats:

- SQLite table `papers`
- Excel
- Markdown
- JSON

## Check

Errors:

- Missing `title`
- Missing `authors`
- Missing `paper_page_url`
- Duplicate `title`

Warnings:

- Missing `abstract`
- Missing `pdf_url`
- Missing `supplementary_url`

## Analyze

Load `references/workflows/wf5-research-analysis.md` and the relevant shared template. Analysis must produce Markdown files under `outputs/computer_vision/cvpr/{year}/analysis/`; do not return only a conversational summary when the user asks for analysis artifacts.
