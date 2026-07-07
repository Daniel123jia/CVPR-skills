# Expected Route: Optional CVF PDF Download

- Route to `conference-cvpr` -> `download-cvf-pdf`.
- State that PDF download is optional and explicit; metadata collection continues to store `pdf_url` without downloading files.
- Resolve the local metadata title with an exact normalized match first. If fuzzy matching returns multiple candidates, list them and require the user to specify `paper_id` without downloading.
- Recommend `download_cvf_pdf.py --dry-run` before the real command.
- Allow only CVF Open Access URLs on the exact `openaccess.thecvf.com` HTTPS hostname.
- State: No automatic full-conference PDF download.
- State: No code repository download.
- Write the selected `.pdf` and `.pdf.json` sidecar under ignored `outputs/`; these are runtime artifacts and must not be committed.
- Run `extract_pdf_text.py` as a separate second step. Do not perform OCR or automatically run the entire reader and idea-miner chain.
- Explain that downloading enables local fulltext reading but does not replace the evidence policy: paper facts still require support from the extracted text, and missing code, experiments, or hyperparameters must not be invented.
