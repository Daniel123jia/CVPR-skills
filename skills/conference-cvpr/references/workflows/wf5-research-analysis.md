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

Choose exactly one analysis mode:

### `title_only`

Condition: `abstract_coverage < 5%`.

- Only produce a coarse-grained title-based preliminary scan.
- Include this exact caveat near the top of every analysis artifact: 当前几乎没有摘要，分析仅基于标题，不适合做细粒度技术结论
- Do not present abstract-level topic distributions or fine-grained technical conclusions.
- If the user needs abstract-level analysis, first recommend running `collect_cvpr.py --year {year} --enrich-pages` with `--limit`, `--sleep`, and `--resume` for a cautious enrichment pass.

For `5% <= abstract_coverage < 50%`, do not enter `title_abstract`; output only a title-based preliminary scan with limited use of available abstracts as examples, not as a complete trend basis.

### `title_abstract`

Condition: `abstract_coverage >= 50%`.

- Use title + abstract for preliminary topic grouping and trend summaries.
- Mark conclusions as metadata-based and preliminary.
- Do not claim that the full papers were read.
- Do not infer methods, datasets, ablations, or experimental results unless those details are explicitly present in the title or abstract.

### `fulltext_assisted`

Condition: the user provides full-text content, parsed PDF text, or explicit paper content. 中文条件：用户提供了全文文本、PDF解析文本或明确的论文内容。

- This is the only mode that may discuss method details, experimental setup, datasets, ablation findings, and results.
- Cite the user-provided text or parsed source for every detailed claim.
- If only metadata is available, do not enter this mode.

In every mode, never invent code links, citation counts, experimental results, datasets, ablation findings, leaderboard positions, project pages, GitHub addresses, or fields not actually collected.
中文约束：无论哪种模式，都禁止编造代码链接、引用量、实验结果、数据集、ablation、leaderboard、项目主页、GitHub地址。

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
