# Workflow 2: Gap Analysis

## 输入要求

- Best with `reader_notes` or `fulltext_notes`.
- Accept `title_abstract` for preliminary gaps when abstracts explicitly mention limitations or unresolved problems.
- Do not perform detailed gap analysis from `title_only`; produce an evidence warning instead.

## 执行步骤

1. Start from a topic map when available; otherwise build a minimal cluster list from provided materials.
2. Extract explicitly stated limitations, failure cases, missing evaluations, datasets, assumptions, and future work from notes or abstracts.
3. Compare clusters for repeated constraints, missing modalities, weak supervision gaps, generalization gaps, efficiency gaps, robustness gaps, or evaluation gaps.
4. Label each gap as `paper-stated`, `cross-paper observation`, or `agent hypothesis`.
5. Rank gaps by evidence strength, novelty potential, feasibility, and experimentability.

## 输出格式

Write `gap_analysis.md` with:

- Standard output header
- Evidence coverage summary
- Gap table with `gap_id`, description, evidence source, related papers, opportunity, risk, and evidence level
- Gaps not supported by evidence
- Inputs needed for deeper analysis

## 反幻觉约束

- Do not invent author-stated limitations.
- Do not claim a gap is "unsolved" without evidence from the provided material.
- Do not name datasets, baselines, or results unless present in the source material.
- If evidence is `title_only`, write `Status: evidence_insufficient`.

