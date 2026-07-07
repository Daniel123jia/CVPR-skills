# Output Contract

Recommended root:

```text
outputs/computer_vision/cvpr/ideas/{year}/
```

Recommended files:

```text
topic_map.md
gap_analysis.md
method_recombination.md
idea_cards.md
experiment_plan.md
```

Every Markdown output must start with:

```markdown
# CVPR Idea Mining — {Artifact Name}

- Conference: CVPR
- Evidence level: {title_only | title_abstract | reader_notes | fulltext_notes | user_hypothesis}
- Source material: {paper titles | abstracts | reader notes | fulltext-derived notes | conference report | user hypothesis}
- Input count: {number of papers/notes}
- Output path: `outputs/computer_vision/cvpr/ideas/{year}/{file}`
- Status: {complete | preliminary | evidence_insufficient}
```

Use Chinese for the main content unless the user asks otherwise.

## File Purposes

- `topic_map.md`: topic clusters, representative papers, evidence level, and uncertainty notes.
- `gap_analysis.md`: cross-paper gaps, limits, missing evaluations, and improvement opportunities.
- `method_recombination.md`: proposed module combinations, source papers, assumptions, and risks.
- `idea_cards.md`: structured research ideas ready for selection and iteration.
- `experiment_plan.md`: datasets, baselines, metrics, first runnable experiment, and validation milestones.

## Optional Reproduction Evidence

When `reader_notes_index.json` includes `files.reproduction_checklist`, it may
be used as an evidence source for idea-card feasibility fields and for
`experiment_plan.md` required inputs, missing details, and risks. Any field
grounded by it must cite the checklist path as its `evidence source`. If the
checklist is absent, idea mining continues from the other indexed notes.
Missing code links, hyperparameters, supplementary details, or unavailable
datasets must remain evidence gaps.

## Topic Map Boundary

If `Input count` is less than 3, `topic_map.md` must label itself as a
single-paper or local topic map based on selected notes. It must not use
phrases such as "CVPR trend" or "CVPR 2026 trend". If `Input count` is 3 or
more, multi-paper topic maps are allowed but must remain bounded by the input
evidence.

## Idea Card Fields

Each idea in `idea_cards.md` must include:

- `idea_id`
- `title`
- `motivation`
- `evidence source`
- `related papers / paper_ids`
- `proposed method`
- `expected contribution`
- `experiment design`
- `required datasets`
- `baseline candidates`
- `risk`
- `first runnable experiment`
- `evidence level`
- `feasibility_score`: 1-5, reflecting startup cost and verifiability, not guaranteed success
- `implementation_difficulty`: low / medium / high
- `data_availability`: available / partially_available / unavailable / unknown
- `dependency_on_original_code`: low / medium / high / unknown
- `expected_novelty`: low / medium / high
- `risk_level`: low / medium / high
- `first_week_action`: one concrete action that can be done in the first week
- `stop_condition`: a concrete reason to stop the idea, such as cannot obtain dataset, cannot reproduce baseline, no reliable boundary mask, or a specified metric degradation

If evidence is insufficient, still write the requested file with `Status: evidence_insufficient` and explain what source material is needed.
