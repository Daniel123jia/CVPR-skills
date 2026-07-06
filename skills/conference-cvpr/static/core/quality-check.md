# CVPR Quality Check

Use this file before reporting task completion.

## Data Quality

Errors:

- Missing `title`
- Missing `authors`
- Missing `paper_page_url`
- Duplicate normalized `title`

Warnings:

- Missing `abstract`
- Missing `pdf_url`
- Missing `supplementary_url`

Coverage summary must be included in `completeness_report.md`:

- `total_papers`
- `abstract_coverage`
- `pdf_url_coverage`
- `supplementary_url_coverage`
- `paper_page_url_coverage`

## Artifact Quality

- Output files must exist at the requested or default paths.
- Existing outputs must be backed up before replacement.
- SQLite export must contain table `papers`.
- Excel export must include at least `title`, `authors`, `year`, `conference`, `abstract`, `pdf_url`, `paper_page_url`, `code_url`, `project_url`, `doi`, `citation_count`.
- Analysis outputs must be Markdown files and cite the input dataset or paper rows they used.
- Analysis must compute `abstract_coverage` before drawing conclusions; if it is below 50%, output only a title-based preliminary scan.

## Scope Quality

- Do not include workshop papers.
- Do not call external enrichment APIs in v1.
- Do not download PDFs in bulk.
