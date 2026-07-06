# CVPR Routing And Operations

This file is always loaded by the `conference-cvpr` router.

## Workflow Detection

Use these routing rules:

- Requests like "获取 CVPR 2026 论文", "采集 CVPR 论文", "crawl CVPR papers" -> `collect-cvf`.
- Requests like "清洗 CVPR 数据", "统一字段", "normalize CVPR metadata" -> `normalize-metadata`.
- Requests like "导出 CVPR Excel", "生成 SQLite", "export CVPR papers" -> `export-artifacts`.
- Requests like "检查完整性", "缺失字段", "重复论文" -> `completeness-check`.
- Requests like "分析 CVPR 研究方向", "生成论文笔记", "研究灵感" -> `research-analysis`.
- Full pipeline/database requests -> `collect-cvf`, `normalize-metadata`, `export-artifacts`, `completeness-check`.

## Source Policy

Use CVF Open Access only in v1. Do not call OpenAlex, DBLP, Semantic Scholar, Papers With Code, GitHub Search, or other enrichment APIs.

Collect CVPR main conference papers only. Exclude workshops and tutorials.

Do not bulk download PDFs. Store `pdf_url` only.

## Output Policy

Produce files, not just prose, when a task asks for data, exports, reports, notes, or idea cards.

Default paths:

```text
data/raw/computer_vision/cvpr/{year}/cvpr_{year}_raw.json
data/normalized/computer_vision/cvpr/{year}/cvpr_{year}_normalized.json
outputs/computer_vision/cvpr/{year}/
outputs/computer_vision/cvpr/{year}/analysis/
```

Existing files are backed up before replacement.

## Failure Handling

- If `?day=all` fails or yields zero papers, fall back to dynamically discovered CVPR day links.
- Do not run per-paper page enrichment by default. Use `--enrich-pages` only when the user explicitly accepts the slower crawl to improve missing abstracts or related links.
- When using `--enrich-pages`, prefer `--limit`, `--sleep`, and `--resume` for staged runs instead of requesting every paper page at once.
- Treat low abstract coverage as a quality constraint: if analysis is requested and `abstract_coverage < 50%`, only produce a title-based preliminary scan.
- If a script fails, report the failing command and the relevant log path.
- If data is incomplete, still write artifacts and record issues in `completeness_report.md` and `failed_items.json`.
- If the user asks for a non-CVPR conference, state that v1 only supports CVPR and do not silently switch scope.
