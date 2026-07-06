# cvpr-idea-miner

`cvpr-idea-miner` is a CVPR-only research idea mining skill for multi-paper metadata, reading notes, and conference reports.

Use it after `conference-cvpr` has produced normalized paper metadata or after `cvpr-paper-reader` has produced paper-level notes. It does not collect whole CVPR proceedings, parse single PDFs, call external enrichment APIs, download PDFs, or perform OCR.

## Inputs

Preferred inputs:

- `cvpr-paper-reader` outputs: `reading_note.md`, `method.md`, `experiments.md`, `limitations_and_ideas.md`
- `conference-cvpr` outputs: normalized JSON, conference reports, paper lists
- User-provided paper metadata, abstracts, reading notes, or hypotheses

Evidence level controls the allowed depth. `cvpr-idea-miner` must read the
`evidence_level` from indexed reader notes when it is available:

- `title_only`: only coarse direction scanning and direction-level preliminary idea.
- `abstract_only`: abstract-level preliminary idea only; do not output experiment details.
- `reader_notes`: use the note's own evidence level to decide whether the idea can go beyond preliminary.
- `fulltext_notes` / fulltext-derived reader notes: can support more complete gap analysis, idea cards, and experiment plans.

Every idea card must label both `evidence source` and `evidence level`.

## Workflows

Default full pipeline:

```text
topic-map -> gap-analysis -> method-recombination -> idea-cards -> experiment-plan
```

Output root:

```text
outputs/computer_vision/cvpr/ideas/{year}/
```

Recommended files:

- `topic_map.md`
- `gap_analysis.md`
- `method_recombination.md`
- `idea_cards.md`
- `experiment_plan.md`

## Optional Tool

Collect local reading note paths into an index:

```bash
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py --input-dir outputs/computer_vision/cvpr/reader --output outputs/computer_vision/cvpr/ideas/reader_notes_index.json
```

The index includes `paper_id`, cleaned `title`, `evidence_level`, note root, and local note file paths. It scans local Markdown only.
