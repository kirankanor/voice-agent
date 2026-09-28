"""Tests for project management module."""

import tempfile
from pathlib import Path

from src.projects import ProjectManager


def test_create_project():
    """Can create a project with requirements."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ProjectManager(Path(tmp))
        project = mgr.create("p1", "Test Project", languages=["en", "hi"])
        assert project.id == "p1"
        assert project.name == "Test Project"
        assert project.languages == ["en", "hi"]
        assert project.status == "active"


def test_get_project():
    """Can retrieve a project by ID."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ProjectManager(Path(tmp))
        mgr.create("p1", "Test Project")
        project = mgr.get("p1")
        assert project is not None
        assert project.id == "p1"


def test_get_missing_project():
    """Returns None for missing project."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ProjectManager(Path(tmp))
        assert mgr.get("nonexistent") is None


def test_list_projects():
    """Can list all projects."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ProjectManager(Path(tmp))
        mgr.create("p1", "Project A")
        mgr.create("p2", "Project B")
        projects = mgr.list_all()
        assert len(projects) == 2
        ids = {p.id for p in projects}
        assert ids == {"p1", "p2"}


def test_update_project():
    """Can update project fields."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ProjectManager(Path(tmp))
        mgr.create("p1", "Test Project")
        updated = mgr.update("p1", budget="1000 USD", latency_target_ms=500)
        assert updated is not None
        assert updated.budget == "1000 USD"
        assert updated.latency_target_ms == 500


def test_archive_project():
    """Can archive a project."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ProjectManager(Path(tmp))
        mgr.create("p1", "Test Project")
        assert mgr.archive("p1") is True
        project = mgr.get("p1")
        assert project.status == "archived"


def test_delete_project():
    """Can delete a project."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ProjectManager(Path(tmp))
        mgr.create("p1", "Test Project")
        assert mgr.delete("p1") is True
        assert mgr.get("p1") is None


def test_project_persistence():
    """Projects persist across manager instances."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        mgr1 = ProjectManager(path)
        mgr1.create("p1", "Persistent Project")
        mgr2 = ProjectManager(path)
        project = mgr2.get("p1")
        assert project is not None
        assert project.name == "Persistent Project"
