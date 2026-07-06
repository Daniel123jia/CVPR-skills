# Expected Route: collect_cvpr_2026

Workflow:

```text
collect-cvf -> normalize-metadata -> export-artifacts -> completeness-check
```

Expected behavior:

- Load `manifest.yaml` and `always_load` core files.
- Load WF1, WF2, WF3, and WF4 workflow fragments.
- Run the deterministic scripts in order.
- Write raw JSON, normalized JSON, exports, `completeness_report.md`, and `failed_items.json`.
- Do not collect workshops, call external APIs, or download PDFs.
