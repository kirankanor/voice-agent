"""Tests for cost calculator module."""

import tempfile
from pathlib import Path

from src.costs import CostCalculator


def test_estimate_cost():
    """Can estimate conversation cost."""
    with tempfile.TemporaryDirectory() as tmp:
        calc = CostCalculator(Path(tmp))
        result = calc.estimate(
            stt_cost_per_min=0.0043,
            tts_cost_per_char=0.00003,
            llm_cost_per_1k_tokens=0.002,
            avg_response_tokens=200,
            avg_chars_per_response=800,
            conversation_duration_min=5.0,
            avg_turns=10,
        )
        assert result["stt"] > 0
        assert result["tts"] > 0
        assert result["llm"] > 0
        assert result["total"] > 0
        assert result["per_minute"] > 0
        assert result["per_1k_conversations"] > 0


def test_estimate_components():
    """Cost components sum to total."""
    with tempfile.TemporaryDirectory() as tmp:
        calc = CostCalculator(Path(tmp))
        result = calc.estimate(
            stt_cost_per_min=0.0043,
            tts_cost_per_char=0.00003,
            llm_cost_per_1k_tokens=0.002,
        )
        component_sum = result["stt"] + result["tts"] + result["llm"]
        assert abs(component_sum - result["total"]) < 0.001


def test_save_estimate():
    """Can save a cost estimate."""
    with tempfile.TemporaryDirectory() as tmp:
        calc = CostCalculator(Path(tmp))
        result = calc.estimate(0.0043, 0.00003, 0.002)
        calc.save_estimate("c1", {"stt": "deepgram"}, result)
        saved = calc.get("c1")
        assert saved is not None
        assert saved["id"] == "c1"
        assert saved["estimate"]["total"] > 0


def test_list_estimates():
    """Can list all cost estimates."""
    with tempfile.TemporaryDirectory() as tmp:
        calc = CostCalculator(Path(tmp))
        r1 = calc.estimate(0.0043, 0.00003, 0.002)
        r2 = calc.estimate(0.01, 0.00005, 0.003)
        calc.save_estimate("c1", {}, r1)
        calc.save_estimate("c2", {}, r2)
        estimates = calc.list_all()
        assert len(estimates) == 2


def test_cost_persistence():
    """Cost estimates persist across calculator instances."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        calc1 = CostCalculator(path)
        r1 = calc1.estimate(0.0043, 0.00003, 0.002)
        calc1.save_estimate("c1", {"stt": "deepgram"}, r1)
        calc2 = CostCalculator(path)
        saved = calc2.get("c1")
        assert saved is not None
        assert saved["providers"]["stt"] == "deepgram"
