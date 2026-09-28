from __future__ import annotations

from pathlib import Path
from typing import Any

from src.models.types import Benchmark
from src.storage.file_store import read_yaml, write_yaml, list_dir


class BenchmarkStore:
    """Stores benchmark results with metrics and raw evidence."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.benchmarks_dir = data_dir / "benchmarks"
        self.benchmarks_dir.mkdir(parents=True, exist_ok=True)

    def create(self, id: str, experiment_id: str, provider: str,
               component: str, latency_ms: float | None = None,
               quality: float | None = None, cost: float | None = None,
               failure_rate: float | None = None,
               raw_result_path: str | None = None) -> Benchmark:
        """Create a new benchmark record."""
        bench = Benchmark(
            id=id,
            experiment_id=experiment_id,
            provider=provider,
            component=component,
            latency_ms=latency_ms,
            quality=quality,
            cost=cost,
            failure_rate=failure_rate,
            raw_result_path=raw_result_path,
        )
        self._save(bench)
        return bench

    def get(self, id: str) -> Benchmark | None:
        """Get a benchmark by ID."""
        path = self.benchmarks_dir / f"{id}.yaml"
        data = read_yaml(path)
        if not data:
            return None
        return Benchmark(**data)

    def list_all(self, experiment_id: str | None = None,
                 provider: str | None = None) -> list[Benchmark]:
        """List benchmarks with optional filters."""
        benchmarks = []
        for path in list_dir(self.benchmarks_dir, ".yaml"):
            data = read_yaml(path)
            if data:
                bench = Benchmark(**data)
                if experiment_id and bench.experiment_id != experiment_id:
                    continue
                if provider and bench.provider != provider:
                    continue
                benchmarks.append(bench)
        return benchmarks

    def delete(self, id: str) -> bool:
        """Delete a benchmark record."""
        path = self.benchmarks_dir / f"{id}.yaml"
        if path.exists():
            path.unlink()
            return True
        return False

    def _save(self, bench: Benchmark) -> None:
        """Save benchmark to YAML."""
        path = self.benchmarks_dir / f"{bench.id}.yaml"
        data = {
            "id": bench.id,
            "experiment_id": bench.experiment_id,
            "provider": bench.provider,
            "component": bench.component,
            "latency_ms": bench.latency_ms,
            "quality": bench.quality,
            "cost": bench.cost,
            "failure_rate": bench.failure_rate,
            "raw_result_path": bench.raw_result_path,
        }
        write_yaml(path, data)
