# Expected Route: analyze_low_abstract_coverage

Workflow:

```text
research-analysis
```

Expected behavior:

- Read normalized JSON or SQLite before analysis.
- Compute `abstract_coverage`.
- If `abstract_coverage < 5%`, use `title_only` mode.
- Output only a title-based preliminary scan.
- Include: 当前几乎没有摘要，分析仅基于标题，不适合做细粒度技术结论
- Do not output method details, datasets, ablation, experimental results, code links, citation counts, project URLs, GitHub addresses, or leaderboard claims.
