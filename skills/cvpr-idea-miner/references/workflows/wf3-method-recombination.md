# Workflow 3: Method Recombination

## 输入要求

- Requires `reader_notes` or `fulltext_notes` for meaningful method modules.
- `title_abstract` can support only high-level preliminary combinations if abstracts name method components.
- `title_only` is insufficient for method recombination.

## 执行步骤

1. Extract method modules from notes: input representation, backbone, training signal, loss, data strategy, inference procedure, evaluation target, and stated limitations.
2. Build a module matrix linking each module to paper ids and note paths.
3. Propose combinations that address a documented gap or limitation.
4. For every combination, separate `source module`, `proposed combination`, and `agent hypothesis`.
5. Reject combinations that require missing method details; mark what source material is needed.

## 输出格式

Write `method_recombination.md` with:

- Standard output header
- Module matrix
- Recombination candidates with `combo_id`, evidence source, related papers, proposed combination, expected benefit, risk, and evidence level
- Explicit assumptions
- Combinations rejected due to insufficient evidence

## 反幻觉约束

- Do not present a combination idea as an existing paper conclusion.
- Do not invent network structures, formulas, training losses, datasets, or baselines.
- Every method module must cite an evidence source.
- If only titles are provided, write a warning and stop before proposing method details.

