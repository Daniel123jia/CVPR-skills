#!/usr/bin/env python3
"""Collect CVPR main-conference papers from CVF Open Access."""

from __future__ import annotations

import argparse
import logging
import re
import time
from html import unescape
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from _cvpr_common import configure_logging, default_raw_path, load_json_records, output_file_in_dir, write_json_with_backup


BASE_URL = "https://openaccess.thecvf.com"
USER_AGENT = "ai-conference-skills/0.1 (+https://openaccess.thecvf.com)"
TITLE_RE = re.compile(
    r"<dt[^>]*class=[\"'][^\"']*\bptitle\b[^\"']*[\"'][^>]*>.*?"
    r"<a\s+[^>]*href=[\"'](?P<href>[^\"']+)[\"'][^>]*>(?P<title>.*?)</a>.*?</dt>",
    re.IGNORECASE | re.DOTALL,
)
ANCHOR_RE = re.compile(
    r"<a\s+[^>]*href=[\"'](?P<href>[^\"']+)[\"'][^>]*>(?P<label>.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", unescape(value)).strip()


def strip_tags(value: str) -> str:
    return clean_text(re.sub(r"<[^>]+>", " ", value))


def join_cvf_url(page_url: str, href: str) -> str:
    if href.startswith(("http://", "https://", "/")):
        return urljoin(page_url, href)
    base = page_url.split("?", 1)[0]
    if not base.endswith("/"):
        base = f"{base}/"
    return urljoin(base, href)


def fetch_url(session: requests.Session, url: str, timeout: int, retries: int) -> str:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            last_error = exc
            logging.warning("Fetch failed attempt %s/%s for %s: %s", attempt, retries, url, exc)
            if attempt < retries:
                time.sleep(min(2 ** (attempt - 1), 8))
    raise RuntimeError(f"Failed to fetch {url}: {last_error}")


def iter_until_next_title(node: Tag) -> Iterable[Tag]:
    for sibling in node.next_siblings:
        if isinstance(sibling, Tag) and sibling.name == "dt" and "ptitle" in sibling.get("class", []):
            break
        if isinstance(sibling, Tag):
            yield sibling


def split_authors(raw_authors: str) -> list[str]:
    text = clean_text(raw_authors)
    if not text:
        return []
    return [author.strip() for author in re.split(r"\s*,\s*", text) if author.strip()]


def find_link(nodes: Iterable[Tag], page_url: str, predicates: tuple[str, ...]) -> str | None:
    for node in nodes:
        for anchor in node.find_all("a", href=True):
            href = anchor.get("href", "")
            label = clean_text(anchor.get_text(" ")).lower()
            href_lower = href.lower()
            if any(token in label or token in href_lower for token in predicates):
                return join_cvf_url(page_url, href)
    return None


def abstract_from_nodes(nodes: Iterable[Tag]) -> str:
    for node in nodes:
        if node.get("id") == "abstract":
            text = clean_text(node.get_text(" "))
            if text:
                return text
        candidate = node.find(id="abstract")
        if isinstance(candidate, Tag):
            text = clean_text(candidate.get_text(" "))
            if text:
                return text
        candidate = node.find(class_=lambda value: value and "abstract" in str(value).lower())
        if isinstance(candidate, Tag):
            text = clean_text(candidate.get_text(" "))
            if text:
                return text
    return ""


def abstract_from_identifier(soup: BeautifulSoup, paper_page_url: str) -> str:
    identifier = Path(paper_page_url).stem
    if not identifier:
        return ""
    container = soup.find(id=identifier)
    if not isinstance(container, Tag):
        return ""
    return abstract_from_nodes([container])


def find_link_in_html(block: str, page_url: str, predicates: tuple[str, ...]) -> str | None:
    for match in ANCHOR_RE.finditer(block):
        href = match.group("href")
        label = strip_tags(match.group("label")).lower()
        href_lower = href.lower()
        if any(token in label or token in href_lower for token in predicates):
            return join_cvf_url(page_url, href)
    return None


def abstract_from_html(block: str) -> str:
    match = re.search(
        r"<[^>]+(?:id|class)=[\"'][^\"']*abstract[^\"']*[\"'][^>]*>(?P<body>.*?)</[^>]+>",
        block,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return ""
    return strip_tags(match.group("body"))


def parse_listing_page_fast(html: str, page_url: str) -> list[dict[str, object]]:
    matches = list(TITLE_RE.finditer(html))
    papers: list[dict[str, object]] = []
    for index, match in enumerate(matches):
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(html)
        block = html[match.end() : block_end]
        author_values = re.findall(
            r"name=[\"']query_author[\"'][^>]*value=[\"']([^\"']+)[\"']",
            block,
            re.IGNORECASE,
        )
        if author_values:
            authors = [clean_text(author) for author in author_values if clean_text(author)]
        else:
            first_dd = re.search(r"<dd[^>]*>(?P<body>.*?)</dd>", block, re.IGNORECASE | re.DOTALL)
            authors = split_authors(strip_tags(first_dd.group("body")) if first_dd else "")
        papers.append(
            {
                "title": strip_tags(match.group("title")),
                "authors": authors,
                "paper_page_url": join_cvf_url(page_url, match.group("href")),
                "pdf_url": find_link_in_html(block, page_url, ("pdf", ".pdf")),
                "abstract": abstract_from_html(block) or None,
                "supplementary_url": find_link_in_html(block, page_url, ("supp", "supplement")),
            }
        )
    return papers


def build_abstract_lookup(soup: BeautifulSoup) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for abstract_node in soup.find_all(id="abstract"):
        if not isinstance(abstract_node, Tag):
            continue
        parent = abstract_node.parent
        while isinstance(parent, Tag):
            identifier = str(parent.get("id") or "")
            if identifier and identifier != "abstract":
                abstract = clean_text(abstract_node.get_text(" "))
                if abstract:
                    lookup[identifier] = abstract
                break
            parent = parent.parent
    return lookup


def parse_listing_page(html: str, page_url: str) -> list[dict[str, object]]:
    if len(html) > 200_000 or "query_author" in html:
        papers = parse_listing_page_fast(html, page_url)
        if papers:
            return papers

    soup = BeautifulSoup(html, "html.parser")
    abstract_lookup: dict[str, str] | None = None
    papers: list[dict[str, object]] = []
    for title_node in soup.select("dt.ptitle"):
        title_link = title_node.find("a", href=True)
        if not title_link:
            continue
        paper_page_url = join_cvf_url(page_url, title_link["href"])
        paper_identifier = Path(paper_page_url).stem
        siblings = list(iter_until_next_title(title_node))
        author_node = next((node for node in siblings if node.name == "dd" and clean_text(node.get_text(" "))), None)
        authors = split_authors(author_node.get_text(" ") if author_node else "")
        pdf_url = find_link(siblings, page_url, ("pdf", ".pdf"))
        supplementary_url = find_link(siblings, page_url, ("supp", "supplement"))
        abstract = abstract_from_nodes(siblings)
        if not abstract:
            if abstract_lookup is None:
                abstract_lookup = build_abstract_lookup(soup)
            abstract = abstract_lookup.get(paper_identifier, "")
        papers.append(
            {
                "title": clean_text(title_link.get_text(" ")),
                "authors": authors,
                "paper_page_url": paper_page_url,
                "pdf_url": pdf_url,
                "abstract": abstract or None,
                "supplementary_url": supplementary_url,
            }
        )
    return papers


def parse_paper_page(html: str, page_url: str) -> dict[str, str | None]:
    soup = BeautifulSoup(html, "html.parser")
    abstract = abstract_from_nodes([soup]) or None
    pdf_url = find_link([soup], page_url, ("pdf", ".pdf"))
    supplementary_url = find_link([soup], page_url, ("supp", "supplement"))
    return {
        "abstract": abstract,
        "pdf_url": pdf_url,
        "supplementary_url": supplementary_url,
    }


def parse_day_links(html: str, home_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: list[str] = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        label = clean_text(anchor.get_text(" ")).lower()
        absolute = urljoin(home_url, href)
        href_lower = absolute.lower()
        if "day=" not in href_lower:
            continue
        if "day=all" in href_lower or "workshop" in href_lower or "tutorial" in href_lower:
            continue
        if "day" in label or "day=" in href_lower:
            links.append(absolute)
    return list(dict.fromkeys(links))


def merge_by_title(papers: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    merged: dict[str, dict[str, object]] = {}
    for paper in papers:
        key = clean_text(str(paper.get("title") or "")).casefold()
        if not key:
            key = str(paper.get("paper_page_url") or "")
        if key not in merged:
            merged[key] = paper
            continue
        existing = merged[key]
        for field in ("authors", "paper_page_url", "pdf_url", "abstract", "supplementary_url"):
            if not existing.get(field) and paper.get(field):
                existing[field] = paper[field]
    return list(merged.values())


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def enrich_missing_from_paper_pages(
    papers: list[dict[str, object]],
    session: requests.Session,
    timeout: int,
    retries: int,
    limit: int | None = None,
    sleep_seconds: float = 0.0,
) -> None:
    attempts = 0
    for paper in papers:
        if paper.get("abstract") and paper.get("pdf_url"):
            continue
        if limit is not None and attempts >= limit:
            break
        paper_page_url = paper.get("paper_page_url")
        if not isinstance(paper_page_url, str) or not paper_page_url:
            continue
        attempts += 1
        try:
            details = parse_paper_page(fetch_url(session, paper_page_url, timeout, retries), paper_page_url)
        except RuntimeError as exc:
            logging.warning("Could not enrich paper page %s: %s", paper_page_url, exc)
            if sleep_seconds > 0 and (limit is None or attempts < limit):
                time.sleep(sleep_seconds)
            continue
        for field in ("abstract", "pdf_url", "supplementary_url"):
            if not paper.get(field) and details.get(field):
                paper[field] = details[field]
        if sleep_seconds > 0 and (limit is None or attempts < limit):
            time.sleep(sleep_seconds)


def collect_cvpr(
    year: int,
    timeout: int = 30,
    retries: int = 3,
    enrich_pages: bool = False,
    limit: int | None = None,
    sleep_seconds: float = 0.0,
) -> list[dict[str, object]]:
    session = build_session()
    home_url = f"{BASE_URL}/CVPR{year}"
    all_url = f"{home_url}?day=all"

    papers: list[dict[str, object]] = []
    try:
        logging.info("Fetching all-papers page: %s", all_url)
        papers = parse_listing_page(fetch_url(session, all_url, timeout, retries), all_url)
    except RuntimeError as exc:
        logging.warning("All-papers page failed: %s", exc)

    if not papers:
        logging.info("Falling back to day links from %s", home_url)
        home_html = fetch_url(session, home_url, timeout, retries)
        day_links = parse_day_links(home_html, home_url)
        if not day_links:
            raise RuntimeError(f"No CVPR day links found at {home_url}")
        for day_url in day_links:
            logging.info("Fetching day page: %s", day_url)
            papers.extend(parse_listing_page(fetch_url(session, day_url, timeout, retries), day_url))

    papers = merge_by_title(papers)
    if limit is not None:
        papers = papers[:limit]
    if enrich_pages:
        enrich_missing_from_paper_pages(papers, session, timeout, retries, limit, sleep_seconds)
    return papers


def resume_from_existing(
    output_path: Path,
    timeout: int,
    retries: int,
    enrich_pages: bool,
    limit: int | None,
    sleep_seconds: float,
) -> list[dict[str, object]]:
    papers: list[dict[str, object]] = load_json_records(output_path)
    if limit is not None:
        papers = papers[:limit]
    if enrich_pages:
        session = build_session()
        enrich_missing_from_paper_pages(papers, session, timeout, retries, limit, sleep_seconds)
    return papers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect CVPR main-conference papers from CVF Open Access.")
    parser.add_argument("--year", type=int, required=True, help="CVPR year, for example 2026.")
    parser.add_argument("--output-dir", help="Directory for cvpr_YEAR_raw.json. Defaults to data/raw/.../cvpr/YEAR/.")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds. Default: 30.")
    parser.add_argument("--retries", type=int, default=3, help="HTTP retry attempts per URL. Default: 3.")
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit records written and per-paper enrichment attempts. Useful for samples and cautious enrichment runs.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Seconds to wait between individual paper-page enrichment requests. Used only with --enrich-pages.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse an existing raw JSON output when present, then optionally enrich/write it again with backups.",
    )
    parser.add_argument(
        "--enrich-pages",
        action="store_true",
        help="Fetch individual paper pages to fill missing abstracts and related links. Slower; disabled by default.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    configure_logging("collect_cvpr", args.year)
    output_path = output_file_in_dir(args.output_dir, default_raw_path(args.year))
    if args.resume and output_path.exists():
        logging.info("Resuming from existing raw JSON: %s", output_path)
        papers = resume_from_existing(
            output_path,
            timeout=args.timeout,
            retries=args.retries,
            enrich_pages=args.enrich_pages,
            limit=args.limit,
            sleep_seconds=args.sleep,
        )
    else:
        if args.resume:
            logging.info("Resume requested, but no existing raw JSON found at %s. Running a fresh collection.", output_path)
        papers = collect_cvpr(
            args.year,
            timeout=args.timeout,
            retries=args.retries,
            enrich_pages=args.enrich_pages,
            limit=args.limit,
            sleep_seconds=args.sleep,
        )
    backup_path = write_json_with_backup(output_path, papers)
    if backup_path:
        logging.info("Backed up existing output to %s", backup_path)
    logging.info("Wrote %s raw CVPR papers to %s", len(papers), output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
