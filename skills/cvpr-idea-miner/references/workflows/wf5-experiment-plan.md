# Workflow 5: Experiment Plan

## 输入要求

- Requires selected idea cards.
- Best with `reader_notes` or `fulltext_notes` that mention datasets, metrics, baselines, implementation constraints, or limitations.
- If only titles or abstracts are available, produce a preliminary plan template and mark missing evidence.

## 执行步骤

1. Choose one or more idea cards to operationalize.
2. Define the first runnable experiment before broad follow-up studies.
3. Extract datasets, metrics, baselines, and ablation candidates only from provided evidence.
4. Mark unverified experiment ingredients as assumptions or user choices.
5. Build a staged plan: sanity check, minimal reproduction or proxy baseline, main comparison, ablation, risk fallback.

## 输出格式

Write `experiment_plan.md` with:

- Standard output header
- Selected idea ids
- First runnable experiment
- Data requirements
- Baseline candidates
- Metrics
- Implementation steps
- Ablation or sensitivity checks
- Risks and fallback plans
- Evidence gaps

## 反幻觉约束

- Do not invent benchmark names, baselines, numerical targets, or expected results.
- Do not claim an experiment will reproduce a paper unless evidence includes the needed setup.
- If evidence is insufficient, write a plan skeleton and list required source materials.
- Distinguish paper-backed experiment ingredients from agent-proposed implementation choices.

