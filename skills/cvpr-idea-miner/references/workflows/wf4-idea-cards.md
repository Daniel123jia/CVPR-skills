# Workflow 4: Idea Cards

## 输入要求

- Works best after topic map, gap analysis, and method recombination.
- Must read `evidence_level` from each reader note or `reader_notes_index.json` entry before deciding card depth.
- Requires at least `title_abstract` for preliminary idea cards.
- `title_only` supports only direction-level preliminary ideas.
- `abstract_only` supports abstract-level preliminary ideas, but not experiment details.
- `reader_notes` or `fulltext_notes` are required for detailed proposed method and experiment fields.
- For one fulltext reader-note folder, prefer a selected-root-only note index; use `--input-dir` for whole-reader-root scans.
- If the index includes `files.reproduction_checklist`, use it as optional evidence for feasibility fields. Its absence does not block idea cards.

## 执行步骤

1. Select ideas from grounded gaps, recombination candidates, or user hypotheses.
2. Assign stable `idea_id` values such as `CVPR-IDEA-001`.
3. Fill every required idea-card field from `static/core/output-contract.md`.
4. Mark missing fields as `Not found in provided material` rather than guessing.
5. Mark each idea with both `evidence source` and `evidence level`.
6. Rank ideas by evidence strength, feasibility, risk, and first experiment clarity.
7. When a checklist supports `dependency_on_original_code`, `data_availability`, `implementation_difficulty`, `first_week_action`, or `stop_condition`, cite `reproduction_checklist.md` as the evidence source.

## 输出格式

Write `idea_cards.md`.

Each idea must include:

- `idea_id`
- `title`
- `motivation`
- `evidence source`
- `evidence level`
- `related papers / paper_ids`
- `proposed method`
- `expected contribution`
- `experiment design`
- `required datasets`
- `baseline candidates`
- `risk`
- `first runnable experiment`
- `feasibility_score`: 1-5
- `implementation_difficulty`: low / medium / high
- `data_availability`: available / partially_available / unavailable / unknown
- `dependency_on_original_code`: low / medium / high / unknown
- `expected_novelty`: low / medium / high
- `risk_level`: low / medium / high
- `first_week_action`
- `stop_condition`

## 反幻觉约束

- Under `title_only`, produce only direction-level preliminary ideas; do not produce detailed proposed methods or experiment designs.
- Under `abstract_only`, do not output experiment details unless they are explicitly stated in the abstract.
- Do not invent datasets or baselines; use `candidate, needs confirmation` only when the user explicitly asks for brainstorming beyond evidence.
- Keep paper facts and proposed ideas separate.
- Cite evidence source and evidence level for each idea.
- `feasibility_score` describes startup cost and verifiability, not whether the idea will succeed.
- If the idea needs original author code and no code link is present in the material, set `dependency_on_original_code` to `high` or `unknown`.
- `first_week_action` and `stop_condition` must be specific and testable.
- Do not invent missing code links, hyperparameters, supplementary details, or unavailable datasets beyond the reproduction checklist; keep them as evidence gaps.
