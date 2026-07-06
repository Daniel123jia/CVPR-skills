#!/usr/bin/env python3
"""Shared helpers for the CVPR collection scripts."""

from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


COMPUTER_VISION = "computer_vision"
CONFERENCE = "cvpr"


def project_root() -> Path:
    return Path.cwd()


def default_raw_path(year: int) -> Path:
    return (
        project_root()
        / "data"
        / "raw"
        / COMPUTER_VISION
        / CONFERENCE
        / str(year)
        / f"cvpr_{year}_raw.json"
    )


def default_normalized_path(year: int) -> Path:
    return (
        project_root()
        / "data"
        / "normalized"
        / COMPUTER_VISION
        / CONFERENCE
        / str(year)
        / f"cvpr_{year}_normalized.json"
    )


def default_export_dir(year: int) -> Path:
    return project_root() / "outputs" / COMPUTER_VISION / CONFERENCE / str(year)


def output_file_in_dir(output_dir: str | None, default_path: Path) -> Path:
    if not output_dir:
        return default_path
    return Path(output_dir).expanduser().resolve() / default_path.name


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def backup_existing(path: Path) -> Path | None:
    if not path.exists():
        return None
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = path.with_name(f"{path.name}.bak.{timestamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def write_json_with_backup(path: Path, data: Any) -> Path | None:
    ensure_parent(path)
    backup_path = backup_existing(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return backup_path


def load_json_records(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        records = data.get("papers", [])
    else:
        records = data
    if not isinstance(records, list):
        raise ValueError(f"Expected a JSON list or an object with papers list: {path}")
    return [record for record in records if isinstance(record, dict)]


def configure_logging(script_name: str, year: int) -> None:
    logs_dir = project_root() / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"{script_name}_{year}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
