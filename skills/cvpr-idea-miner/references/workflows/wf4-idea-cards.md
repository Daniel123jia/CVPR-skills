# Workflow 4: Idea Cards

## 输入要求

- Works best after topic map, gap analysis, and method recombination.
- Requires at least `title_abstract` for preliminary idea cards.
- `reader_notes` or `fulltext_notes` are required for detailed proposed method and experiment fields.

## 执行步骤

1. Select ideas from grounded gaps, recombination candidates, or user hypotheses.
2. Assign stable `idea_id` values such as `CVPR-IDEA-001`.
3. Fill every required idea-card field from `static/core/output-contract.md`.
4. Mark missing fields as `Not found in provided material` rather than guessing.
5. Rank ideas by evidence strength, feasibility, risk, and first experiment clarity.

## 输出格式

Write `idea_cards.md`.

Each idea must include:

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

## 反幻觉约束

- Under `title_only`, do not produce detailed proposed methods or experiment designs.
- Do not invent datasets or baselines; use `candidate, needs confirmation` only when the user explicitly asks for brainstorming beyond evidence.
- Keep paper facts and proposed ideas separate.
- Cite evidence source for each idea.

