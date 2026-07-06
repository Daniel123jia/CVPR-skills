# CVPR-skills

一个面向 CVPR main conference papers 的 Codex / Claude Code Agent Skill 集合，用于从 CVF Open Access 采集、清洗、导出、完整性检查、会议级初步分析，单篇/少量 CVPR 论文精读，以及多篇论文/阅读笔记的研究灵感挖掘。

当前仓库只做 CVPR-skills，不扩展其他会议。当前包含三个 skill：`conference-cvpr`、`cvpr-paper-reader` 和 `cvpr-idea-miner`。v1 专注 CVPR main conference papers，不新增其他会议 skill，不采集 workshops，不调用外部 enrichment API，不批量下载 PDF。

## At A Glance

```text
conference-cvpr       ->  cvpr-paper-reader       ->  cvpr-idea-miner
采集 / 清洗 / 导出 / 检查   单篇阅读笔记与证据分级      topic map / gap / idea cards
```

**v1.3 状态**

| 能力 | 状态 |
| --- | --- |
| CVPR 2026 小样本采集 | 已通过本地真实样本验收 |
| `title_only` reader / idea mining | 已通过本地真实样本验收 |
| `abstract_only` reader note | 已通过 CVF 真实摘要验收 |
| `fulltext` reader / idea mining | 已通过本地 fixture 验收；真实 PDF 验收需用户本地已有 PDF |
| 安全边界 | 不新增其他会议、不接外部 enrichment API、不下载 PDF、不做 OCR |

## Skill Navigator

`skills/conference-cvpr/`、`skills/cvpr-paper-reader/` 和 `skills/cvpr-idea-miner/` 是当前可触发 skill；`skills/_shared/` 只存放共享 schema、规则和模板，不作为独立 skill 使用。

| Skill | 边界 | 典型用途 |
| --- | --- | --- |
| `conference-cvpr` | 整届 CVPR 数据入口 | 整届 CVPR 论文采集、清洗、导出、完整性检查、会议级初步分析 |
| `cvpr-paper-reader` | 单篇论文精读 | 论文精读、方法提取、实验表、中文阅读笔记、局限性分析 |
| `cvpr-idea-miner` | 多篇论文/阅读笔记的研究灵感挖掘 | 方向归纳、研究空白发现、方法组合、idea cards、实验计划 |

| 场景 | 你可以这样说 | Agent 路线 | 推荐入口 |
| --- | --- | --- | --- |
| 一键完整流程 | “获取 CVPR 2026 论文并导出结果” | 采集 → 清洗 → 导出 → 检查 | `python skills/conference-cvpr/scripts/run_pipeline.py --year 2026` |
| 快速采集 | “只采集 CVPR 论文列表” | `collect-cvf` | `collect_cvpr.py --year 2026` |
| 补充摘要 | “给 CVPR 数据补摘要，分批慢一点” | `collect-cvf` with page enrichment | `run_pipeline.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume` |
| 导出文件 | “导出 CVPR 论文 Excel / SQLite / Markdown / JSON” | `export-artifacts` | `export_cvpr.py --year 2026` |
| 质量检查 | “检查缺失字段和重复论文” | `completeness-check` | `check_completeness.py --year 2026` |
| 初步分析 | “分析 CVPR 研究方向” | `research-analysis` with coverage gate | 读取 normalized JSON 或 SQLite 后生成 Markdown 分析 |
| 单篇论文精读 | “精读这篇 CVPR 论文” | `paper-summary -> method-extraction -> experiment-table -> limitations-and-ideas -> reading-note` | `skills/cvpr-paper-reader/` |
| 方法/实验提取 | “提取这篇论文的方法 / 整理实验设置和结果” | `method-extraction` / `experiment-table` | 提供全文、PDF 解析文本或论文片段 |
| 摘要级阅读 | “总结这篇 CVPR 论文” + title/abstract | `paper-summary` preliminary | 只能输出 preliminary summary |
| 多篇论文找灵感 | “从这些 CVPR 论文找研究灵感” | `topic-map -> gap-analysis -> method-recombination -> idea-cards -> experiment-plan` | `skills/cvpr-idea-miner/` |
| 阅读笔记生成 idea | “根据这些阅读笔记生成 idea” | `idea-cards` with `reader_notes` evidence | 读取 `cvpr-paper-reader` 输出 |
| 方法组合 | “把这些 CVPR 方法模块组合一下” | `method-recombination` | 必须标记 evidence source |

**边界很重要：** 只支持 CVPR main conference papers；不采集 workshops，不新增其他会议，不调用外部 enrichment API，不下载 PDF。`conference-cvpr` 不负责单篇精读，`cvpr-paper-reader` 不负责整届会议采集，`cvpr-idea-miner` 不负责整届论文采集或单篇 PDF 解析。

## Quick Start

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run a small CVPR collection sample:

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026 --limit 5
```

Index local paper-reader notes before idea mining:

```bash
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py --input-dir outputs/computer_vision/cvpr/reader --output outputs/computer_vision/cvpr/ideas/reader_notes_index.json
```

Runtime outputs go under `data/`, `outputs/`, and `logs/`; they are intentionally ignored by git.

## Repository Layout

```text
CVPR-skills/
├── README.md
├── LICENSE
├── requirements.txt
├── plugin.json
├── marketplace.json
├── evals/
│   ├── prompts/
│   └── expected/
├── examples/
│   ├── end_to_end_demo/
│   ├── sample_commands.md
│   └── sample_cvpr_2026_5_papers.md
├── scripts/
│   └── update-codex-skills.sh
├── skills/
│   ├── _shared/
│   │   ├── core/
│   │   └── templates/
│   ├── conference-cvpr/
│   │   ├── README.md
│   │   ├── SKILL.md
│   │   ├── manifest.yaml
│   │   ├── static/core/
│   │   ├── references/workflows/
│   │   └── scripts/
│   ├── cvpr-paper-reader/
│   │   ├── README.md
│   │   ├── SKILL.md
│   │   ├── manifest.yaml
│   │   ├── static/core/
│   │   ├── references/workflows/
│   │   └── scripts/
│   └── cvpr-idea-miner/
│       ├── README.md
│       ├── SKILL.md
│       ├── manifest.yaml
│       ├── static/core/
│       ├── references/workflows/
│       └── scripts/
└── tests/
    └── fixtures/
```

`skills/conference-cvpr/` 是会议级 workflow 核心；`skills/cvpr-paper-reader/` 是论文级精读 workflow；`skills/cvpr-idea-miner/` 是多篇论文/阅读笔记的 idea mining workflow。`data/`、`outputs/` 和 `logs/` 是运行产物，不提交仓库。

## Install

```bash
cd CVPR-skills
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/update-codex-skills.sh
```

安装脚本会同步 `skills/` 下的顶层目录到 `${CODEX_HOME:-$HOME/.codex}/skills`。如果目标目录已有同名 skill，会先备份，再合并覆盖同名文件，不删除目标目录里的额外文件。

## Use

在 Codex / Claude Code 中触发 `conference-cvpr` skill，例如：

- 获取 CVPR 2026 论文
- 采集 CVPR 论文
- 构建 CVPR 数据库
- 导出 CVPR 论文 Excel
- 分析 CVPR 研究方向

推荐一键运行完整流程：

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026
```

需要分批补摘要时：

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

默认完整流程等价于：

```text
collect -> normalize -> export -> check
```

高级用法：分别运行每一步。

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026
python skills/conference-cvpr/scripts/normalize_cvpr.py --year 2026
python skills/conference-cvpr/scripts/export_cvpr.py --year 2026
python skills/conference-cvpr/scripts/check_completeness.py --year 2026
```

输出路径：

```text
data/raw/computer_vision/cvpr/{year}/cvpr_{year}_raw.json
data/normalized/computer_vision/cvpr/{year}/cvpr_{year}_normalized.json
outputs/computer_vision/cvpr/{year}/
```

导出格式包括 SQLite、Excel、Markdown 和 JSON；SQLite 表名为 `papers`。

触发 `cvpr-paper-reader` skill 的例子：

- 精读这篇 CVPR 论文
- 帮我读这篇 CVPR paper
- 总结这篇 CVPR 论文
- 提取这篇论文的方法
- 整理实验设置和结果
- 生成论文阅读笔记
- 从这篇 CVPR 论文找研究灵感
- CVPR paper reader
- read CVPR paper

本地 PDF 可以先提取文本：

```bash
python skills/cvpr-paper-reader/scripts/extract_pdf_text.py --pdf path/to/paper.pdf --output outputs/computer_vision/cvpr/reader/{paper_id}/paper_text.md
```

论文级默认输出路径：

```text
outputs/computer_vision/cvpr/reader/{paper_id}/
```

推荐输出文件包括 `summary.md`、`method.md`、`experiments.md`、`limitations_and_ideas.md` 和 `reading_note.md`。

触发 `cvpr-idea-miner` skill 的例子：

- 从这些 CVPR 论文找研究灵感
- 帮我分析 CVPR 研究空白
- 根据这些阅读笔记生成 idea
- 帮我做 CVPR topic map
- 从 CVPR 2026 中找可做的研究方向
- 根据这些论文总结未来工作
- CVPR idea miner
- research idea from CVPR papers

它面向多篇论文或阅读笔记，默认完整流程是：

```text
topic-map -> gap-analysis -> method-recombination -> idea-cards -> experiment-plan
```

可先索引 `cvpr-paper-reader` 的本地输出：

```bash
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py --input-dir outputs/computer_vision/cvpr/reader --output outputs/computer_vision/cvpr/ideas/reader_notes_index.json
```

idea mining 推荐输出路径：

```text
outputs/computer_vision/cvpr/ideas/{year}/
```

推荐输出文件包括 `topic_map.md`、`gap_analysis.md`、`method_recombination.md`、`idea_cards.md` 和 `experiment_plan.md`。

## Fast Collection And Enrichment

默认采集是快速模式，主要读取 CVF 列表页可直接获得的字段：标题、作者、论文页、PDF 链接和 supplementary 链接。CVF 列表页通常不稳定提供摘要，因此 `abstract` 默认可能大量缺失。

如果需要摘要级分析，请显式运行分批 enrichment：

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

`--enrich-pages` 会逐篇访问 `paper_page_url` 补摘要。建议配合 `--limit`、`--sleep`、`--resume` 分批进行，避免一次性请求整届会议的所有论文页。

常用命令和轻量输出结构示例见 `examples/`。示例文件只展示字段形态，不包含真实完整 CVPR 2026 数据。

## Analysis Guardrails

`research-analysis` 必须先读取 normalized JSON 或 SQLite 并计算 `abstract_coverage`：

- `abstract_coverage < 5%`：只能做 `title_only` 粗粒度 preliminary scan，并写明“当前几乎没有摘要，分析仅基于标题，不适合做细粒度技术结论”。
- `abstract_coverage >= 50%`：可以做 `title_abstract` 初步主题归类和趋势总结，但不能声称读过全文。
- 只有用户提供全文文本、PDF 解析文本或明确论文内容时，才进入 `fulltext_assisted`，讨论方法细节、实验设置、数据集、ablation 和结果。

无论哪种模式，都不能编造代码链接、引用量、实验结果、数据集、ablation、leaderboard、项目主页或 GitHub 地址。

`cvpr-paper-reader` 使用更严格的论文级证据等级：

- `title_only`：只能做标题级粗略判断，不能输出方法和实验细节。
- `abstract_only`：只能做摘要级 preliminary summary。
- `fulltext`：可以做完整阅读笔记、方法提取、实验表、局限性和研究灵感。
- `user_provided_notes`：可以结合用户笔记分析，但要区分原文证据和用户推断。

`cvpr-idea-miner` 使用多篇论文/阅读笔记级证据等级：

- `title_only`：只能做标题级粗粒度方向扫描。
- `abstract_only`：只能做摘要级 preliminary idea，不能补实验细节。
- `title_abstract`：可以做初步主题归类和 preliminary idea。
- `reader_notes`：可以基于阅读笔记做 gap analysis 和 idea cards，但必须继承笔记本身的证据边界。
- `fulltext_notes`：可以做较完整的方法组合和实验计划。
- `user_hypothesis`：可以结合用户想法，但必须区分论文事实和用户设想。

`collect_reader_notes.py` 会从 `reading_note.md`、`method.md`、`experiments.md` 和 `limitations_and_ideas.md` 建立本地索引，并记录：

- `paper_id`
- 清洗后的 `title`
- `evidence_level`
- 每个本地 note 文件路径

常见阅读笔记标题后缀如 `中文阅读笔记`、`Reading Note`、`Paper Reading Note` 会被清理，不会进入索引标题。

## Evals

`evals/` 提供轻量路由样例：

- `collect_cvpr_2026`
- `export_cvpr_excel`
- `analyze_low_abstract_coverage`
- `reject_non_cvpr`
- `read_single_cvpr_paper`
- `method_extraction`
- `abstract_only_warning`
- `idea_from_reader_notes`
- `title_only_idea_warning`
- `method_recombination`

这些样例用于人工或自动检查 Agent 是否选择正确 workflow，并遵守 v1 只支持 CVPR main conference papers 的范围。

## Test

```bash
python -m unittest discover -s tests
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py --help
python skills/cvpr-paper-reader/scripts/extract_pdf_text.py --help
python skills/conference-cvpr/scripts/run_pipeline.py --help
python skills/conference-cvpr/scripts/collect_cvpr.py --help
python skills/conference-cvpr/scripts/normalize_cvpr.py --help
python skills/conference-cvpr/scripts/export_cvpr.py --help
python skills/conference-cvpr/scripts/check_completeness.py --help
```

当前发布前验证：

- `44 tests OK`
- `run_pipeline.py --help` passed
- `extract_pdf_text.py --help` passed
- `collect_reader_notes.py --help` passed
- `git diff --check` passed
