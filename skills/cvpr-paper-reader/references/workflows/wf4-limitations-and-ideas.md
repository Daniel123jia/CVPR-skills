# WF4 — Limitations And Ideas

## 输入要求

- Best: full paper text with limitations, discussion, experiments, and failure cases.
- Acceptable: abstract plus user notes for preliminary idea generation.
- Title-only input supports only a warning and broad topic questions.

## 执行步骤

1. Extract explicit limitations, failure cases, assumptions, and negative results.
2. Infer possible limitations only when grounded in method or experiment evidence.
3. Separate paper-stated limitations from reader-inferred limitations.
4. Generate research ideas that address identified gaps or natural extensions.
5. For every idea, include the evidence anchor and what must be verified next.

## 输出格式

Write `limitations_and_ideas.md`:

```markdown
# {title} — 局限性与研究灵感

- Evidence level: {level}
- Status: {complete | preliminary | evidence_insufficient}

## 论文明确提到的局限
## 基于证据的潜在局限
## 可验证研究灵感
| Idea | Motivation | Evidence anchor | First validation |
## 不应过度解读的地方
```

## 反幻觉约束

- Do not present speculative ideas as paper conclusions.
- Do not invent failure cases, limitations, code links, project pages, or citation impact.
- Under `abstract_only`, label ideas as preliminary and explain missing evidence.
