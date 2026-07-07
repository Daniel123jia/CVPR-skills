# Evidence Policy

Strictly ground every claim in the provided CVPR material.

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
| `title_only` | Multiple paper titles, optionally with authors or URLs, but no abstracts or notes | 标题级方向扫描、关键词聚类、非常粗粒度的 preliminary idea。不得输出方法细节、实验设计、数据集、结果、baseline 或论文结论。 |
| `abstract_only` | Reader notes or records explicitly marked abstract-only | 摘要级 preliminary idea。不能输出实验细节、数据集细节、ablation、baseline 或结果，除非摘要中明示。 |
| `title_abstract` | Titles plus abstracts, but no reader notes or fulltext-derived notes | 初步主题归类、preliminary topic map、摘要可支撑的机会点。不得重构完整方法、实验表、ablation 或结果，除非摘要明示。 |
| `reader_notes` | `cvpr-paper-reader` notes such as `reading_note.md`, `method.md`, `experiments.md`, `limitations_and_ideas.md` | 基于阅读笔记做 gap analysis、idea cards 和有限 method recombination。缺失字段必须标记为未在笔记中找到。 |
| `fulltext_notes` | Fulltext-derived notes that cover methods, experiments, limitations, or author-stated future work | 较完整的方法组合、idea cards 和实验计划。仍需逐项标记 evidence source。 |
| `user_hypothesis` | User ideas, assumptions, or preferred research directions combined with paper evidence | 可以结合用户想法，但必须区分论文事实、用户设想和 agent 推断。 |

## Labeling Rules

- Mark evidence level near the top of every output file.
- When using `reader_notes_index.json`, read each paper's `evidence_level` before deciding output depth.
- When using an entire reader root, explicitly check whether `title_only`, `abstract_only`, and `fulltext` notes are mixed.
- If duplicate titles appear with different evidence levels, prefer the highest-evidence record before generating detailed ideas.
- Every claim about a paper must include `evidence source` with paper id, title, note path, abstract, or user-provided snippet.
- Use `Not found in provided material` or `未在给定材料中找到` instead of filling gaps.
- Method recombination is a proposed combination, not an existing paper conclusion unless the source explicitly says so.
- For `title_only`, include a warning that the analysis is preliminary and title-level only.
- For `abstract_only`, keep ideas preliminary and do not add experiment details beyond the abstract.
- For `reader_notes`, preserve the note-level evidence boundary; title-only notes remain title-only even after indexing.
- For `fulltext_notes`, use the richer evidence only when the notes include fulltext-derived method, experiment, or limitation content.
- For `user_hypothesis`, label user ideas as hypotheses before turning them into experiment plans.
- If `input_count < 3`, topic maps are single-paper/local analyses based on selected notes; do not describe them as CVPR-wide trends.
