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
reproduction_checklist.md
```

`reproduction_checklist.md` is an optional reader artifact. Use it when
fulltext evidence is available and the user asks to reproduce or improve the
paper, provided `paper_text.md` contains enough method and experiment setup.
Record missing code, supplementary material, key hyperparameters, datasets, or
training details as evidence gaps. Never invent a code link, optimizer,
learning rate, training iterations, external repository, or unavailable
dataset. When present, `cvpr-idea-miner` may use this artifact to ground
feasibility assessment and experiment planning.

For `experiments.md`, include a `Numeric Extraction Confidence` section when
numbers come from parsed PDF text. Low-confidence table extraction must not
support strong conclusions; medium confidence requires cautious wording.

Optional local PDF text extraction:

```bash
python skills/cvpr-paper-reader/scripts/extract_pdf_text.py --pdf path/to/paper.pdf --output outputs/computer_vision/cvpr/reader/{paper_id}/paper_text.md
```
