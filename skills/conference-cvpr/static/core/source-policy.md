# CVPR Source Policy

## Implemented Source

CVF Open Access:

```text
https://openaccess.thecvf.com/CVPR{year}
https://openaccess.thecvf.com/CVPR{year}?day=all
```

Primary fields:

- `title`
- `authors`
- `paper_page_url`
- `pdf_url`
- `abstract`
- `supplementary_url`

## Fallback

If `?day=all` fails or produces no papers, parse the CVPR home page for links containing `day=` and collect each day page. Exclude links that contain `day=all`, `workshop`, or `tutorial`.

## Exclusions In v1

- Do not collect CVPR workshops or tutorials.
- Do not download PDFs in bulk.
- Do not call OpenAlex, DBLP, Semantic Scholar, Papers With Code, GitHub Search, or other enrichment APIs.
- Do not infer code/project URLs unless they are already present in user-provided data.

Future enrichment notes live in `references/`.
