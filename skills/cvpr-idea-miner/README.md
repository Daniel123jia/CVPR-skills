# cvpr-idea-miner

`cvpr-idea-miner` is a CVPR-only research idea mining skill for multi-paper metadata, reading notes, and conference reports.

Use it after `conference-cvpr` has produced normalized paper metadata or after `cvpr-paper-reader` has produced paper-level notes. It does not collect whole CVPR proceedings, parse single PDFs, call external enrichment APIs, download PDFs, or perform OCR.

## Inputs

Preferred inputs:

- `cvpr-paper-reader` outputs: `reading_note.md`, `method.md`, `experiments.md`, `limitations_and_ideas.md`, and optional `reproduction_checklist.md`
- `conference-cvpr` outputs: normalized JSON, conference reports, paper lists
- User-provided paper metadata, abstracts, reading notes, or hypotheses

Evidence level controls the allowed depth. `cvpr-idea-miner` must read the
`evidence_level` from indexed reader notes when it is available:

- `title_only`: only coarse direction scanning and direction-level preliminary idea.
- `abstract_only`: abstract-level preliminary idea only; do not output experiment details.
- `reader_notes`: use the note's own evidence level to decide whether the idea can go beyond preliminary.
- `fulltext_notes` / fulltext-derived reader notes: can support more complete gap analysis, idea cards, and experiment plans.

Every idea card must label both `evidence source` and `evidence level`.

When indexed, `reproduction_checklist.md` is an optional evidence source for
`dependency_on_original_code`, `data_availability`,
`implementation_difficulty`, `first_week_action`, `stop_condition`, and
experiment-plan inputs, missing details, and risks. Its absence does not block
idea mining. Do not fill evidence gaps with invented code links or
hyperparameters.

When collecting notes from a full reader root, historical `title_only`,
`abstract_only`, and `fulltext` samples can be mixed. For single-paper fulltext
validation, prefer a filtered index:

```bash
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py \
  --selected-root outputs/computer_vision/cvpr/reader/directfisheye_gs_fulltext_test \
  --min-evidence-level fulltext \
  --dedupe-title prefer_highest_evidence \
  --output outputs/computer_vision/cvpr/ideas/directfisheye_gs_fulltext_test/reader_notes_index.json
```

`--selected-root` automatically infers the parent `input_dir`. Use
`--input-dir outputs/computer_vision/cvpr/reader` when scanning the whole reader
root; passing both flags is still supported.

If the same paper appears at multiple evidence levels, prefer
`--dedupe-title prefer_highest_evidence`.

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

The index includes `paper_id`, cleaned `title`, `evidence_level`, note root, and
local note file paths. If present, `files.reproduction_checklist` records the
optional checklist path. It scans local Markdown only.

If `input_count < 3`, topic maps must be labeled as single-paper or local topic
maps based on selected notes. Do not describe them as a CVPR trend or CVPR 2026
trend. With `input_count >= 3`, multi-paper topic maps are allowed, but still
must stay inside the provided evidence.
