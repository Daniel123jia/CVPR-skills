# WF5 - Metadata-Level Research Analysis

Use this workflow when the user asks for conference-level CVPR direction analysis, metadata-level topic grouping, preliminary trend summaries, or a conference report from normalized/exported CVPR metadata.

This workflow is metadata-level and preliminary. It does not read full papers, extract methods, extract experiments, or generate paper-level ideas.

## Inputs

Prefer normalized JSON:

```text
data/normalized/computer_vision/cvpr/{year}/cvpr_{year}_normalized.json
```

If exports already exist, Markdown, JSON, SQLite, or Excel exports can be used as supporting artifacts. Do not download PDFs for WF5.

## Rules

- Do not call external enrichment APIs in v1.
- Do not download PDFs in bulk.
- Use only collected metadata fields such as title, abstract, authors, paper page URL, PDF URL, and supplementary URL.
- If only CVF metadata is available, limit analysis to title + abstract signals.
- Do not claim full-paper findings.
- Do not invent code links, citation counts, experimental results, datasets, ablation findings, leaderboard positions, project pages, GitHub addresses, or fields not actually collected.
- Mark conclusions as preliminary when they are inferred only from titles and abstracts.
- Use `../_shared/core/research-taxonomy.md` to organize directions when needed.
- Output Markdown files under `outputs/computer_vision/cvpr/{year}/analysis/`.
- Include source rows, paper IDs, titles, and URLs where possible.

## Handoff

If the user asks to read a CVPR paper, summarize a full paper, extract methods, extract experiments, create paper reading notes, or analyze PDF fulltext, hand off to `cvpr-paper-reader`.

If the user asks to generate idea cards, gap analysis, topic maps, method recombinations, or experiment plans from reader notes, hand off to `cvpr-idea-miner`.

WF5 may recommend those handoffs, but it must not imply that conference-cvpr has read the full paper.

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

In every mode, never invent code links, citation counts, experimental results, datasets, ablation findings, leaderboard positions, project pages, GitHub addresses, or fields not actually collected.
中文约束：无论哪种模式，都禁止编造代码链接、引用量、实验结果、数据集、ablation、leaderboard、项目主页、GitHub地址。

## Suggested Outputs

```text
outputs/computer_vision/cvpr/{year}/analysis/cvpr_{year}_metadata_report.md
outputs/computer_vision/cvpr/{year}/analysis/cvpr_{year}_topic_scan.md
outputs/computer_vision/cvpr/{year}/analysis/cvpr_{year}_handoff_candidates.md
```

## Minimum Analysis Shape

- Conference-level summary with paper count, data source, and caveats.
- Metadata coverage summary, including `abstract_coverage`.
- Topic scan using the shared research taxonomy where appropriate.
- Representative paper list with `paper_id`, title, authors, and URLs.
- Handoff candidates for local fulltext reading or idea mining, clearly labeled as next steps.
