from __future__ import annotations

from pathlib import Path
from typing import Any

from src.models.types import Experiment
from src.storage.file_store import read_yaml, write_yaml, list_dir


class ExperimentManager:
    """Manages experiment definitions and lifecycle."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.experiments_dir = data_dir / "experiments"
        self.experiments_dir.mkdir(parents=True, exist_ok=True)

    def create(self, id: str, project_id: str, experiment_type: str,
               providers: list[str] | None = None,
               configuration: dict[str, Any] | None = None) -> Experiment:
        """Create a new experiment."""
        experiment = Experiment(
            id=id,
            project_id=project_id,
            experiment_type=experiment_type,
            providers=providers or [],
            configuration=configuration or {},
        )
        self._save(experiment)
        return experiment

    def get(self, id: str) -> Experiment | None:
        """Get an experiment by ID."""
        path = self.experiments_dir / f"{id}.yaml"
        data = read_yaml(path)
        if not data:
            return None
        return Experiment(**data)

    def list_all(self, project_id: str | None = None) -> list[Experiment]:
        """List all experiments, optionally filtered by project."""
        experiments = []
        for path in list_dir(self.experiments_dir, ".yaml"):
            data = read_yaml(path)
            if data:
                exp = Experiment(**data)
                if project_id is None or exp.project_id == project_id:
                    experiments.append(exp)
        return experiments

    def update_status(self, id: str, status: str) -> Experiment | None:
        """Update experiment status."""
        experiment = self.get(id)
        if not experiment:
            return None
        experiment.status = status
        self._save(experiment)
        return experiment

    def record_results(self, id: str, results: dict[str, Any]) -> Experiment | None:
        """Record experiment results."""
        experiment = self.get(id)
        if not experiment:
            return None
        experiment.results = results
        self._save(experiment)
        return experiment

    def delete(self, id: str) -> bool:
        """Delete an experiment."""
        path = self.experiments_dir / f"{id}.yaml"
        if path.exists():
            path.unlink()
            return True
        return False

    def _save(self, experiment: Experiment) -> None:
        """Save experiment to YAML."""
        path = self.experiments_dir / f"{experiment.id}.yaml"
        data = {
            "id": experiment.id,
            "project_id": experiment.project_id,
            "experiment_type": experiment.experiment_type,
            "providers": experiment.providers,
            "configuration": experiment.configuration,
            "status": experiment.status,
            "results": experiment.results,
        }
        write_yaml(path, data)
