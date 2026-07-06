# End-to-End Acceptance Checklist

Use this checklist for a local manual验收 of the existing `conference-cvpr`, `cvpr-paper-reader`, and `cvpr-idea-miner` loop. The checklist itself is the only committed artifact from this demo.

## conference-cvpr

- [ ] `conference-cvpr` successfully generated raw / normalized / exports / completeness report for a small CVPR 2026 sample.
- [ ] The raw artifact contains CVF metadata only and does not include downloaded PDFs.
- [ ] The normalized artifact has stable `paper_id`, title, authors, year, conference, source, paper page URL, PDF URL metadata, and abstract fields when available.
- [ ] The exports directory was produced locally, but no Excel, SQLite, JSON dump, Markdown export, data directory, outputs directory, or logs directory is committed from this demo.
- [ ] The completeness report identifies missing or low-coverage fields instead of silently treating incomplete metadata as complete.

## cvpr-paper-reader

- [ ] `cvpr-paper-reader` correctly distinguishes evidence level based on available evidence: `fulltext` when full paper text is provided, or `abstract_only` when only title and摘要 are provided.
- [ ] `cvpr-paper-reader` preserves the evidence level in `summary.md`, `method.md`, `experiments.md`, `limitations_and_ideas.md`, or `reading_note.md`.
- [ ] `cvpr-paper-reader` 没有编造实验结果、数据集、ablation findings, baseline comparisons, 代码链接, project URLs, citation counts, or leaderboard claims.
- [ ] When evidence is `abstract_only`, the note is marked preliminary and does not present full-paper method or experiment conclusions.
- [ ] In a `title_only` case, the reader has not output detailed conclusions, method details, dataset claims, ablation claims, or numeric results.
- [ ] Real small-sample `title_only` acceptance has passed when no abstract or local PDF is available.
- [ ] `abstract_only` behavior is covered by local committed fixtures under `tests/fixtures/reader_notes/`, not by committed runtime outputs.
- [ ] `fulltext` behavior is covered by local committed fixtures under `tests/fixtures/reader_notes/`, and future real fulltext acceptance should use only local PDFs already present on disk.

## cvpr-idea-miner

- [ ] `cvpr-idea-miner` 正确读取 reader notes collected from `reading_note.md`, `method.md`, `experiments.md`, and `limitations_and_ideas.md`.
- [ ] `collect_reader_notes.py` indexes the expected reader notes, cleans note-title suffixes, records `evidence_level`, and reports the expected paper count.
- [ ] `cvpr-idea-miner` 区分论文事实和新 idea hypotheses.
- [ ] `idea_cards.md` includes evidence source, risk, and first runnable experiment for each idea card.
- [ ] `idea_cards.md` includes evidence level for each idea card.
- [ ] `idea_cards.md` does not turn a speculative idea into a claimed paper result.
- [ ] In a `title_only` input situation, `cvpr-idea-miner` only performs coarse direction scanning and 没有输出细节结论.
- [ ] In an `abstract_only` input situation, `cvpr-idea-miner` only produces abstract-level preliminary ideas and no experiment details.

## Final Manual Gate

- [ ] All anti-hallucination rules were manually checked before accepting the demo loop.
- [ ] Every claim is traceable to a visible evidence level.
- [ ] No external API was connected during local acceptance.
- [ ] No PDF was downloaded for this demo.
- [ ] No data, outputs, logs, PDF, Excel, or SQLite files were committed.
