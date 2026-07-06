# Shared Output Contract

Generated files are runtime artifacts. Keep source-controlled skill files in `skills/`, and write data products to `data/` or `outputs/` under the current working directory.

Raw JSON:

```text
data/raw/computer_vision/cvpr/{year}/cvpr_{year}_raw.json
```

Normalized JSON:

```text
data/normalized/computer_vision/cvpr/{year}/cvpr_{year}_normalized.json
```

Exports:

```text
outputs/computer_vision/cvpr/{year}/cvpr_{year}_papers.sqlite
outputs/computer_vision/cvpr/{year}/cvpr_{year}_papers.xlsx
outputs/computer_vision/cvpr/{year}/cvpr_{year}_papers.md
outputs/computer_vision/cvpr/{year}/cvpr_{year}_papers.json
outputs/computer_vision/cvpr/{year}/completeness_report.md
outputs/computer_vision/cvpr/{year}/failed_items.json
```

Existing files are backed up with `.bak.YYYYMMDDHHMMSS` before replacement.

Completeness reports must include a coverage summary:

- `total_papers`
- `abstract_coverage`
- `pdf_url_coverage`
- `supplementary_url_coverage`
- `paper_page_url_coverage`

Analysis outputs should be Markdown files under:

```text
outputs/computer_vision/cvpr/{year}/analysis/
```

Use templates from `skills/_shared/templates/` for paper notes, conference reports, and idea cards.
