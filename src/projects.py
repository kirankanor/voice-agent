from __future__ import annotations

from pathlib import Path
from typing import Any

from src.models.types import Project
from src.storage.file_store import read_yaml, write_yaml, list_dir


class ProjectManager:
    """Manages client projects with YAML-based storage."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.projects_dir = data_dir / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    def create(self, id: str, name: str, languages: list[str] | None = None,
               latency_target_ms: int | None = None, budget: str | None = None,
               use_case: str = "") -> Project:
        """Create a new project."""
        project = Project(
            id=id,
            name=name,
            languages=languages or [],
            latency_target_ms=latency_target_ms,
            budget=budget,
            use_case=use_case,
        )
        self._save(project)
        return project

    def get(self, id: str) -> Project | None:
        """Get a project by ID."""
        path = self.projects_dir / f"{id}.yaml"
        data = read_yaml(path)
        if not data:
            return None
        return Project(**data)

    def list_all(self) -> list[Project]:
        """List all projects."""
        projects = []
        for path in list_dir(self.projects_dir, ".yaml"):
            data = read_yaml(path)
            if data:
                projects.append(Project(**data))
        return projects

    def update(self, id: str, **kwargs: Any) -> Project | None:
        """Update a project's fields."""
        project = self.get(id)
        if not project:
            return None
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
        self._save(project)
        return project

    def archive(self, id: str) -> bool:
        """Archive a project (set status to archived)."""
        project = self.get(id)
        if not project:
            return False
        project.status = "archived"
        self._save(project)
        return True

    def delete(self, id: str) -> bool:
        """Delete a project."""
        path = self.projects_dir / f"{id}.yaml"
        if path.exists():
            path.unlink()
            return True
        return False

    def _save(self, project: Project) -> None:
        """Save a project to YAML."""
        path = self.projects_dir / f"{project.id}.yaml"
        data = {
            "id": project.id,
            "name": project.name,
            "languages": project.languages,
            "latency_target_ms": project.latency_target_ms,
            "budget": project.budget,
            "use_case": project.use_case,
            "status": project.status,
        }
        write_yaml(path, data)
