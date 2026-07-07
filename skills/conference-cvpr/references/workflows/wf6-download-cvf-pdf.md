# Workflow: Explicit CVF PDF Download

Use this workflow only after an explicit user request to download selected CVPR papers. Keep it outside the default collection pipeline.

## Procedure

1. Read local normalized or exported JSON metadata when selection uses `paper_id` or title.
2. Recommend `--dry-run` before the first download.
3. Require a unique normalized title match. If fuzzy lookup yields multiple candidates, show them and require `paper_id`.
4. Accept only HTTPS PDF URLs on the exact `openaccess.thecvf.com` hostname.
5. Download one paper by default. Require `--allow-batch`, `--limit`, and `--sleep` for repeated `--paper-id` values.
6. Keep PDFs and `.pdf.json` sidecars under ignored runtime output directories.
7. Run `extract_pdf_text.py` separately when the user wants fulltext reading. Do not perform OCR or automatically invoke reader or idea-miner workflows.

## Recommended Commands

```bash
python skills/conference-cvpr/scripts/download_cvf_pdf.py \
  --metadata data/normalized/computer_vision/cvpr/2026/cvpr_2026_normalized.json \
  --paper-id CVPR2026_000002 \
  --output-dir outputs/computer_vision/cvpr/pdfs/2026 \
  --dry-run

python skills/conference-cvpr/scripts/download_cvf_pdf.py \
  --metadata data/normalized/computer_vision/cvpr/2026/cvpr_2026_normalized.json \
  --paper-id CVPR2026_000002 \
  --output-dir outputs/computer_vision/cvpr/pdfs/2026

python skills/cvpr-paper-reader/scripts/extract_pdf_text.py \
  --pdf outputs/computer_vision/cvpr/pdfs/2026/CVPR2026_000002.pdf \
  --output outputs/computer_vision/cvpr/reader/CVPR2026_000002/paper_text.md
```

The download enables local fulltext evidence. It does not change or replace the paper-reader evidence policy.
