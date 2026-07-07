# Evidence Policy

Strictly ground every claim in the provided material.

## 严格禁止编造

- 方法细节
- 网络结构
- 公式
- 数据集
- baseline
- 实验结果
- ablation
- leaderboard
- 代码链接
- 项目主页
- 引用量

## 证据等级

| Level | Available evidence | Allowed output |
| --- | --- | --- |
| `title_only` | Only paper title, or title with authors/URLs but no abstract/body | Title-level orientation, possible topic keywords, and a clear warning. No method, network, experiment, result, dataset, or conclusion details. |
| `abstract_only` | Title plus abstract, but no full paper text | Preliminary summary based on the abstract. No full method reconstruction, experiment table, ablation, or numerical result claims unless explicitly present in the abstract. |
| `fulltext` | Full paper text, parsed PDF text, or pasted sections covering method and experiments | Complete reading note, method extraction, experiment table, limitations, and grounded ideas. Missing sections still stay marked as missing. |
| `user_provided_notes` | User notes, annotations, or summaries in addition to any source text | Analyze the notes, but clearly separate original-paper evidence from user inference or user-provided interpretation. |

## Labeling Rules

- Mark the evidence level near the top of every output file.
- Separate `原文证据`, `用户笔记`, and `推断/启发` when user notes are involved.
- Use `Not found in provided material` or `未在给定材料中找到` rather than filling gaps.
- If a user asks for method or experiments under `title_only`, produce a warning file and state that the requested detail cannot be produced.
- If a user asks for full reading under `abstract_only`, mark the result as `preliminary` and avoid method/experiment specifics beyond the abstract.
- Experimental numbers extracted from PDF tables must include numeric extraction confidence.
- If numeric confidence is `low`, do not make strong claims from those numbers.
- If numeric confidence is `medium`, use cautious language and ask for manual PDF verification.
- If different metrics trade off, do not write "uniformly best" or equivalent simplified claims.
- Reproduction assumptions must be separated from paper-backed facts. Do not invent code links, optimizer settings, learning rates, iterations, external repositories, or missing supplementary details.
- Generate the optional `reproduction_checklist.md` only with sufficient `fulltext` method and experiment evidence and a reproduction or improvement intent.
- Missing code, supplementary material, key hyperparameters, datasets, or training details are evidence gaps, not fields to infer. The checklist may ground `cvpr-idea-miner` feasibility and experiment-plan fields.
