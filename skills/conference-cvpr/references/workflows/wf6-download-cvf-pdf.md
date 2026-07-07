# Workflow: Explicit CVF PDF Download

Use this workflow only after an explicit user request to download selected CVPR papers. Keep it outside the default collection pipeline.

Supported selectors are `paper_id`, title, and direct CVF `pdf_url`. The recommended sequence is dry-run first, then a real download only after the user confirms the selected paper and output path.

## Procedure

1. Read local normalized or exported JSON metadata when selection uses `paper_id` or title.
2. Recommend `--dry-run` before the first download.
3. Require a unique normalized title match. If fuzzy lookup yields multiple candidates, show them and require `paper_id`.
4. Accept only HTTPS CVF Open Access PDF URLs on the exact `openaccess.thecvf.com` hostname.
5. Download one paper by default. Require `--allow-batch`, `--limit`, and `--sleep` for repeated `--paper-id` values.
6. Keep PDFs and `.pdf.json` sidecars under ignored runtime output directories.
7. Run `extract_pdf_text.py` separately when the user wants fulltext reading. Do not perform OCR or automatically invoke reader or idea-miner workflows.

## Recommended Commands

```bash
python skills/conference-cvpr/scripts/download_cvf_pdf.py \
  --metadata outputs/computer_vision/cvpr/2026/cvpr_2026_papers.json \
  --paper-id CVPR2026_000002 \
  --output-dir outputs/computer_vision/cvpr/pdfs/2026 \
  --dry-run

python skills/conference-cvpr/scripts/download_cvf_pdf.py \
  --metadata outputs/computer_vision/cvpr/2026/cvpr_2026_papers.json \
  --title "DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization" \
  --output-dir outputs/computer_vision/cvpr/pdfs/2026 \
  --dry-run

python skills/conference-cvpr/scripts/download_cvf_pdf.py \
  --pdf-url https://openaccess.thecvf.com/content/CVPR2026/papers/example.pdf \
  --paper-id CVPR2026_000002 \
  --output-dir outputs/computer_vision/cvpr/pdfs/2026 \
  --dry-run

python skills/cvpr-paper-reader/scripts/extract_pdf_text.py \
  --pdf outputs/computer_vision/cvpr/pdfs/2026/CVPR2026_000002.pdf \
  --output outputs/computer_vision/cvpr/reader/CVPR2026_000002/paper_text.md
```

The download enables local fulltext evidence. It does not change or replace the paper-reader evidence policy.

Downloaded PDFs, sidecar JSON, checksums, and logs are runtime artifacts. Do not commit them. No automatic full-conference PDF download is allowed.
