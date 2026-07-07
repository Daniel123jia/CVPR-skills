#!/usr/bin/env python3
"""Explicitly download selected CVPR PDFs from CVF Open Access metadata."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlparse

import requests


DOWNLOADER_VERSION = "1.5.0"
CVF_HOSTNAME = "openaccess.thecvf.com"
DEFAULT_MAX_BYTES = 100 * 1024 * 1024
DEFAULT_TIMEOUT = 30.0
FUZZY_THRESHOLD = 0.55
FUZZY_CANDIDATE_LIMIT = 8


class DownloadError(RuntimeError):
    """Base error for safe, user-visible download failures."""


class SelectionError(DownloadError):
    """Raised when local metadata cannot select exactly one intended paper."""


class UrlPolicyError(DownloadError):
    """Raised when a URL is outside the CVF PDF allowlist."""


class UsageError(DownloadError):
    """Raised when CLI arguments violate the explicit-download contract."""


def normalize_title(value: Any) -> str:
    text = unicodedata.normalize("NFKC", html.unescape(str(value or "")))
    text = re.sub(r"[‐‑‒–—−]", "-", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def _candidate_message(candidates: Iterable[Dict[str, Any]]) -> str:
    lines = []
    for record in candidates:
        lines.append("- {}: {}".format(record.get("paper_id") or "<missing>", record.get("title") or "<untitled>"))
    return "\n".join(lines)


def select_records(
    records: List[Dict[str, Any]],
    paper_ids: Optional[List[str]] = None,
    title: Optional[str] = None,
) -> List[Dict[str, Any]]:
    if bool(paper_ids) == bool(title):
        raise SelectionError("Select papers with either --paper-id or --title, not both.")

    if paper_ids:
        selected = []
        for paper_id in paper_ids:
            matches = [record for record in records if str(record.get("paper_id") or "") == paper_id]
            if not matches:
                raise SelectionError("paper_id not found: {}".format(paper_id))
            if len(matches) > 1:
                raise SelectionError("paper_id is not unique in metadata: {}".format(paper_id))
            if not matches[0].get("pdf_url"):
                raise SelectionError("paper_id has no pdf_url: {}".format(paper_id))
            selected.append(matches[0])
        return selected

    query = normalize_title(title)
    if not query:
        raise SelectionError("--title must not be empty")

    exact = [record for record in records if normalize_title(record.get("title")) == query]
    if len(exact) == 1:
        if not exact[0].get("pdf_url"):
            raise SelectionError("matched title has no pdf_url: {}".format(exact[0].get("paper_id")))
        return exact
    if len(exact) > 1:
        raise SelectionError(
            "Multiple exact title matches; specify --paper-id:\n{}".format(_candidate_message(exact))
        )

    scored = []
    for record in records:
        candidate = normalize_title(record.get("title"))
        if not candidate:
            continue
        score = SequenceMatcher(None, query, candidate).ratio()
        if score >= FUZZY_THRESHOLD:
            scored.append((score, record))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("paper_id") or "")))
    candidates = [record for _, record in scored[:FUZZY_CANDIDATE_LIMIT]]

    if not candidates:
        raise SelectionError("No title match found; search metadata and specify --paper-id.")
    if len(candidates) > 1:
        raise SelectionError(
            "Multiple fuzzy title candidates; specify --paper-id:\n{}".format(_candidate_message(candidates))
        )
    if not candidates[0].get("pdf_url"):
        raise SelectionError("matched title has no pdf_url: {}".format(candidates[0].get("paper_id")))
    return candidates


def validate_cvf_pdf_url(url: str) -> str:
    text = str(url or "").strip()
    parsed = urlparse(text)
    try:
        port = parsed.port
    except ValueError as exc:
        raise UrlPolicyError("Invalid URL port: {}".format(exc))

    if parsed.scheme.lower() != "https":
        raise UrlPolicyError("Only HTTPS CVF PDF URLs are allowed.")
    if (parsed.hostname or "").lower() != CVF_HOSTNAME:
        raise UrlPolicyError("Only openaccess.thecvf.com PDF URLs are allowed.")
    if parsed.username or parsed.password or port not in (None, 443):
        raise UrlPolicyError("CVF URLs must not contain credentials or a non-default port.")
    if not parsed.path.lower().endswith(".pdf"):
        raise UrlPolicyError("The CVF URL path must end with .pdf.")
    if parsed.fragment:
        raise UrlPolicyError("CVF PDF URLs must not contain fragments.")
    return text


def sanitize_paper_id(paper_id: Any) -> str:
    text = unicodedata.normalize("NFKC", str(paper_id or "")).strip()
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text)
    text = text.strip("._-")[:120]
    if not text:
        raise SelectionError("paper_id does not contain a safe filename token")
    return text


def _remove_if_present(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def _write_json_atomic(path: Path, payload: Dict[str, Any]) -> None:
    temporary = path.with_name(path.name + ".part")
    _remove_if_present(temporary)
    try:
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
    finally:
        _remove_if_present(temporary)


def download_record(
    record: Dict[str, Any],
    output_dir: Path,
    session: Optional[Any] = None,
    timeout: float = DEFAULT_TIMEOUT,
    max_bytes: int = DEFAULT_MAX_BYTES,
    force: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    paper_id = str(record.get("paper_id") or "")
    safe_id = sanitize_paper_id(paper_id)
    source_url = validate_cvf_pdf_url(str(record.get("pdf_url") or ""))
    output_dir = Path(output_dir).expanduser()
    target = output_dir / "{}.pdf".format(safe_id)
    sidecar = output_dir / "{}.pdf.json".format(safe_id)

    base_result = {
        "paper_id": paper_id,
        "title": record.get("title"),
        "source_url": source_url,
        "saved_path": str(target),
    }
    if dry_run:
        return dict(base_result, status="dry_run")
    if target.exists() and not force:
        return dict(base_result, status="skipped")
    if timeout <= 0:
        raise UsageError("timeout must be positive")
    if max_bytes <= 0:
        raise UsageError("max file size must be positive")

    client = session or requests.Session()
    output_dir.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + ".part")
    _remove_if_present(partial)

    digest = hashlib.sha256()
    total = 0
    final_url = source_url
    try:
        with client.get(source_url, stream=True, timeout=timeout, allow_redirects=True) as response:
            response.raise_for_status()
            final_url = validate_cvf_pdf_url(str(response.url or source_url))
            declared = response.headers.get("Content-Length")
            if declared:
                try:
                    declared_bytes = int(declared)
                except (TypeError, ValueError):
                    declared_bytes = None
                if declared_bytes is not None and declared_bytes > max_bytes:
                    raise DownloadError(
                        "PDF exceeds max file size: {} > {} bytes".format(declared_bytes, max_bytes)
                    )

            with partial.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=65536):
                    if not chunk:
                        continue
                    total += len(chunk)
                    if total > max_bytes:
                        raise DownloadError("PDF exceeds max file size while streaming.")
                    digest.update(chunk)
                    handle.write(chunk)
        partial.replace(target)
    finally:
        _remove_if_present(partial)
        if session is None:
            client.close()

    downloaded_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    payload = {
        "paper_id": paper_id,
        "title": record.get("title"),
        "source_url": final_url,
        "saved_path": str(target),
        "sha256": digest.hexdigest(),
        "bytes": total,
        "downloaded_at": downloaded_at,
        "downloader_version": DOWNLOADER_VERSION,
        "source": "cvf_openaccess",
    }
    _write_json_atomic(sidecar, payload)
    return dict(payload, status="downloaded")


def load_json_records(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = data.get("papers", []) if isinstance(data, dict) else data
    if not isinstance(records, list):
        raise SelectionError("Expected a JSON list or an object containing a papers list: {}".format(path))
    return [record for record in records if isinstance(record, dict)]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Explicitly download selected CVF Open Access PDFs from local CVPR metadata."
    )
    parser.add_argument("--metadata", help="Local normalized or exported CVPR JSON metadata.")
    parser.add_argument("--paper-id", action="append", help="Paper ID to select; repeat only with explicit batch flags.")
    parser.add_argument("--title", help="Paper title; exact normalized match is preferred before fuzzy lookup.")
    parser.add_argument("--pdf-url", help="Direct CVF Open Access PDF URL; requires exactly one --paper-id.")
    parser.add_argument("--output-dir", required=True, help="Directory for ignored PDF runtime artifacts.")
    parser.add_argument("--allow-batch", action="store_true", help="Explicitly allow repeated --paper-id values.")
    parser.add_argument("--limit", type=int, help="Maximum batch items; required with --allow-batch.")
    parser.add_argument("--sleep", type=float, help="Seconds between batch items; required with --allow-batch.")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Request timeout in seconds (default: 30).")
    parser.add_argument(
        "--max-file-size-mb",
        type=float,
        default=100.0,
        help="Maximum PDF size in MiB (default: 100).",
    )
    parser.add_argument("--force", action="store_true", help="Atomically replace an existing PDF and sidecar.")
    parser.add_argument("--dry-run", action="store_true", help="Show selected URL and path without writing or downloading.")
    return parser


def validate_cli_args(args: argparse.Namespace) -> None:
    paper_ids = args.paper_id or []
    if args.timeout <= 0 or args.max_file_size_mb <= 0:
        raise UsageError("--timeout and --max-file-size-mb must be positive")
    if args.limit is not None and args.limit <= 0:
        raise UsageError("--limit must be positive")
    if args.sleep is not None and args.sleep < 0:
        raise UsageError("--sleep must be non-negative")

    if args.pdf_url:
        if args.metadata or args.title:
            raise UsageError("--pdf-url cannot be combined with --metadata or --title")
        if len(paper_ids) != 1:
            raise UsageError("--pdf-url requires exactly one --paper-id")
        if args.allow_batch:
            raise UsageError("Direct --pdf-url mode is single-paper only")
        validate_cvf_pdf_url(args.pdf_url)
        return

    if not args.metadata:
        raise UsageError("--metadata is required for --paper-id or --title selection")
    if bool(paper_ids) == bool(args.title):
        raise UsageError("With --metadata, use either --paper-id or --title")
    if len(paper_ids) > 1 and not args.allow_batch:
        raise UsageError("Multiple --paper-id values require --allow-batch")
    if args.allow_batch and (args.limit is None or args.sleep is None):
        raise UsageError("--allow-batch requires explicit --limit and --sleep")


def _selected_records(args: argparse.Namespace) -> List[Dict[str, Any]]:
    if args.pdf_url:
        return [{"paper_id": args.paper_id[0], "title": None, "pdf_url": args.pdf_url}]
    metadata_path = Path(args.metadata).expanduser()
    if not metadata_path.is_file():
        raise SelectionError("Metadata file does not exist: {}".format(metadata_path))
    records = load_json_records(metadata_path)
    selected = select_records(records, paper_ids=args.paper_id, title=args.title)
    if args.allow_batch:
        selected = selected[: args.limit]
    return selected


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        validate_cli_args(args)
        records = _selected_records(args)
        safe_ids = [sanitize_paper_id(record.get("paper_id")) for record in records]
        if len(set(safe_ids)) != len(safe_ids):
            raise SelectionError("Selected paper IDs collide after filename sanitization.")

        output_dir = Path(args.output_dir).expanduser()
        max_bytes = int(args.max_file_size_mb * 1024 * 1024)
        session = requests.Session()
        try:
            for index, record in enumerate(records):
                result = download_record(
                    record,
                    output_dir,
                    session=session,
                    timeout=args.timeout,
                    max_bytes=max_bytes,
                    force=args.force,
                    dry_run=args.dry_run,
                )
                print(json.dumps(result, ensure_ascii=False, sort_keys=True))
                if args.allow_batch and index + 1 < len(records):
                    time.sleep(args.sleep)
        finally:
            session.close()
    except (DownloadError, OSError, ValueError, requests.RequestException) as exc:
        print("Error: {}".format(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
