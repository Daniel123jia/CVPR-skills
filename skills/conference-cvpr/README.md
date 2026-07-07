# conference-cvpr

CVPR Agent Skill for Codex / Claude Code.

只使用 CVF Open Access 作为主数据源，采集 CVPR main conference papers，不采集 workshops，不接 OpenAlex、DBLP、Semantic Scholar 等外部 API。默认流程只保存 `pdf_url`；v1.5 另提供 optional PDF download，且必须由用户显式选择论文后触发。

## Workflow Axis

`SKILL.md` 是 router。它先读取 `manifest.yaml` 和 `always_load` 中的核心文件，再按用户意图加载 `references/workflows/` 下的 workflow 片段。

- `collect-cvf`: 采集 CVPR main conference papers
- `normalize-metadata`: 清洗并统一 metadata schema
- `export-artifacts`: 输出 SQLite、Excel、Markdown、JSON
- `completeness-check`: 生成 completeness report 和 failed items
- `research-analysis`: 基于 normalized/exported 数据生成论文阅读笔记、会议报告、研究灵感卡片
- `download-cvf-pdf`: 从本地 metadata 中显式下载指定 CVF PDF

## Default Workflow

Recommended:

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026
```

With cautious abstract enrichment:

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

Advanced per-step use:

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026
python skills/conference-cvpr/scripts/normalize_cvpr.py --year 2026
python skills/conference-cvpr/scripts/export_cvpr.py --year 2026
python skills/conference-cvpr/scripts/check_completeness.py --year 2026
```

Pipeline:

```text
collect-cvf -> normalize-metadata -> export-artifacts -> completeness-check
```

Default collection is the fast CVF listing-page mode. It captures titles, authors, paper pages, PDF links, and supplementary links when CVF exposes them on the listing page. Abstracts may be largely missing in this mode.

Use cautious per-paper enrichment only when abstract-level analysis is needed:

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

`--enrich-pages` visits each `paper_page_url` to fill missing abstracts and related links. Keep it disabled for fast full-conference runs; use `--limit`, `--sleep`, and `--resume` for staged enrichment instead of requesting all paper pages at once.

## Optional PDF Download

No automatic full-conference PDF download. Collection still stores URLs only. To enter the local fulltext workflow, select a paper explicitly and start with a dry run:

```bash
python skills/conference-cvpr/scripts/download_cvf_pdf.py \
  --metadata data/normalized/computer_vision/cvpr/2026/cvpr_2026_normalized.json \
  --paper-id CVPR2026_000002 \
  --output-dir outputs/computer_vision/cvpr/pdfs/2026 \
  --dry-run
```

Remove `--dry-run` to download. You may replace `--paper-id` with `--title`; ambiguous fuzzy matches print candidates and require `paper_id`. Direct `--pdf-url` mode accepts only `https://openaccess.thecvf.com/...pdf` and also requires a `--paper-id` for the local filename.

After download, extract embedded text separately:

```bash
python skills/cvpr-paper-reader/scripts/extract_pdf_text.py \
  --pdf outputs/computer_vision/cvpr/pdfs/2026/CVPR2026_000002.pdf \
  --output outputs/computer_vision/cvpr/reader/CVPR2026_000002/paper_text.md
```

The downloader does not perform OCR, download code repositories, or automatically invoke reader or idea-miner workflows. PDFs and sidecars are ignored runtime artifacts.

## Outputs

- Raw JSON: `data/raw/computer_vision/cvpr/{year}/cvpr_{year}_raw.json`
- Normalized JSON: `data/normalized/computer_vision/cvpr/{year}/cvpr_{year}_normalized.json`
- Exports: `outputs/computer_vision/cvpr/{year}/`

Exported formats:

- SQLite, table `papers`
- Excel `.xlsx`
- Markdown `.md`
- JSON `.json`
- Completeness reports

Completeness reports include coverage summary fields for `abstract`, `pdf_url`, `supplementary_url`, and `paper_page_url`. Research analysis must read normalized JSON or SQLite first, compute `abstract_coverage`, and downgrade to a title-based preliminary scan when abstracts are missing.

## Scope

Implemented:

- CVF Open Access collection
- `?day=all` first, then day-link fallback
- URL normalization with `urljoin`
- stable `paper_id`
- completeness error/warning report
- explicit selected-paper CVF PDF download
- analysis task rules and shared templates
- nature-academic-search style router with `always_load` and `axes.workflow`

Reserved for later:

- OpenAlex enrichment
- code/project URL discovery
- citation counts
- other AI conferences
