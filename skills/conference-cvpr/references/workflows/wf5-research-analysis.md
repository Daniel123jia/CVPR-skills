# WF5 — Research Analysis

Use this workflow when the user asks to analyze CVPR research directions, read papers, summarize trends, create paper notes, create a conference report, or generate research ideas.

## Inputs

Prefer normalized JSON:

```text
data/normalized/computer_vision/cvpr/{year}/cvpr_{year}_normalized.json
```

If exports already exist, Markdown and SQLite can also be used as supporting artifacts.

## Rules

- Do not call external enrichment APIs in v1.
- Do not download PDFs in bulk.
- Use available metadata and any user-provided paper text.
- If only CVF metadata is available, limit analysis to title + abstract signals.
- Do not claim full-paper findings unless the user provided full paper text.
- Do not invent code links, citation counts, experimental results, datasets, ablation findings, or leaderboard positions.
- Mark conclusions as preliminary when they are inferred only from titles and abstracts.
- Use `../_shared/core/research-taxonomy.md` to organize directions.
- Use `../_shared/templates/paper-note.md` for individual paper reading notes.
- Use `../_shared/templates/conference-report.md` for conference-level summaries.
- Use `../_shared/templates/idea-card.md` for research ideas.
- Output Markdown files under `outputs/computer_vision/cvpr/{year}/analysis/`.
- Include source rows, paper IDs, titles, and URLs where possible.

## Metadata Coverage Gate

Before analysis, read the normalized JSON or SQLite export and compute:

```text
abstract_coverage = papers_with_non_empty_abstract / total_papers
```

- If `abstract_coverage < 50%`, output only a title-based preliminary scan. Do not present abstract-level topic distributions or fine-grained technical claims.
- If `abstract_coverage < 5%`, include this exact caveat near the top of every analysis artifact: 当前几乎没有摘要，分析仅基于标题，不适合做细粒度技术结论
- When coverage is below either threshold, do not output method details, experimental results, datasets, ablation findings, code links, citation counts, leaderboard positions, or other fields not actually collected.
- 中文约束：不能输出方法细节、实验结果、数据集、ablation、代码链接、引用量等未采集字段。
- If the user needs abstract-level analysis, first recommend running `collect_cvpr.py --year {year} --enrich-pages` with `--limit`, `--sleep`, and `--resume` for a cautious enrichment pass.

## Suggested Outputs

```text
outputs/computer_vision/cvpr/{year}/analysis/cvpr_{year}_conference_report.md
outputs/computer_vision/cvpr/{year}/analysis/cvpr_{year}_idea_cards.md
outputs/computer_vision/cvpr/{year}/analysis/paper_notes/
```

## Minimum Analysis Shape

- Conference-level summary with paper count, data source, and caveats.
- Topic map using the shared research taxonomy.
- Representative paper list with `paper_id`, title, authors, and URLs.
- Idea cards that state inspiration, hypothesis, method, evaluation, risk, and first experiment.
