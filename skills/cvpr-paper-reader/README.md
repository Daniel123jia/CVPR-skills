# cvpr-paper-reader

`cvpr-paper-reader` is a single-paper or small-batch CVPR reading skill. It turns paper text, local PDF text, pasted content, a CVF paper page, or `conference-cvpr` metadata into Chinese Markdown reading artifacts.

Use it for:

- 精读这篇 CVPR 论文
- 总结这篇 CVPR paper
- 提取这篇论文的方法
- 整理实验设置和结果
- 生成论文阅读笔记
- 从这篇 CVPR 论文找研究灵感

It does not collect an entire CVPR year, call external enrichment APIs, batch download PDFs, or perform OCR. Use `conference-cvpr` for conference-level CVF collection, export, and completeness checks.

Recommended output path:

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

Optional local PDF text extraction:

```bash
python skills/cvpr-paper-reader/scripts/extract_pdf_text.py --pdf path/to/paper.pdf --output outputs/computer_vision/cvpr/reader/{paper_id}/paper_text.md
```
