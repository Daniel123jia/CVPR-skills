# CVPR-skills

一个面向 CVPR main conference papers 的 Codex / Claude Code Agent Skill，用于从 CVF Open Access 采集、清洗、导出、完整性检查和初步研究分析。

当前仓库只包含一个 skill：`conference-cvpr`。v1 专注 CVPR main conference papers，不新增其他会议 skill，不采集 workshops，不调用外部 enrichment API，不批量下载 PDF。

## Skill Navigator

`skills/conference-cvpr/` 是当前唯一可触发 skill；`skills/_shared/` 只存放共享 schema、规则和模板，不作为独立 skill 使用。

| 场景 | 你可以这样说 | Agent 路线 | 推荐入口 |
| --- | --- | --- | --- |
| 一键完整流程 | “获取 CVPR 2026 论文并导出结果” | 采集 → 清洗 → 导出 → 检查 | `python skills/conference-cvpr/scripts/run_pipeline.py --year 2026` |
| 快速采集 | “只采集 CVPR 论文列表” | `collect-cvf` | `collect_cvpr.py --year 2026` |
| 补充摘要 | “给 CVPR 数据补摘要，分批慢一点” | `collect-cvf` with page enrichment | `run_pipeline.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume` |
| 导出文件 | “导出 CVPR 论文 Excel / SQLite / Markdown / JSON” | `export-artifacts` | `export_cvpr.py --year 2026` |
| 质量检查 | “检查缺失字段和重复论文” | `completeness-check` | `check_completeness.py --year 2026` |
| 初步分析 | “分析 CVPR 研究方向” | `research-analysis` with coverage gate | 读取 normalized JSON 或 SQLite 后生成 Markdown 分析 |

**边界很重要：** 只支持 CVPR main conference papers；不采集 workshops，不新增其他会议，不调用外部 enrichment API，不下载 PDF。

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
│   ├── sample_commands.md
│   └── sample_cvpr_2026_5_papers.md
├── scripts/
│   └── update-codex-skills.sh
├── skills/
│   ├── _shared/
│   │   ├── core/
│   │   └── templates/
│   └── conference-cvpr/
│       ├── README.md
│       ├── SKILL.md
│       ├── manifest.yaml
│       ├── static/core/
│       ├── references/workflows/
│       └── scripts/
└── tests/
```

`skills/conference-cvpr/` 是仓库核心。`data/`、`outputs/` 和 `logs/` 是运行产物，不提交仓库。

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

## Evals

`evals/` 提供轻量路由样例：

- `collect_cvpr_2026`
- `export_cvpr_excel`
- `analyze_low_abstract_coverage`
- `reject_non_cvpr`

这些样例用于人工或自动检查 Agent 是否选择正确 workflow，并遵守 v1 只支持 CVPR main conference papers 的范围。

## Test

```bash
python -m unittest discover -s tests
python skills/conference-cvpr/scripts/run_pipeline.py --help
python skills/conference-cvpr/scripts/collect_cvpr.py --help
python skills/conference-cvpr/scripts/normalize_cvpr.py --help
python skills/conference-cvpr/scripts/export_cvpr.py --help
python skills/conference-cvpr/scripts/check_completeness.py --help
```
