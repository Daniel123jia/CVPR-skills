# Expected Behavior: fulltext_no_hallucination

- Use evidence level `fulltext`.
- Method and experiment extraction is allowed only when supported by provided fulltext snippets.
- Every method and experiment claim must include `evidence source`.
- Missing code links, citation counts, leaderboard entries, datasets, baselines, ablations, or experimental results must be written as `Not found in provided material`.
- `cvpr-idea-miner` may generate idea cards, but each new idea must be marked as `agent hypothesis`.
- An idea must not be described as `论文已有结论` unless the fulltext explicitly states it.
