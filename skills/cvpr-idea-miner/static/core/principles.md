# Principles

- 只做 CVPR 相关研究灵感挖掘；不要扩展到 ICCV、ECCV、NeurIPS、ICML、ACL、AAAI、IJCAI 或其他会议。
- 优先使用 cvpr-paper-reader 生成的 `reading_note.md`、`method.md`、`experiments.md`、`limitations_and_ideas.md`。
- 可以使用 `conference-cvpr` 产出的 normalized JSON、conference report、paper list 作为输入。
- 如果只有 title，只能做粗粒度方向扫描。
- 如果有 title + abstract，可以做 preliminary topic map 和 preliminary idea。
- 如果有 reading notes 或 fulltext-derived notes，才可以做较深入的 gap analysis 和 method recombination。
- 不能把模型推断当成论文事实；将论文事实、用户设想和 agent 启发分开标记。
- 输出要落成 Markdown 文件，优先写入 `outputs/computer_vision/cvpr/ideas/{year}/`。
- 不负责整届论文采集，不负责单篇 PDF 解析，不调用外部 API，不批量下载 PDF，不做 OCR。
