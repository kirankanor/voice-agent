from __future__ import annotations

from pathlib import Path
from typing import Any

from src.models.types import Decision
from src.storage.file_store import read_yaml, write_yaml, list_dir


class DecisionManager:
    """Manages architecture decision records with provenance."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.decisions_dir = data_dir / "decisions"
        self.decisions_dir.mkdir(parents=True, exist_ok=True)

    def create(self, id: str, project_id: str, requirement: str,
               candidates: list[str] | None = None,
               constraints: list[str] | None = None,
               experiment_ids: list[str] | None = None,
               evidence: str = "", decision: str = "",
               trade_offs: str = "",
               rejected: list[str] | None = None) -> Decision:
        """Create a new decision record."""
        dec = Decision(
            id=id,
            project_id=project_id,
            requirement=requirement,
            candidates=candidates or [],
            constraints=constraints or [],
            experiment_ids=experiment_ids or [],
            evidence=evidence,
            decision=decision,
            trade_offs=trade_offs,
            rejected=rejected or [],
        )
        self._save(dec)
        return dec

    def get(self, id: str) -> Decision | None:
        """Get a decision by ID."""
        path = self.decisions_dir / f"{id}.yaml"
        data = read_yaml(path)
        if not data:
            return None
        return Decision(**data)

    def list_all(self, project_id: str | None = None) -> list[Decision]:
        """List all decisions, optionally filtered by project."""
        decisions = []
        for path in list_dir(self.decisions_dir, ".yaml"):
            data = read_yaml(path)
            if data:
                dec = Decision(**data)
                if project_id is None or dec.project_id == project_id:
                    decisions.append(dec)
        return decisions

    def update(self, id: str, **kwargs: Any) -> Decision | None:
        """Update a decision record."""
        dec = self.get(id)
        if not dec:
            return None
        for key, value in kwargs.items():
            if hasattr(dec, key):
                setattr(dec, key, value)
        self._save(dec)
        return dec

    def delete(self, id: str) -> bool:
        """Delete a decision record."""
        path = self.decisions_dir / f"{id}.yaml"
        if path.exists():
            path.unlink()
            return True
        return False

    def _save(self, dec: Decision) -> None:
        """Save decision to YAML."""
        path = self.decisions_dir / f"{dec.id}.yaml"
        data = {
            "id": dec.id,
            "project_id": dec.project_id,
            "requirement": dec.requirement,
            "candidates": dec.candidates,
            "constraints": dec.constraints,
            "experiment_ids": dec.experiment_ids,
            "evidence": dec.evidence,
            "decision": dec.decision,
            "trade_offs": dec.trade_offs,
            "rejected": dec.rejected,
        }
        write_yaml(path, data)
