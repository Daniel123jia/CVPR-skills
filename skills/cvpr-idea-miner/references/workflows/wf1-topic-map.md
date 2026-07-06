# Workflow 1: Topic Map

## 输入要求

- Multiple CVPR paper titles, title+abstract records, reader notes, fulltext-derived notes, or a `conference-cvpr` normalized JSON/paper list.
- Accept `title_only`, `title_abstract`, `reader_notes`, `fulltext_notes`, or `user_hypothesis`.
- If only titles are available, mark the output as `preliminary`.

## 执行步骤

1. Normalize paper identifiers, titles, available abstracts, note paths, and evidence level.
2. Group papers by visible research theme, task, modality, learning setup, model family, or evaluation target.
3. For each cluster, list representative papers and the exact evidence source used.
4. Separate observed evidence from agent-proposed interpretation.
5. Identify under-covered or ambiguous clusters for later gap analysis.

## 输出格式

Write `topic_map.md` with:

- Standard output header from `static/core/output-contract.md`
- Evidence summary table
- Topic clusters
- Representative papers / paper_ids
- Preliminary opportunity notes
- Missing evidence and uncertainty

## 反幻觉约束

- Under `title_only`, only infer coarse topics from titles; do not claim method, dataset, experiment, or result details.
- Under `title_abstract`, only use abstract-stated information.
- Do not treat cluster labels as paper conclusions.
- Every representative paper must include an evidence source.

