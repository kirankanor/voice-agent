"""Tests for decision records module."""

import tempfile
from pathlib import Path

from src.decisions import DecisionManager


def test_create_decision():
    """Can create a decision record."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = DecisionManager(Path(tmp))
        dec = mgr.create("d1", "p1", "STT selection",
                        candidates=["deepgram", "whisper"],
                        decision="deepgram",
                        evidence="latency benchmark results")
        assert dec.id == "d1"
        assert dec.decision == "deepgram"


def test_get_decision():
    """Can retrieve a decision by ID."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = DecisionManager(Path(tmp))
        mgr.create("d1", "p1", "STT selection")
        dec = mgr.get("d1")
        assert dec is not None
        assert dec.id == "d1"


def test_list_decisions():
    """Can list all decisions."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = DecisionManager(Path(tmp))
        mgr.create("d1", "p1", "STT selection")
        mgr.create("d2", "p1", "TTS selection")
        mgr.create("d3", "p2", "LLM selection")
        all_dec = mgr.list_all()
        assert len(all_dec) == 3


def test_list_by_project():
    """Can filter decisions by project."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = DecisionManager(Path(tmp))
        mgr.create("d1", "p1", "STT selection")
        mgr.create("d2", "p1", "TTS selection")
        mgr.create("d3", "p2", "LLM selection")
        p1_dec = mgr.list_all(project_id="p1")
        assert len(p1_dec) == 2


def test_update_decision():
    """Can update a decision record."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = DecisionManager(Path(tmp))
        mgr.create("d1", "p1", "STT selection")
        updated = mgr.update("d1", decision="deepgram", trade_offs="higher cost but lower latency")
        assert updated is not None
        assert updated.decision == "deepgram"
        assert updated.trade_offs == "higher cost but lower latency"


def test_delete_decision():
    """Can delete a decision record."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = DecisionManager(Path(tmp))
        mgr.create("d1", "p1", "STT selection")
        assert mgr.delete("d1") is True
        assert mgr.get("d1") is None


def test_decision_with_experiments():
    """Can link decisions to experiments."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = DecisionManager(Path(tmp))
        dec = mgr.create("d1", "p1", "STT selection",
                        experiment_ids=["exp-1", "exp-2"],
                        evidence="see experiments exp-1 and exp-2")
        assert dec.experiment_ids == ["exp-1", "exp-2"]


def test_decision_persistence():
    """Decisions persist across manager instances."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        mgr1 = DecisionManager(path)
        mgr1.create("d1", "p1", "STT selection", decision="deepgram")
        mgr2 = DecisionManager(path)
        dec = mgr2.get("d1")
        assert dec is not None
        assert dec.decision == "deepgram"
