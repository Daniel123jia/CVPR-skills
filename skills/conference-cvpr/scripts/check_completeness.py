#!/usr/bin/env python3
"""Check completeness of normalized CVPR records."""

from __future__ import annotations

import argparse
import json
import logging
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from _cvpr_common import (
    backup_existing,
    configure_logging,
    default_export_dir,
    default_normalized_path,
    load_json_records,
    write_json_with_backup,
)


def clean_key(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def has_authors(record: dict[str, Any]) -> bool:
    authors = record.get("authors")
    if isinstance(authors, list) and any(str(author).strip() for author in authors):
        return True
    return bool(str(record.get("authors_text") or "").strip())


def add_issue(
    issues: list[dict[str, Any]],
    severity: str,
    issue: str,
    record: dict[str, Any] | None,
    message: str,
    paper_ids: list[str] | None = None,
) -> None:
    item: dict[str, Any] = {
        "severity": severity,
        "issue": issue,
        "message": message,
    }
    if record is not None:
        item["paper_id"] = record.get("paper_id")
        item["title"] = record.get("title")
    if paper_ids is not None:
        item["paper_ids"] = paper_ids
    issues.append(item)


def has_value(record: dict[str, Any], field: str) -> bool:
    value = record.get(field)
    if isinstance(value, list):
        return any(str(item).strip() for item in value)
    return bool(str(value or "").strip())


def field_coverage(records: list[dict[str, Any]], field: str) -> float:
    if not records:
        return 0.0
    present = sum(1 for record in records if has_value(record, field))
    return present / len(records)


def build_coverage_summary(records: list[dict[str, Any]]) -> dict[str, float | int]:
    return {
        "total_papers": len(records),
        "abstract_coverage": field_coverage(records, "abstract"),
        "pdf_url_coverage": field_coverage(records, "pdf_url"),
        "supplementary_url_coverage": field_coverage(records, "supplementary_url"),
        "paper_page_url_coverage": field_coverage(records, "paper_page_url"),
    }


def format_coverage(value: float | int) -> str:
    if isinstance(value, int):
        return str(value)
    return f"{value:.2%}"


def build_markdown_report(
    year: int,
    total: int,
    issues: list[dict[str, Any]],
    coverage: dict[str, float | int],
) -> str:
    error_count = sum(1 for issue in issues if issue["severity"] == "error")
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")
    lines = [
        f"# CVPR {year} Completeness Report",
        "",
        f"- Total papers: {total}",
        f"- Errors: {error_count}",
        f"- Warnings: {warning_count}",
        "",
        "## Coverage Summary",
        "",
        f"- total_papers: {coverage['total_papers']}",
        f"- abstract_coverage: {format_coverage(coverage['abstract_coverage'])}",
        f"- pdf_url_coverage: {format_coverage(coverage['pdf_url_coverage'])}",
        f"- supplementary_url_coverage: {format_coverage(coverage['supplementary_url_coverage'])}",
        f"- paper_page_url_coverage: {format_coverage(coverage['paper_page_url_coverage'])}",
        "",
        "## Issues",
        "",
    ]
    if not issues:
        lines.append("No completeness issues found.")
    else:
        lines.extend(["| severity | issue | paper_id | title | message |", "| --- | --- | --- | --- | --- |"])
        for issue in issues:
            lines.append(
                "| {severity} | {issue} | {paper_id} | {title} | {message} |".format(
                    severity=issue.get("severity", ""),
                    issue=issue.get("issue", ""),
                    paper_id=issue.get("paper_id") or ",".join(issue.get("paper_ids", [])),
                    title=str(issue.get("title") or "").replace("|", "\\|"),
                    message=str(issue.get("message") or "").replace("|", "\\|"),
                )
            )
    return "\n".join(lines) + "\n"


def check_records(input_file: Path, output_dir: Path, year: int) -> dict[str, Any]:
    records = load_json_records(input_file)
    issues: list[dict[str, Any]] = []
    titles: dict[str, list[dict[str, Any]]] = defaultdict(list)
    coverage = build_coverage_summary(records)

    for record in records:
        title_key = clean_key(record.get("title"))
        if title_key:
            titles[title_key].append(record)
        if not title_key:
            add_issue(issues, "error", "missing_title", record, "title is required")
        if not has_authors(record):
            add_issue(issues, "error", "missing_authors", record, "authors is required")
        if not str(record.get("paper_page_url") or "").strip():
            add_issue(issues, "error", "missing_paper_page_url", record, "paper_page_url is required")
        if not str(record.get("abstract") or "").strip():
            add_issue(issues, "warning", "missing_abstract", record, "abstract is missing")
        if not str(record.get("pdf_url") or "").strip():
            add_issue(issues, "warning", "missing_pdf_url", record, "pdf_url is missing")
        if not str(record.get("supplementary_url") or "").strip():
            add_issue(issues, "warning", "missing_supplementary_url", record, "supplementary_url is missing")

    for duplicate_records in titles.values():
        if len(duplicate_records) > 1:
            add_issue(
                issues,
                "error",
                "duplicate_title",
                None,
                f"duplicate title: {duplicate_records[0].get('title')}",
                [str(record.get("paper_id") or "") for record in duplicate_records],
            )

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "completeness_report.md"
    backup_existing(report_path)
    report_path.write_text(build_markdown_report(year, len(records), issues, coverage), encoding="utf-8")
    write_json_with_backup(output_dir / "failed_items.json", issues)

    report = {
        "summary": {
            "year": year,
            "total_papers": len(records),
            "error_count": sum(1 for issue in issues if issue["severity"] == "error"),
            "warning_count": sum(1 for issue in issues if issue["severity"] == "warning"),
            "coverage": coverage,
        },
        "issues": issues,
    }
    logging.info("Completeness check found %s errors and %s warnings", report["summary"]["error_count"], report["summary"]["warning_count"])
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check normalized CVPR paper completeness.")
    parser.add_argument("--year", type=int, required=True, help="CVPR year, for example 2026.")
    parser.add_argument("--input-file", help="Normalized JSON file. Defaults to data/normalized/.../cvpr/YEAR/cvpr_YEAR_normalized.json.")
    parser.add_argument("--output-dir", help="Report directory. Defaults to outputs/computer_vision/cvpr/YEAR/.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    configure_logging("check_completeness", args.year)
    input_file = Path(args.input_file).expanduser().resolve() if args.input_file else default_normalized_path(args.year)
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else default_export_dir(args.year)
    check_records(input_file, output_dir, args.year)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
