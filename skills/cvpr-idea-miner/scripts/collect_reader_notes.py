#!/usr/bin/env python3
"""Collect cvpr-paper-reader note paths into a local JSON index.

This helper scans local Markdown files only. It does not call external APIs,
download PDFs, parse PDFs, or perform OCR.
"""

import argparse
import json
import sys
from pathlib import Path


NOTE_FILES = {
    "reading_note": "reading_note.md",
    "method": "method.md",
    "experiments": "experiments.md",
    "limitations_and_ideas": "limitations_and_ideas.md",
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


def parse_title(markdown_path):
    try:
        for line in markdown_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
            if stripped.lower().startswith("title:"):
                return stripped.split(":", 1)[1].strip()
    except UnicodeDecodeError:
        return None
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
                    "root": str(note_dir),
                    "files": {},
                },
            )
            record["files"][key] = str(path)
            if not record["title"]:
                record["title"] = parse_title(path)

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

