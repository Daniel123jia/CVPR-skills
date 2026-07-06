# ai-conference-skills

面向人工智能顶会论文采集、清洗、导出、阅读、分析和研究灵感生成的 Codex / Claude Code Agent Skill 库。

这个项目模仿 `nature-skills` 的组织思想：`skills/` 下每个顶层目录都是一个可安装 skill，复杂规则拆到 `manifest.yaml`、`static/`、`references/`、`scripts/`，共享规则统一放在 `skills/_shared/`。`scripts/` 是 skill 的工具，不是项目主体；`data/` 和 `outputs/` 是运行产物，不纳入源码结构。

第一版只实现 `conference-cvpr`。后续计划扩展 ICCV、ECCV、NeurIPS、ICML、ACL、AAAI、IJCAI。

## 结构

```text
ai-conference-skills/
├── README.md
├── LICENSE
├── requirements.txt
├── scripts/
│   └── update-codex-skills.sh
└── skills/
    ├── _shared/
    │   ├── core/
    │   └── templates/
    └── conference-cvpr/
        ├── README.md
        ├── SKILL.md
        ├── manifest.yaml
        ├── static/
        │   ├── core/
        ├── references/
        │   └── workflows/
        └── scripts/
```

## 安装

```bash
cd ai-conference-skills
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/update-codex-skills.sh
```

安装脚本会同步 `skills/` 下的顶层目录到 `${CODEX_HOME:-$HOME/.codex}/skills`。如果目标目录已有同名 skill，会先备份，再合并覆盖同名文件，不删除目标目录里的额外文件。

## 使用

在 Codex / Claude Code 中触发 `conference-cvpr` skill，例如：

- 获取 CVPR 2026 论文
- 采集 CVPR 论文
- 构建 CVPR 数据库
- 导出 CVPR 论文 Excel
- 分析 CVPR 研究方向

完整默认流程：

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026
python skills/conference-cvpr/scripts/normalize_cvpr.py --year 2026
python skills/conference-cvpr/scripts/export_cvpr.py --year 2026
python skills/conference-cvpr/scripts/check_completeness.py --year 2026
```

第一版范围：

- 只采集 CVPR main conference papers
- 主数据源只用 CVF Open Access
- 不采集 workshops
- 不接 OpenAlex、DBLP、Semantic Scholar
- 不批量下载 PDF，只保存 `pdf_url`
- 输出 SQLite、Excel、Markdown、JSON 作为运行产物

默认采集是快速模式，主要读取 CVF 列表页可直接获得的字段。CVF 列表页通常不稳定提供摘要，因此 `abstract` 默认可能大量缺失；如果需要摘要级分析，请显式运行：

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

`--enrich-pages` 会逐篇访问 `paper_page_url` 补摘要，建议配合 `--limit`、`--sleep`、`--resume` 分批进行，避免一次性请求整届会议的所有论文页。`research-analysis` 在摘要缺失严重时只做 title-based preliminary scan，不会输出细粒度技术结论。

## 共享设计

`conference-cvpr` 模仿 `nature-academic-search` 的 router 形态：`SKILL.md` 只负责加载 `manifest.yaml`、读取 `always_load` 核心文件、识别 `axes.workflow`，然后加载 `references/workflows/` 中对应片段。

`skills/_shared/core/` 定义跨会议共用规则：

- `metadata-schema.md`
- `dedup-rules.md`
- `output-contract.md`
- `database-schema.md`
- `research-taxonomy.md`

`skills/_shared/templates/` 定义阅读、分析和灵感生成模板：

- `paper-note.md`
- `conference-report.md`
- `idea-card.md`

## 测试

```bash
python3.11 -m unittest discover -s tests
```

测试覆盖 CVF HTML 解析、字段归一化、SQLite/Excel/Markdown/JSON 导出和 completeness error/warning 分层。
