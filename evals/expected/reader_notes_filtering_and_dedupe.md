# Expected Behavior

- Recommend `collect_reader_notes.py` filters instead of scanning everything blindly.
- Use `--selected-root` when the user wants one local fulltext case.
- Use `--min-evidence-level fulltext` to avoid title_only and abstract_only notes.
- When the same paper title appears as title_only and fulltext, recommend `--dedupe-title prefer_highest_evidence`.
- The generated JSON should include a `filters` field recording paper ids, evidence levels, min evidence level, include-unknown flag, dedupe mode, and selected root.
- Do not call external APIs, download PDFs, or read real `outputs/` in tests.
