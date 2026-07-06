# WF1 — Paper Summary

## 输入要求

- Minimum: title.
- Recommended: title + abstract.
- Best: full paper text or parsed PDF text.

## 执行步骤

1. Identify evidence level.
2. Extract title, authors, venue/year, abstract, and source URLs when present.
3. Summarize the problem, motivation, claimed contribution, method overview, and reported findings only from available evidence.
4. Under `abstract_only`, mark the output as `preliminary`.
5. Under `title_only`, produce only title-level orientation and missing-evidence warnings.

## 输出格式

Write `summary.md`:

```markdown
# {title} — 论文总结

- Conference: CVPR
- Evidence level: {level}
- Status: {complete | preliminary | evidence_insufficient}

## 一句话总结
## 研究问题
## 核心贡献
## 方法概览
## 实验与结论
## 证据不足与注意事项
```

## 反幻觉约束

- Do not infer method internals from the title.
- Do not invent datasets, metrics, baselines, numbers, or conclusions.
- If only the abstract is available, do not claim full-paper coverage.
