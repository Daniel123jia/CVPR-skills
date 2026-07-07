# Expected Behavior

- Recommend `collect_reader_notes.py` filters instead of scanning everything blindly.
- Use a selected-root-only command when the user wants one local fulltext case; `--input-dir` is not required in that scenario.
- Use `--input-dir` when scanning the whole reader root.
- `--selected-root` should automatically infer the parent `input_dir`.
- Use `--min-evidence-level fulltext` to avoid title_only and abstract_only notes.
- When the same paper title appears as title_only and fulltext, recommend `--dedupe-title prefer_highest_evidence`.
- The generated JSON should include a `filters` field recording paper ids, evidence levels, min evidence level, include-unknown flag, dedupe mode, selected root, input dir, and `inferred_input_dir`.
- Do not call external APIs, download PDFs, or read real `outputs/` in tests.
