# Shared Database Schema

SQLite is an export artifact for downstream querying. It is not the project center.

CVPR SQLite database file:

```text
outputs/computer_vision/cvpr/{year}/cvpr_{year}_papers.sqlite
```

Table name:

```sql
papers
```

Columns:

```text
paper_id
title
authors
authors_text
year
conference
field
source
abstract
pdf_url
paper_page_url
supplementary_url
code_url
project_url
doi
citation_count
openalex_id
semantic_scholar_id
dblp_key
```

`authors` is stored as `; ` joined text for spreadsheet/database readability. The normalized JSON remains the authoritative structured representation.
