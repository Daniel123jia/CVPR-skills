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


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description=(
            "Index cvpr-paper-reader outputs by scanning reading_note.md, "
            "method.md, experiments.md, and limitations_and_ideas.md. "
            "No network, PDF download, or OCR is performed."
        )
    )
    parser.add_argument("--input-dir", required=True, help="Directory containing per-paper reader outputs.")
    parser.add_argument("--output", required=True, help="Path to write reader_notes_index.json.")
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


def collect_notes(input_dir):
    input_dir = input_dir.resolve()
    papers = {}

    for key, filename in NOTE_FILES.items():
        for path in sorted(input_dir.rglob(filename)):
            note_dir = path.parent.resolve()
            paper_id = paper_id_for(note_dir, input_dir)
            record = papers.setdefault(
                str(note_dir),
                {
                    "paper_id": paper_id,
                    "title": None,
                    "evidence_level": "unknown",
                    "root": str(note_dir),
                    "files": {},
                },
            )
            record["files"][key] = str(path)
            if not record["title"]:
                record["title"] = parse_title(path)
            if record["evidence_level"] == "unknown":
                record["evidence_level"] = parse_evidence_level(path) or "unknown"

    for record in papers.values():
        if not record["title"]:
            record["title"] = record["paper_id"]

    return sorted(papers.values(), key=lambda item: item["paper_id"])


def write_index(output_path, input_dir, papers):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_root": str(input_dir.resolve()),
        "note_files": NOTE_FILES,
        "paper_count": len(papers),
        "papers": papers,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    input_dir = Path(args.input_dir).expanduser()
    output_path = Path(args.output).expanduser()

    if not input_dir.is_dir():
        print("Error: input directory does not exist: {}".format(input_dir), file=sys.stderr)
        return 2

    papers = collect_notes(input_dir)
    write_index(output_path, input_dir, papers)
    print("Indexed {} paper note directories into {}".format(len(papers), output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
