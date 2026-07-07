# Clean Clone Walkthrough

This walkthrough verifies the repository from a clean clone to a first local CVPR run. It does not require external enrichment APIs, a live PDF download, or committed runtime artifacts.

## 1. Clone The Repository

```bash
git clone https://github.com/Daniel123jia/CVPR-skills.git
cd CVPR-skills
```

## 2. Create A Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

If your system does not have `python3.11`, use Python 3.10+.

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run Local Tests

```bash
python -m unittest discover -s tests
```

The tests use local fixtures and documentation checks. They do not run real network collection and do not require a PDF.

## 5. Run A Small CVPR Sample

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026 --limit 5
```

This writes local runtime artifacts under:

```text
data/
outputs/
logs/
```

These are generated runtime artifacts and must not be committed to the repository.

## 6. Optionally Download One Selected PDF

The optional PDF download is explicit and outside the default pipeline. Preview one metadata match first:

```bash
python skills/conference-cvpr/scripts/download_cvf_pdf.py \
  --metadata data/normalized/computer_vision/cvpr/2026/cvpr_2026_normalized.json \
  --paper-id CVPR2026_000002 \
  --output-dir outputs/computer_vision/cvpr/pdfs/2026 \
  --dry-run
```

Remove `--dry-run` to download that selected CVF PDF. The script accepts only `openaccess.thecvf.com` PDF URLs and never downloads the full conference automatically. Keep the PDF and sidecar out of git.

## 7. Enter The Reader Flow

Use `cvpr-paper-reader` when you want paper-level notes:

- `title_only`: title and metadata only.
- `abstract_only`: title plus abstract.
- `fulltext`: extracted text from a user-provided local PDF or pasted paper text.

Use a PDF already on disk or one explicitly selected through the optional downloader. The project must not automatically download PDFs.

For local fulltext validation, first extract embedded PDF text:

```bash
python skills/cvpr-paper-reader/scripts/extract_pdf_text.py --pdf outputs/computer_vision/cvpr/pdfs/2026/CVPR2026_000002.pdf --output outputs/computer_vision/cvpr/reader/CVPR2026_000002/paper_text.md
```

Then generate:

```text
outputs/computer_vision/cvpr/reader/{paper_id}/reading_note.md
outputs/computer_vision/cvpr/reader/{paper_id}/method.md
outputs/computer_vision/cvpr/reader/{paper_id}/experiments.md
outputs/computer_vision/cvpr/reader/{paper_id}/limitations_and_ideas.md
```

## 8. Enter The Idea-Miner Flow

Use `cvpr-idea-miner` after reader notes exist:

```bash
python skills/cvpr-idea-miner/scripts/collect_reader_notes.py \
  --selected-root outputs/computer_vision/cvpr/reader/{paper_id} \
  --min-evidence-level fulltext \
  --dedupe-title prefer_highest_evidence \
  --output outputs/computer_vision/cvpr/ideas/{paper_id}/reader_notes_index.json
```

For whole-reader-root scans, pass `--input-dir outputs/computer_vision/cvpr/reader`. For a single paper folder, `--selected-root` automatically infers the parent reader root.

Then generate topic maps, gap analysis, idea cards, and experiment plans from the indexed notes. Keep paper facts separate from agent hypotheses, and keep generated outputs out of git.
