# Expected Route: export_cvpr_excel

Workflow:

```text
export-artifacts
```

Expected behavior:

- Load the export workflow fragment.
- Read normalized JSON from the default path or the user-provided input file.
- Run `export_cvpr.py`.
- Produce Excel, SQLite, Markdown, and JSON exports under `outputs/computer_vision/cvpr/{year}/`.
- Keep SQLite table name `papers`.
