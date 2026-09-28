"""Tests for experiment definitions module."""

import tempfile
from pathlib import Path

from src.experiments import ExperimentManager


def test_create_experiment():
    """Can create an experiment."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ExperimentManager(Path(tmp))
        exp = mgr.create("e1", "p1", "stt_comparison", providers=["deepgram", "whisper"])
        assert exp.id == "e1"
        assert exp.project_id == "p1"
        assert exp.status == "defined"


def test_get_experiment():
    """Can retrieve an experiment by ID."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ExperimentManager(Path(tmp))
        mgr.create("e1", "p1", "stt_comparison")
        exp = mgr.get("e1")
        assert exp is not None
        assert exp.id == "e1"


def test_list_experiments():
    """Can list all experiments."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ExperimentManager(Path(tmp))
        mgr.create("e1", "p1", "stt_comparison")
        mgr.create("e2", "p1", "tts_comparison")
        mgr.create("e3", "p2", "llm_comparison")
        all_exps = mgr.list_all()
        assert len(all_exps) == 3


def test_list_by_project():
    """Can filter experiments by project."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ExperimentManager(Path(tmp))
        mgr.create("e1", "p1", "stt_comparison")
        mgr.create("e2", "p1", "tts_comparison")
        mgr.create("e3", "p2", "llm_comparison")
        p1_exps = mgr.list_all(project_id="p1")
        assert len(p1_exps) == 2


def test_update_status():
    """Can update experiment status."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ExperimentManager(Path(tmp))
        mgr.create("e1", "p1", "stt_comparison")
        updated = mgr.update_status("e1", "running")
        assert updated is not None
        assert updated.status == "running"


def test_record_results():
    """Can record experiment results."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ExperimentManager(Path(tmp))
        mgr.create("e1", "p1", "stt_comparison")
        results = {"deepgram": {"latency_ms": 320}, "whisper": {"latency_ms": 800}}
        updated = mgr.record_results("e1", results)
        assert updated is not None
        assert updated.results["deepgram"]["latency_ms"] == 320


def test_delete_experiment():
    """Can delete an experiment."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = ExperimentManager(Path(tmp))
        mgr.create("e1", "p1", "stt_comparison")
        assert mgr.delete("e1") is True
        assert mgr.get("e1") is None


def test_experiment_persistence():
    """Experiments persist across manager instances."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        mgr1 = ExperimentManager(path)
        mgr1.create("e1", "p1", "stt_comparison")
        mgr2 = ExperimentManager(path)
        exp = mgr2.get("e1")
        assert exp is not None
        assert exp.experiment_type == "stt_comparison"
