# WF1 — Collect CVF

Use this workflow when the user asks to get, collect, crawl, fetch, or build CVPR paper data.

## Inputs

- `year`: required, for example `2026`.
- Optional `--output-dir` when the user wants raw JSON somewhere other than the default runtime path.
- Optional `--enrich-pages` only when the user explicitly wants slower per-paper page enrichment.
- Optional `--limit`, `--sleep`, and `--resume` for cautious staged enrichment or sampled runs.

## Source Rules

- Collect CVPR main conference papers only.
- Use CVF Open Access as the only source.
- First request `https://openaccess.thecvf.com/CVPR{year}?day=all`.
- If that fails or returns no papers, request `https://openaccess.thecvf.com/CVPR{year}` and discover day links dynamically.
- Do not hardcode day dates.
- Exclude workshop and tutorial pages.
- Use `urljoin` for every URL.
- Do not download PDF files.
- Do not fetch every individual paper page by default. Use `--enrich-pages` only for an explicit enrichment run.
- Default fast mode primarily collects fields visible on CVF listing pages; `abstract` may be mostly empty.
- `--enrich-pages` visits each `paper_page_url` to fill missing abstracts and related links.
- Use `--limit`, `--sleep`, and `--resume` to avoid a single run requesting thousands of individual paper pages.

Read `references/cvf-openaccess.md` or `references/cvpr-year-patterns.md` only when CVF parsing or year routing needs clarification.

## Execution

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026
```

Slow enrichment mode:

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

## Output

```text
data/raw/computer_vision/cvpr/{year}/cvpr_{year}_raw.json
```

Existing output is backed up before replacement.
