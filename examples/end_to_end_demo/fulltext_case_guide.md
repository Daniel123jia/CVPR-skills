# Fulltext Local Validation Guide

This guide describes a local fulltext acceptance case for the existing three CVPR skills. It is documentation only. Do not commit the PDF, extracted text, generated outputs, Excel files, SQLite files, or logs.

## 1. Prepare A Local CVPR PDF

Manually prepare one local CVPR PDF that you already have permission to use. The PDF 不提交仓库.

Rules:

- Do not fetch papers through automation.
- Do not use external enrichment services.
- Do not add the PDF to git.
- Keep the PDF path outside committed source, or under an ignored runtime directory.

## 2. Extract Embedded Text

Use `cvpr-paper-reader`'s local helper. It extracts embedded text only and does not perform OCR.

```bash
python skills/cvpr-paper-reader/scripts/extract_pdf_text.py --pdf path/to/local_cvpr_paper.pdf --output outputs/computer_vision/cvpr/reader/{paper_id}/paper_text.md
```

If `extract_pdf_text.py` reports `Missing dependency pypdf` or a `pypdf` compatibility error, run `python -m pip install -r requirements.txt` and confirm the installed `pypdf` version is within `>=3.17.4,<4.0`.

Expected local artifact:

```text
outputs/computer_vision/cvpr/reader/{paper_id}/paper_text.md
```

## 3. Generate Fulltext Reader Notes

Use `cvpr-paper-reader` on the extracted `paper_text.md` and generate:

```text
outputs/computer_vision/cvpr/reader/{paper_id}/reading_note.md
outputs/computer_vision/cvpr/reader/{paper_id}/method.md
outputs/computer_vision/cvpr/reader/{paper_id}/experiments.md
outputs/computer_vision/cvpr/reader/{paper_id}/limitations_and_ideas.md
```

Required reader-note checks:

- Mark `Evidence level: fulltext`.
- Cite `paper_text.md` as the evidence source.
- Keep method, experiment, and limitation claims tied to text evidence.
- Use `Not found in provided material` or `未在给定材料中找到` for missing fields.

## 4. Generate Idea Cards

Collect the reader notes:

```bash
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py \
  --input-dir outputs/computer_vision/cvpr/reader \
  --selected-root outputs/computer_vision/cvpr/reader/{paper_id} \
  --min-evidence-level fulltext \
  --dedupe-title prefer_highest_evidence \
  --output outputs/computer_vision/cvpr/ideas/{paper_id}/reader_notes_index.json
```

Then use `cvpr-idea-miner` to generate local idea mining artifacts such as:

```text
outputs/computer_vision/cvpr/ideas/{year}/topic_map.md
outputs/computer_vision/cvpr/ideas/{year}/gap_analysis.md
outputs/computer_vision/cvpr/ideas/{year}/idea_cards.md
outputs/computer_vision/cvpr/ideas/{year}/experiment_plan.md
```

Each `idea_cards.md` entry must include:

- evidence level
- evidence source
- risk
- first runnable experiment
- clear separation between paper facts and agent hypothesis

## 5. Manual Anti-Hallucination Gate

Before accepting the fulltext case, manually check:

- No fabricated 代码链接.
- No fabricated 引用量.
- No fabricated leaderboard.
- No 未出现的数据集.
- No 未出现的实验结果.
- No unsupported ablation or baseline claims.
- Every method, experiment, limitation, and idea claim has a visible source.

## 6. Do Not Commit Runtime Artifacts

Do not commit:

- `outputs/`
- `data/`
- `logs/`
- PDF
- Excel
- SQLite
- extracted `paper_text.md`

Only this guide and lightweight tests belong in the repository.
