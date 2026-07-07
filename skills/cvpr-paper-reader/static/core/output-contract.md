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
reproduction_checklist.md
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
- `reproduction_checklist.md`: optional reproducibility bridge for users who want to reproduce or improve the paper.

## Numeric Extraction Confidence

`experiments.md` should include this section when experimental numbers are
extracted from PDF text:

```markdown
## Numeric Extraction Confidence

| Table/Figure | Confidence | Reason | Action |
| --- | --- | --- | --- |
| Table 1 | high/medium/low/unavailable | why | use / verify manually / do not summarize |
```

Confidence definitions:

- `high`: numbers and row/column mapping are clear.
- `medium`: numbers are readable, but rows/columns are compressed or partially ambiguous.
- `low`: numbers or row/column mapping are unreliable; require manual PDF checking.
- `unavailable`: figures, supplementary material, or key tables are missing from extracted text.

If confidence is `low`, do not generate strong conclusions from those numbers.
If confidence is `medium`, use cautious wording. If metrics trade off, do not
write simplified claims such as "uniformly best". Every experimental value must
include an evidence anchor, and compressed PDF table extraction must be stated.

## Reproduction Checklist

Use `reproduction_checklist.md` when the user asks to reproduce the paper, wants
to build an improvement, or fulltext contains methods and experiments while
supplement/code details are missing. Do not create a detailed reproduction
checklist without fulltext evidence.

Required sections:

1. Required inputs: dataset, calibration/camera parameters, preprocessing artifacts, model code or compatible implementation, hardware assumption.
2. Paper-backed implementation details: method modules, losses, training strategy, evaluation metrics, baselines.
3. Missing or uncertain details: code link not found, supplementary algorithms missing, optimizer/lr/iterations not found, table extraction uncertainty.
4. Reproduction risks: missing dataset, missing code, table ambiguity, calibration requirement, high hardware requirement.
5. Minimum reproducible target: smallest dataset/scene, baseline to reproduce first, first metric to check, expected evidence source, what not to claim before reproduction.

Clearly separate paper-backed facts from reproduction assumptions. Never invent
code links, hyperparameters, training iterations, external repos, or missing
supplementary details.

If evidence is insufficient, still write the requested file with `Status: evidence_insufficient` and explain what source material is needed. Never silently omit a requested artifact.
