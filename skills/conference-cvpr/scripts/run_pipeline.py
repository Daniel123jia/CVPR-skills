#!/usr/bin/env python3
"""Run the CVPR collection pipeline end to end."""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Sequence


PIPELINE_STEPS = [
    ("collect", "collect_cvpr.py"),
    ("normalize", "normalize_cvpr.py"),
    ("export", "export_cvpr.py"),
    ("check", "check_completeness.py"),
]


def command_text(command: Sequence[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def build_command(
    script_name: str,
    year: int,
    enrich_pages: bool,
    limit: Optional[int],
    sleep_seconds: float,
    resume: bool,
    python_executable: str,
) -> List[str]:
    script_path = Path(__file__).resolve().parent / script_name
    command = [python_executable, str(script_path), "--year", str(year)]
    if script_name == "collect_cvpr.py":
        if enrich_pages:
            command.append("--enrich-pages")
        if limit is not None:
            command.extend(["--limit", str(limit)])
        if sleep_seconds:
            command.extend(["--sleep", str(sleep_seconds)])
        if resume:
            command.append("--resume")
    return command


def run_pipeline(
    year: int,
    enrich_pages: bool = False,
    limit: Optional[int] = None,
    sleep_seconds: float = 0.0,
    resume: bool = False,
    python_executable: Optional[str] = None,
) -> int:
    interpreter = python_executable or sys.executable
    total = len(PIPELINE_STEPS)
    for index, (step_name, script_name) in enumerate(PIPELINE_STEPS, start=1):
        command = build_command(script_name, year, enrich_pages, limit, sleep_seconds, resume, interpreter)
        print(f"[{index}/{total}] {step_name}: {command_text(command)}")
        result = subprocess.run(command)
        if result.returncode != 0:
            print(f"Pipeline stopped: step '{step_name}' failed with exit code {result.returncode}.", file=sys.stderr)
            print(f"Failed command: {command_text(command)}", file=sys.stderr)
            return result.returncode
    print("Pipeline completed successfully.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run CVPR collect -> normalize -> export -> check pipeline.")
    parser.add_argument("--year", type=int, required=True, help="CVPR year, for example 2026.")
    parser.add_argument(
        "--enrich-pages",
        action="store_true",
        help="Pass through to collect_cvpr.py to fetch individual paper pages. Disabled by default.",
    )
    parser.add_argument("--limit", type=int, help="Pass through to collect_cvpr.py.")
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Pass through to collect_cvpr.py as seconds between enrichment requests.",
    )
    parser.add_argument("--resume", action="store_true", help="Pass through to collect_cvpr.py.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return run_pipeline(
        year=args.year,
        enrich_pages=args.enrich_pages,
        limit=args.limit,
        sleep_seconds=args.sleep,
        resume=args.resume,
    )


if __name__ == "__main__":
    raise SystemExit(main())
