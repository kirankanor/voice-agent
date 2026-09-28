"""Tests for CLI interface."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from src.cli import main, get_managers


def test_cli_help():
    """CLI shows help."""
    with patch("sys.argv", ["wbench"]):
        try:
            main()
        except SystemExit:
            pass


def test_project_create():
    """Can create project via CLI."""
    with tempfile.TemporaryDirectory() as tmp:
        with patch("src.cli.DATA_DIR", Path(tmp)):
            with patch("sys.argv", ["wbench", "project", "create", "--id", "p1", "--name", "Test"]):
                main()


def test_project_list():
    """Can list projects via CLI."""
    with tempfile.TemporaryDirectory() as tmp:
        with patch("src.cli.DATA_DIR", Path(tmp)):
            with patch("sys.argv", ["wbench", "project", "create", "--id", "p1", "--name", "Test"]):
                main()
            with patch("sys.argv", ["wbench", "project", "list"]):
                main()


def test_registry_init():
    """Can initialize default providers."""
    with tempfile.TemporaryDirectory() as tmp:
        with patch("src.cli.DATA_DIR", Path(tmp)):
            with patch("sys.argv", ["wbench", "registry", "init"]):
                main()


def test_registry_list():
    """Can list providers."""
    with tempfile.TemporaryDirectory() as tmp:
        with patch("src.cli.DATA_DIR", Path(tmp)):
            with patch("sys.argv", ["wbench", "registry", "init"]):
                main()
            with patch("sys.argv", ["wbench", "registry", "list"]):
                main()


def test_cost_estimate():
    """Can estimate costs."""
    with tempfile.TemporaryDirectory() as tmp:
        with patch("src.cli.DATA_DIR", Path(tmp)):
            with patch("sys.argv", ["wbench", "cost", "estimate"]):
                main()


def test_managers_initialization():
    """All managers can be initialized."""
    with tempfile.TemporaryDirectory() as tmp:
        with patch("src.cli.DATA_DIR", Path(tmp)):
            managers = get_managers()
            assert "projects" in managers
            assert "registry" in managers
            assert "experiments" in managers
            assert "benchmarks" in managers
            assert "agents" in managers
            assert "decisions" in managers
            assert "costs" in managers
