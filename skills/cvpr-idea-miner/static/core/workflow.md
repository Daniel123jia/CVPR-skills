# Workflow

## Default Full Pipeline

```text
topic-map -> gap-analysis -> method-recombination -> idea-cards -> experiment-plan
```

## Operating Rules

1. Load `manifest.yaml` and all files listed in `always_load`.
2. Identify input evidence level with `static/core/evidence-policy.md`.
3. Select one or more workflow fragments from `manifest.yaml`.
4. Load only selected workflow fragments; do not read all workflow files by default.
5. Produce Markdown files under `outputs/computer_vision/cvpr/ideas/{year}/`.
6. Mark every output with evidence level, source material, and status.
7. Keep CVPR-only scope and refuse requests that require other conferences or external enrichment APIs.

## Reader Notes Collection Guard

When using `collect_reader_notes.py` for a single-paper fulltext validation,
prefer:

```bash
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py \
  --selected-root outputs/computer_vision/cvpr/reader/directfisheye_gs_fulltext_test \
  --min-evidence-level fulltext \
  --dedupe-title prefer_highest_evidence \
  --output outputs/computer_vision/cvpr/ideas/directfisheye_gs_fulltext_test/reader_notes_index.json
```

`--selected-root` automatically infers the parent `input_dir`. Use `--input-dir`
for whole-reader-root scans. Passing both `--input-dir` and `--selected-root`
is still supported.

If scanning the whole reader directory, check for mixed `title_only`,
`abstract_only`, and `fulltext` notes. If one paper appears at multiple evidence
levels, prefer highest evidence before generating ideas.

If `reader_notes_index.json` contains `files.reproduction_checklist`, treat it
as optional evidence for feasibility fields and `experiment_plan.md` required
inputs, missing details, and risks. Cite that path when used. Without it,
continue idea mining from the remaining notes and preserve all evidence gaps.

## Topic Map Boundary

If `input_count < 3`, write a single-paper or local topic map and say it is
based on selected notes. Do not call it a CVPR trend or CVPR 2026 trend.
If `input_count >= 3`, a multi-paper topic map is allowed, but it must still
stay within the provided evidence.

## Workflow Selection

| User intent | Workflow |
| --- | --- |
| topic map, direction map, cluster these papers | `topic-map` |
| gaps, limitations, future work, opportunities | `gap-analysis` |
| combine methods, recombine modules, new architecture idea | `method-recombination` |
| generate ideas, idea cards, research inspirations | `idea-cards` |
| experiments, first runnable experiment, validation plan | `experiment-plan` |

If a user asks for "research directions from CVPR 2026" and provides only a paper list, start with `topic-map` and mark `title_only` or `title_abstract` according to available fields.
