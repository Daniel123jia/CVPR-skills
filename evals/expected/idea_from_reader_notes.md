# Expected Route: Idea From Reader Notes

- Skill: `cvpr-idea-miner`
- Workflow: `gap-analysis -> idea-cards`
- Evidence level: `reader_notes`
- Output file: `outputs/computer_vision/cvpr/ideas/{year}/idea_cards.md`

Expected behavior:

- Generate structured idea cards because reader notes are available.
- Each card includes `idea_id`, title, motivation, evidence source, related papers / paper_ids, proposed method, expected contribution, experiment design, required datasets, baseline candidates, risk, first runnable experiment, and evidence level.
- Mark missing datasets or baselines as `Not found in provided material` when notes do not contain them.
- Keep paper facts separate from proposed ideas.

