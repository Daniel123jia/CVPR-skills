#!/usr/bin/env python3
"""Extract text from a local PDF into a Markdown file.

This helper intentionally does not perform OCR. Scanned PDFs or pages without
embedded text will fail clearly instead of generating guessed content.
"""

import argparse
import sys
from pathlib import Path


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Extract embedded text from a local PDF into Markdown. No OCR is performed.",
    )
    parser.add_argument("--pdf", required=True, help="Path to the local PDF file.")
    parser.add_argument("--output", required=True, help="Path to write the extracted Markdown text.")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional maximum number of pages to extract, starting from page 1.",
    )
    return parser.parse_args(argv)


def load_pdf_reader():
    try:
        from pypdf import PdfReader
    except Exception as exc:  # pragma: no cover - depends on local environment
        raise RuntimeError("Missing dependency pypdf. Install with: pip install -r requirements.txt") from exc
    return PdfReader


def extract_text(pdf_path, max_pages=None):
    PdfReader = load_pdf_reader()
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        raise RuntimeError("Could not parse PDF: {}".format(exc)) from exc

    pages = reader.pages
    if max_pages is not None:
        if max_pages <= 0:
            raise RuntimeError("--max-pages must be a positive integer")
        pages = pages[:max_pages]

    chunks = []
    failed_pages = []
    for index, page in enumerate(pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            failed_pages.append(index)
            continue
        text = text.strip()
        if text:
            chunks.append((index, text))

    if not chunks:
        raise RuntimeError(
            "No embedded text could be extracted. The PDF may be scanned, encrypted, or unsupported. OCR is not supported."
        )

    return chunks, failed_pages, len(reader.pages)


def write_markdown(output_path, pdf_path, chunks, failed_pages, total_pages):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Extracted PDF Text",
        "",
        "- Source PDF: `{}`".format(pdf_path),
        "- Total pages: {}".format(total_pages),
        "- OCR: not performed",
    ]
    if failed_pages:
        lines.append("- Pages skipped due to extraction errors: {}".format(", ".join(map(str, failed_pages))))
    lines.append("")

    for page_number, text in chunks:
        lines.extend(
            [
                "## Page {}".format(page_number),
                "",
                text,
                "",
            ]
        )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    pdf_path = Path(args.pdf).expanduser()
    output_path = Path(args.output).expanduser()

    if not pdf_path.is_file():
        print("Error: PDF file does not exist: {}".format(pdf_path), file=sys.stderr)
        return 2

    try:
        chunks, failed_pages, total_pages = extract_text(pdf_path, args.max_pages)
        write_markdown(output_path, pdf_path, chunks, failed_pages, total_pages)
    except RuntimeError as exc:
        print("Error: {}".format(exc), file=sys.stderr)
        return 2

    print("Wrote extracted text to {}".format(output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
