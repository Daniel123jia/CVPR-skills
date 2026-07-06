# Expected Route: reject_non_cvpr

Workflow:

```text
none
```

Expected behavior:

- State that v1 only supports CVPR main conference papers.
- Refuse to run collection, normalization, export, or analysis for non-CVPR conferences.
- Do not silently switch the request to CVPR.
- Do not create new conference skills or placeholder folders.
