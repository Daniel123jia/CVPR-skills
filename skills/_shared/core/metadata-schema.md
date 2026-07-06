# Shared Metadata Schema

Normalized paper records are JSON objects with stable keys. CVPR v1 fills CVF fields directly and reserves enrichment fields for later sources.

| field | type | required | note |
| --- | --- | --- | --- |
| paper_id | string | yes | `CVPR{year}_{index:06d}` |
| title | string/null | yes | Cleaned title text |
| authors | array[string] | yes | Cleaned author names |
| authors_text | string | yes | `; ` joined authors |
| year | integer | yes | Conference year |
| conference | string | yes | `CVPR` |
| field | string | yes | `computer_vision` |
| source | string | yes | `cvf_openaccess` |
| abstract | string/null | no | Warning if missing |
| paper_page_url | string/null | yes | Error if missing |
| pdf_url | string/null | no | Warning if missing |
| supplementary_url | string/null | no | Warning if missing |
| code_url | string/null | no | Reserved, v1 null |
| project_url | string/null | no | Reserved, v1 null |
| doi | string/null | no | Reserved, v1 null |
| citation_count | integer/null | no | Reserved, v1 null |
| openalex_id | string/null | no | Reserved, v1 null |
| semantic_scholar_id | string/null | no | Reserved, v1 null |
| dblp_key | string/null | no | Reserved, v1 null |
