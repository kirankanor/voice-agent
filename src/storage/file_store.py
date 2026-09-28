from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def ensure_dir(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def read_yaml(path: Path) -> dict[str, Any]:
    """Read a YAML file and return its contents."""
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    """Write data to a YAML file atomically."""
    ensure_dir(path.parent)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    if path.exists():
        path.unlink()
    tmp.rename(path)


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file and return its contents."""
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    """Write data to a JSON file atomically."""
    ensure_dir(path.parent)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if path.exists():
        path.unlink()
    tmp.rename(path)


def list_dir(path: Path, extension: str | None = None) -> list[Path]:
    """List files in a directory, optionally filtered by extension."""
    if not path.exists():
        return []
    files = [f for f in path.iterdir() if f.is_file()]
    if extension:
        files = [f for f in files if f.suffix == extension]
    return sorted(files)
