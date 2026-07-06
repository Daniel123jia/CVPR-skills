# CVPR Output Contract

All paths are relative to the current working directory where the skill tool is run.

Raw:

```text
data/raw/computer_vision/cvpr/{year}/cvpr_{year}_raw.json
```

Normalized:

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

Every write creates parent directories automatically. Existing files are backed up before replacement.

`completeness_report.md` must include a coverage summary:

- `total_papers`
- `abstract_coverage`
- `pdf_url_coverage`
- `supplementary_url_coverage`
- `paper_page_url_coverage`
