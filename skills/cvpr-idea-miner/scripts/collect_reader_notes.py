#!/usr/bin/env python3
"""Collect cvpr-paper-reader note paths into a local JSON index.

This helper scans local Markdown files only. It does not call external APIs,
download PDFs, parse PDFs, or perform OCR.
"""

import argparse
import json
import re
import sys
from pathlib import Path


NOTE_FILES = {
    "reading_note": "reading_note.md",
    "method": "method.md",
    "experiments": "experiments.md",
    "limitations_and_ideas": "limitations_and_ideas.md",
}

TITLE_DECORATIONS = [
    "CVPR Paper Reading Note",
    "Paper Reading Note",
    "论文阅读笔记",
    "中文阅读笔记",
    "Reading Note",
    "阅读笔记",
]

EVIDENCE_LEVELS = {
    "title_only",
    "abstract_only",
    "title_abstract",
    "reader_notes",
    "fulltext",
    "fulltext_notes",
    "user_provided_notes",
    "user_hypothesis",
    "unknown",
}

EVIDENCE_RANK = {
    "unknown": -1,
    "title_only": 0,
    "abstract_only": 1,
    "title_abstract": 1,
    "fulltext": 2,
    "reader_notes": 3,
    "user_provided_notes": 3,
    "fulltext_notes": 4,
}

MIN_EVIDENCE_LEVELS = ["title_only", "abstract_only", "fulltext", "reader_notes", "fulltext_notes"]


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description=(
            "Index cvpr-paper-reader outputs by scanning reading_note.md, "
            "method.md, experiments.md, and limitations_and_ideas.md. "
            "No network, PDF download, or OCR is performed."
        )
    )
    parser.add_argument(
        "--input-dir",
        default=None,
        help="Directory containing per-paper reader outputs; required unless --selected-root is provided.",
    )
    parser.add_argument("--output", required=True, help="Path to write reader_notes_index.json.")
    parser.add_argument(
        "--paper-id",
        action="append",
        default=[],
        help="Only include matching paper_id values. May be passed multiple times.",
    )
    parser.add_argument(
        "--evidence-level",
        action="append",
        default=[],
        help="Only include matching evidence_level values. May be passed multiple times.",
    )
    parser.add_argument(
        "--min-evidence-level",
        choices=MIN_EVIDENCE_LEVELS,
        default=None,
        help=(
            "Keep notes at or above this evidence level using the hierarchy "
            "title_only < abstract_only < fulltext < reader_notes < fulltext_notes."
        ),
    )
    parser.add_argument(
        "--include-unknown-evidence",
        action="store_true",
        help="Allow notes with missing or unknown evidence_level when evidence filters are used.",
    )
    parser.add_argument(
        "--dedupe-title",
        choices=["none", "prefer_highest_evidence"],
        default="none",
        help="Dedupe records with the same normalized title.",
    )
    parser.add_argument(
        "--selected-root",
        default=None,
        help="Only scan one reader note subdirectory instead of the whole input directory.",
    )
    return parser.parse_args(argv)


def clean_title(title):
    title = re.sub(r"\s+", " ", title or "").strip().strip("\"'")
    if not title:
        return None

    for decoration in TITLE_DECORATIONS:
        title = re.sub(
            r"^\s*{}\s*[-:：—–|]*\s*".format(re.escape(decoration)),
            "",
            title,
            flags=re.IGNORECASE,
        )
        if decoration in {"CVPR Paper Reading Note", "Paper Reading Note"}:
            suffix_pattern = r"\s+[-:：—–|]+\s*{}\s*$".format(re.escape(decoration))
        else:
            suffix_pattern = r"\s*[-:：—–|]*\s*{}\s*$".format(re.escape(decoration))
        title = re.sub(suffix_pattern, "", title, flags=re.IGNORECASE)
        title = title.strip(" \t-:：—–|_")

    return title or None


def parse_frontmatter_title(lines):
    if not lines or lines[0].strip() != "---":
        return None

    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return None
        match = re.match(r"(?i)^title\s*:\s*(.+)$", stripped)
        if match:
            return clean_title(match.group(1))
    return None


def parse_explicit_title(lines):
    for line in lines:
        stripped = line.strip()
        match = re.match(r"(?i)^(?:title|paper title)\s*:\s*(.+)$", stripped)
        if match:
            return clean_title(match.group(1))
        match = re.match(r"^论文标题\s*[:：]\s*(.+)$", stripped)
        if match:
            return clean_title(match.group(1))
    return None


def parse_heading_title(lines):
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return clean_title(stripped[2:].strip())
    return None


def parse_title(markdown_path):
    try:
        lines = markdown_path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return None

    return parse_frontmatter_title(lines) or parse_explicit_title(lines) or parse_heading_title(lines)


def parse_evidence_level(markdown_path):
    try:
        lines = markdown_path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return None

    patterns = [
        r"(?i)^\s*-?\s*evidence\s+level\s*:\s*`?([A-Za-z0-9_]+)`?",
        r"(?i)^\s*-?\s*evidence_level\s*:\s*`?([A-Za-z0-9_]+)`?",
        r"^\s*-?\s*证据等级\s*[:：]\s*`?([A-Za-z0-9_]+)`?",
    ]
    for line in lines:
        for pattern in patterns:
            match = re.match(pattern, line.strip())
            if match:
                level = match.group(1).strip().lower()
                return level if level in EVIDENCE_LEVELS else level
    return None


def paper_id_for(note_dir, input_dir):
    if note_dir == input_dir:
        return input_dir.name
    return note_dir.name


def evidence_rank(level):
    return EVIDENCE_RANK.get((level or "unknown").lower(), -1)


def normalize_title_key(title):
    normalized = clean_title(title) or ""
    normalized = normalized.lower()
    normalized = re.sub(r"\s+", " ", normalized).strip()
    normalized = re.sub(r"[\W_]+", "", normalized, flags=re.UNICODE)
    return normalized


def file_count(record):
    return len(record.get("files", {}))


def is_better_duplicate(candidate, existing):
    candidate_rank = evidence_rank(candidate.get("evidence_level"))
    existing_rank = evidence_rank(existing.get("evidence_level"))
    if candidate_rank != existing_rank:
        return candidate_rank > existing_rank

    candidate_file_count = file_count(candidate)
    existing_file_count = file_count(existing)
    if candidate_file_count != existing_file_count:
        return candidate_file_count > existing_file_count

    return candidate.get("_scan_order", 0) < existing.get("_scan_order", 0)


def dedupe_by_title(papers):
    selected = {}
    for record in papers:
        key = normalize_title_key(record.get("title"))
        if not key:
            key = record.get("paper_id")
        if key not in selected or is_better_duplicate(record, selected[key]):
            selected[key] = record
    return list(selected.values())


def record_matches_filters(record, paper_ids, evidence_levels, min_evidence_level, include_unknown_evidence):
    if paper_ids and record["paper_id"] not in paper_ids:
        return False

    record_level = (record.get("evidence_level") or "unknown").lower()
    is_unknown = record_level == "unknown"

    if evidence_levels and record_level not in evidence_levels:
        return False

    if min_evidence_level:
        if is_unknown:
            return include_unknown_evidence
        if evidence_rank(record_level) < evidence_rank(min_evidence_level):
            return False

    return True


def collect_notes(input_dir, selected_root=None):
    input_dir = input_dir.resolve()
    scan_root = selected_root.resolve() if selected_root else input_dir
    papers = {}
    scan_order = 0

    for key, filename in NOTE_FILES.items():
        for path in sorted(scan_root.rglob(filename)):
            note_dir = path.parent.resolve()
            paper_id = paper_id_for(note_dir, scan_root)
            record = papers.setdefault(
                str(note_dir),
                {
                    "paper_id": paper_id,
                    "title": None,
                    "evidence_level": "unknown",
                    "root": str(note_dir),
                    "files": {},
                    "_scan_order": scan_order,
                },
            )
            if record["_scan_order"] == scan_order:
                scan_order += 1
            record["files"][key] = str(path)
            if not record["title"]:
                record["title"] = parse_title(path)
            if record["evidence_level"] == "unknown":
                record["evidence_level"] = parse_evidence_level(path) or "unknown"

    for record in papers.values():
        if not record["title"]:
            record["title"] = record["paper_id"]

    return sorted(papers.values(), key=lambda item: item["paper_id"])


def apply_filters(papers, paper_ids=None, evidence_levels=None, min_evidence_level=None, include_unknown_evidence=False, dedupe_title="none"):
    paper_ids = paper_ids or []
    evidence_levels = [level.lower() for level in (evidence_levels or [])]

    filtered = [
        record
        for record in papers
        if record_matches_filters(record, paper_ids, evidence_levels, min_evidence_level, include_unknown_evidence)
    ]

    if dedupe_title == "prefer_highest_evidence":
        filtered = dedupe_by_title(filtered)

    for record in filtered:
        record.pop("_scan_order", None)

    return sorted(filtered, key=lambda item: item["paper_id"])


def write_index(output_path, input_dir, papers, filters):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_root": str(input_dir.resolve()),
        "filters": filters,
        "note_files": NOTE_FILES,
        "paper_count": len(papers),
        "papers": papers,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    output_path = Path(args.output).expanduser()
    selected_root = Path(args.selected_root).expanduser() if args.selected_root else None
    inferred_input_dir = False

    if not args.input_dir and not selected_root:
        print("Error: Either --input-dir or --selected-root must be provided.", file=sys.stderr)
        return 2

    if selected_root and not selected_root.is_dir():
        print("Error: selected_root does not exist: {}".format(selected_root), file=sys.stderr)
        return 2

    if args.input_dir:
        input_dir = Path(args.input_dir).expanduser()
    else:
        input_dir = selected_root.parent
        inferred_input_dir = True

    if not input_dir.is_dir():
        print("Error: input directory does not exist: {}".format(input_dir), file=sys.stderr)
        return 2

    filters = {
        "paper_ids": args.paper_id,
        "evidence_levels": [level.lower() for level in args.evidence_level],
        "min_evidence_level": args.min_evidence_level,
        "include_unknown_evidence": args.include_unknown_evidence,
        "dedupe_title": args.dedupe_title,
        "selected_root": args.selected_root,
        "input_dir": str(input_dir),
        "inferred_input_dir": inferred_input_dir,
    }

    papers = collect_notes(input_dir, selected_root=selected_root)
    papers = apply_filters(
        papers,
        paper_ids=args.paper_id,
        evidence_levels=args.evidence_level,
        min_evidence_level=args.min_evidence_level,
        include_unknown_evidence=args.include_unknown_evidence,
        dedupe_title=args.dedupe_title,
    )
    write_index(output_path, input_dir, papers, filters)
    print("Indexed {} paper note directories into {}".format(len(papers), output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
