# CVF Open Access Reference

CVPR proceedings are published at:

```text
https://openaccess.thecvf.com/CVPR{year}
```

The collector uses:

```text
https://openaccess.thecvf.com/CVPR{year}?day=all
```

If the all-papers page is unavailable or empty, the collector parses the CVPR home page and follows day links dynamically. Do not hardcode day dates.

Expected HTML patterns:

- Paper titles are usually in `dt.ptitle`.
- The title link points to the paper page.
- Author and resource links usually appear in following `dd` siblings.
- PDF links can be identified by link text or `.pdf` href.
- Supplementary links can be identified by `supp` or `supplement`.

All extracted URLs must be resolved with `urljoin`.
