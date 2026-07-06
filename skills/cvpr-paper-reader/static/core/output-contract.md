# Output Contract

Recommended root:

```text
outputs/computer_vision/cvpr/reader/{paper_id}/
```

Recommended files:

```text
summary.md
method.md
experiments.md
limitations_and_ideas.md
reading_note.md
```

Every Markdown output must start with:

```markdown
# {Paper Title} — {Artifact Name}

- Conference: CVPR
- Evidence level: {title_only | abstract_only | fulltext | user_provided_notes}
- Source material: {pasted text | local PDF text | CVF page | conference-cvpr metadata | user notes}
- Paper page: {URL or Not provided}
- PDF: {URL/path or Not provided}
- Status: {complete | preliminary | evidence_insufficient}
```

Use Chinese for the main content unless the user asks otherwise.

## File Purposes

- `summary.md`: paper-level summary and contribution overview.
- `method.md`: method framework, modules, process, formulas, and implementation-relevant details.
- `experiments.md`: datasets, metrics, baselines, main results, and ablations.
- `limitations_and_ideas.md`: limitations, risks, missing evidence, and grounded research ideas.
- `reading_note.md`: integrated Chinese reading note that links or summarizes the other artifacts.

If evidence is insufficient, still write the requested file with `Status: evidence_insufficient` and explain what source material is needed. Never silently omit a requested artifact.
