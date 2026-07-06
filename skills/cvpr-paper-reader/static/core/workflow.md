# Core Workflow

1. Identify the paper entry: title, authors, year, CVF paper page URL, PDF URL, local PDF path, pasted text, or `conference-cvpr` record.
2. Create a stable `paper_id`. Prefer an existing `paper_id`; otherwise derive a readable slug from the title.
3. Gather source material:
   - Use pasted full text or user-provided sections directly.
   - For a local PDF, optionally run `scripts/extract_pdf_text.py`.
   - For a CVF paper page, use the page only as a paper-level entry source. Do not start whole-conference crawling.
4. Assign one evidence level from `evidence-policy.md`.
5. Select one or more workflows from `manifest.yaml`.
6. Load only the selected workflow file(s).
7. Write Markdown artifacts under `outputs/computer_vision/cvpr/reader/{paper_id}/`.
8. At the top of each output, include paper identity, evidence level, source material, and missing-evidence warnings.

## Default Complete Reading Flow

For "精读", "完整阅读笔记", or "read this CVPR paper", use:

```text
paper-summary -> method-extraction -> experiment-table -> limitations-and-ideas -> reading-note
```

Stop or downgrade any workflow that is not allowed by the evidence level. For example, under `abstract_only`, create `summary.md` and optionally a preliminary `reading_note.md`, but do not fabricate `method.md` or `experiments.md`.

## Small-Batch Behavior

For a small number of papers, repeat the single-paper workflow for each paper and keep separate folders. Do not merge them into conference-level analysis unless the user explicitly asks for a cross-paper comparison based only on provided texts.
