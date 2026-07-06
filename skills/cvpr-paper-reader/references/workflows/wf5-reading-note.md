# WF5 — Reading Note

## 输入要求

- Full reading note requires full paper text or parsed PDF text.
- Abstract-only input produces a preliminary reading note.
- Title-only input produces an evidence-insufficient note and cannot include method or experiment details.

## 执行步骤

1. Reuse outputs from summary, method, experiments, and limitations workflows when available.
2. Organize the paper into a Chinese note for future review.
3. Highlight what is directly supported by the paper versus user notes or reader inference.
4. Add a short action list for follow-up reading, reproduction, or idea validation.
5. Keep unsupported sections explicit rather than padded.

## 输出格式

Write `reading_note.md`:

```markdown
# {title} — 中文阅读笔记

- Evidence level: {level}
- Status: {complete | preliminary | evidence_insufficient}

## 论文信息
## 速读结论
## 背景与问题
## 方法详解
## 实验整理
## 局限性
## 研究灵感
## 待读问题
## 证据索引
```

## 反幻觉约束

- Do not make the note look complete when only abstract or title is available.
- For `title_only`, state that method and experiment sections cannot be produced.
- For `abstract_only`, mark `preliminary` and avoid fulltext-only claims.
