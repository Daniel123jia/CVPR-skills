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

If evidence is insufficient, still write the requested file with `Status: evidence_insufficient` and explain what source material is needed.

