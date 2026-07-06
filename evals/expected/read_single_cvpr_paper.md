# Expected Route: read_single_cvpr_paper

- Skill: `cvpr-paper-reader`
- Evidence level: `fulltext`
- Workflows: `paper-summary -> method-extraction -> experiment-table -> limitations-and-ideas -> reading-note`
- Output path: `outputs/computer_vision/cvpr/reader/{paper_id}/`
- Output files: `summary.md`, `method.md`, `experiments.md`, `limitations_and_ideas.md`, `reading_note.md`

Expected behavior:

- 可以完整精读，因为输入包含全文片段。
- 方法、实验、局限性和研究灵感必须锚定在给定全文内容上。
- 不调用外部 enrichment API，不批量下载 PDF，不补充未给出的代码链接、项目主页或引用量。
