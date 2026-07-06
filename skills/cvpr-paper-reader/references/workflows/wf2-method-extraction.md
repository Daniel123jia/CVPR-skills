# WF2 — Method Extraction

## 输入要求

- Required for full extraction: full paper text, parsed PDF text, or pasted method sections.
- Abstract-only input may support a short preliminary method sketch only if the abstract explicitly states it.
- Title-only input is insufficient.

## 执行步骤

1. Locate method, approach, model, architecture, training, inference, and loss sections.
2. Extract the framework as components, data flow, and training/inference procedure.
3. Copy or restate formulas only when they appear in the provided material.
4. Mark implementation-relevant details as found, missing, or ambiguous.
5. If evidence is insufficient, write a warning-oriented `method.md` instead of guessing.

## 输出格式

Write `method.md`:

```markdown
# {title} — 方法提取

- Evidence level: {level}
- Status: {complete | preliminary | evidence_insufficient}

## 方法总览
## 模块与职责
| 模块 | 输入 | 输出 | 作用 | 原文证据 |
## 流程
## 核心公式
## 训练与推理
## 复现要点
## 缺失信息
```

## 反幻觉约束

- Do not invent 网络结构, loss, optimizer, schedule, prompts, data pipeline, or formulas.
- If a component name is not in the material, label it as an inferred description rather than a paper term.
- For `title_only`, state: `不得生成方法、网络结构、实验或结果细节`.
