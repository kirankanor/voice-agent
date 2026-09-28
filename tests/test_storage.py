"""Tests for file-based storage utilities."""

import tempfile
from pathlib import Path

from src.storage.file_store import read_yaml, write_yaml, read_json, write_json, list_dir, ensure_dir


def test_write_read_yaml():
    """Can write and read YAML files."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test.yaml"
        write_yaml(path, {"key": "value", "num": 42})
        data = read_yaml(path)
        assert data["key"] == "value"
        assert data["num"] == 42


def test_write_read_json():
    """Can write and read JSON files."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test.json"
        write_json(path, {"key": "value", "num": 42})
        data = read_json(path)
        assert data["key"] == "value"
        assert data["num"] == 42


def test_read_missing_yaml():
    """Reading missing YAML returns empty dict."""
    with tempfile.TemporaryDirectory() as tmp:
        data = read_yaml(Path(tmp) / "missing.yaml")
        assert data == {}


def test_read_missing_json():
    """Reading missing JSON returns empty dict."""
    with tempfile.TemporaryDirectory() as tmp:
        data = read_json(Path(tmp) / "missing.json")
        assert data == {}


def test_overwrite_yaml():
    """Can overwrite existing YAML file."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test.yaml"
        write_yaml(path, {"version": 1})
        write_yaml(path, {"version": 2})
        data = read_yaml(path)
        assert data["version"] == 2


def test_overwrite_json():
    """Can overwrite existing JSON file."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test.json"
        write_json(path, {"version": 1})
        write_json(path, {"version": 2})
        data = read_json(path)
        assert data["version"] == 2


def test_list_dir():
    """Can list files in directory."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        write_yaml(tmp_path / "a.yaml", {"a": 1})
        write_yaml(tmp_path / "b.yaml", {"b": 2})
        write_json(tmp_path / "c.json", {"c": 3})
        yaml_files = list_dir(tmp_path, ".yaml")
        assert len(yaml_files) == 2
        json_files = list_dir(tmp_path, ".json")
        assert len(json_files) == 1


def test_ensure_dir():
    """Can create nested directories."""
    with tempfile.TemporaryDirectory() as tmp:
        nested = Path(tmp) / "a" / "b" / "c"
        ensure_dir(nested)
        assert nested.exists()


def test_atomic_write():
    """No temp files left after write."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test.yaml"
        write_yaml(path, {"data": "test"})
        tmp_files = list(Path(tmp).glob("*.tmp"))
        assert len(tmp_files) == 0
