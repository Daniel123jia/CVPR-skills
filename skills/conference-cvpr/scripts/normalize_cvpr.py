#!/usr/bin/env python3
"""Normalize raw CVPR records into the shared paper schema."""

from __future__ import annotations

import argparse
import logging
import re
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from _cvpr_common import (
    configure_logging,
    default_normalized_path,
    default_raw_path,
    load_json_records,
    output_file_in_dir,
    write_json_with_backup,
)


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", unescape(str(value))).strip()


def clean_url(value: Any, base_url: str) -> str | None:
    text = clean_text(value)
    if not text:
        return None
    return urljoin(base_url, text)


def clean_authors(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        candidates = value
    else:
        candidates = re.split(r"\s*(?:,|;)\s*", str(value))
    authors = [clean_text(author) for author in candidates]
    return [author for author in authors if author]


def normalize_records(raw_records: list[dict[str, Any]], year: int, base_url: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_records, start=1):
        authors = clean_authors(raw.get("authors"))
        records.append(
            {
                "paper_id": f"CVPR{year}_{index:06d}",
                "title": clean_text(raw.get("title")) or None,
                "authors": authors,
                "authors_text": "; ".join(authors),
                "year": year,
                "conference": "CVPR",
                "field": "computer_vision",
                "source": "cvf_openaccess",
                "abstract": clean_text(raw.get("abstract")) or None,
                "paper_page_url": clean_url(raw.get("paper_page_url"), base_url),
                "pdf_url": clean_url(raw.get("pdf_url"), base_url),
                "supplementary_url": clean_url(raw.get("supplementary_url"), base_url),
                "code_url": None,
                "project_url": None,
                "doi": None,
                "citation_count": None,
                "openalex_id": None,
                "semantic_scholar_id": None,
                "dblp_key": None,
            }
        )
    return records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Normalize raw CVPR JSON into the shared paper schema.")
    parser.add_argument("--year", type=int, required=True, help="CVPR year, for example 2026.")
    parser.add_argument("--input-file", help="Raw JSON file. Defaults to data/raw/.../cvpr/YEAR/cvpr_YEAR_raw.json.")
    parser.add_argument("--output-dir", help="Directory for cvpr_YEAR_normalized.json. Defaults to data/normalized/.../cvpr/YEAR/.")
    parser.add_argument("--base-url", help="Base URL for relative CVF links. Defaults to https://openaccess.thecvf.com/CVPRYEAR.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    configure_logging("normalize_cvpr", args.year)
    input_path = Path(args.input_file).expanduser().resolve() if args.input_file else default_raw_path(args.year)
    output_path = output_file_in_dir(args.output_dir, default_normalized_path(args.year))
    base_url = args.base_url or f"https://openaccess.thecvf.com/CVPR{args.year}"
    raw_records = load_json_records(input_path)
    records = normalize_records(raw_records, args.year, base_url)
    backup_path = write_json_with_backup(output_path, records)
    if backup_path:
        logging.info("Backed up existing output to %s", backup_path)
    logging.info("Wrote %s normalized CVPR papers to %s", len(records), output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
