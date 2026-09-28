"""Tests for benchmark store module."""

import tempfile
from pathlib import Path

from src.benchmarks import BenchmarkStore


def test_create_benchmark():
    """Can create a benchmark record."""
    with tempfile.TemporaryDirectory() as tmp:
        store = BenchmarkStore(Path(tmp))
        bench = store.create("b1", "exp1", "deepgram", "stt",
                            latency_ms=320, quality=0.91, cost=0.0043)
        assert bench.id == "b1"
        assert bench.provider == "deepgram"
        assert bench.latency_ms == 320


def test_get_benchmark():
    """Can retrieve a benchmark by ID."""
    with tempfile.TemporaryDirectory() as tmp:
        store = BenchmarkStore(Path(tmp))
        store.create("b1", "exp1", "deepgram", "stt")
        bench = store.get("b1")
        assert bench is not None
        assert bench.id == "b1"


def test_list_benchmarks():
    """Can list all benchmarks."""
    with tempfile.TemporaryDirectory() as tmp:
        store = BenchmarkStore(Path(tmp))
        store.create("b1", "exp1", "deepgram", "stt")
        store.create("b2", "exp1", "whisper", "stt")
        store.create("b3", "exp2", "elevenlabs", "tts")
        all_bench = store.list_all()
        assert len(all_bench) == 3


def test_list_by_experiment():
    """Can filter benchmarks by experiment."""
    with tempfile.TemporaryDirectory() as tmp:
        store = BenchmarkStore(Path(tmp))
        store.create("b1", "exp1", "deepgram", "stt")
        store.create("b2", "exp1", "whisper", "stt")
        store.create("b3", "exp2", "elevenlabs", "tts")
        exp1_bench = store.list_all(experiment_id="exp1")
        assert len(exp1_bench) == 2


def test_list_by_provider():
    """Can filter benchmarks by provider."""
    with tempfile.TemporaryDirectory() as tmp:
        store = BenchmarkStore(Path(tmp))
        store.create("b1", "exp1", "deepgram", "stt")
        store.create("b2", "exp2", "deepgram", "stt")
        store.create("b3", "exp3", "whisper", "stt")
        deepgram_bench = store.list_all(provider="deepgram")
        assert len(deepgram_bench) == 2


def test_delete_benchmark():
    """Can delete a benchmark record."""
    with tempfile.TemporaryDirectory() as tmp:
        store = BenchmarkStore(Path(tmp))
        store.create("b1", "exp1", "deepgram", "stt")
        assert store.delete("b1") is True
        assert store.get("b1") is None


def test_benchmark_persistence():
    """Benchmarks persist across store instances."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        store1 = BenchmarkStore(path)
        store1.create("b1", "exp1", "deepgram", "stt", latency_ms=320)
        store2 = BenchmarkStore(path)
        bench = store2.get("b1")
        assert bench is not None
        assert bench.latency_ms == 320
