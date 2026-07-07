# WF3 — Experiment Table

## 输入要求

- Required: full paper text, parsed PDF text, or pasted experiment/results sections.
- Abstract-only input can mention only experiment facts explicitly present in the abstract.
- Title-only input is insufficient.

## 执行步骤

1. Locate experiments, implementation details, datasets, metrics, baselines, main results, and ablation sections.
2. Extract exact dataset names, task settings, metrics, compared methods, and reported values.
3. Preserve numeric values exactly as given.
4. Separate main results, ablations, robustness studies, and qualitative results.
5. Mark missing tables or unreadable PDF extraction gaps.
6. Add `Numeric Extraction Confidence` for every extracted table or figure containing numbers.

## 输出格式

Write `experiments.md`:

```markdown
# {title} — 实验整理

- Evidence level: {level}
- Status: {complete | preliminary | evidence_insufficient}

## 实验设置
| 项目 | 内容 | 原文证据 |

## 主结果
| 数据集 | 指标 | 本文方法 | baseline | 结果 | 备注 |

## 消融实验
| 变量 | 设置 | 结果 | 结论 | 原文证据 |

## Numeric Extraction Confidence
| Table/Figure | Confidence | Reason | Action |
| --- | --- | --- | --- |

## 复现相关信息
## 缺失信息
```

## 反幻觉约束

- Do not invent 数据集, baseline, metrics, numbers, ablation, leaderboard, or implementation settings.
- If a table is absent or extraction lost it, write `未在给定材料中找到`.
- Do not normalize or reinterpret results unless the paper explicitly defines the metric.
- `high`: 数字和行列对应关系清晰.
- `medium`: 数字可读，但表格行列有压缩或局部歧义; 只能写谨慎结论.
- `low`: 数字/行列难以可靠对应; 不允许生成强结论, 必须提醒人工查看 PDF.
- `unavailable`: 图表、补充材料或关键表格不在提取文本中.
- If PDF extraction compresses tables, state that explicitly.
- If metrics trade off, do not summarize the method as `uniformly best`.
