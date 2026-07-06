# Dedup Rules

## Collection Deduplication

When `collect_cvpr.py` falls back from `?day=all` to individual day pages, merge records by normalized title:

1. Collapse whitespace.
2. Case-fold the title.
3. Keep the first record order from CVF.
4. Fill missing fields from later duplicates only when the first record has an empty value.

If a title is missing, use `paper_page_url` as the fallback key.

## Completeness Duplicate Check

`check_completeness.py` treats repeated normalized titles as an error. This check is intentionally separate from collection deduplication so imported or manually edited normalized files can still be audited.
