"""Tests for component registry module."""

import tempfile
from pathlib import Path

from src.registry import ComponentRegistry, register_defaults
from src.models.types import ProviderCategory


def test_register_provider():
    """Can register a provider with metadata."""
    with tempfile.TemporaryDirectory() as tmp:
        reg = ComponentRegistry(Path(tmp))
        meta = reg.register("test-stt", "Test STT", ProviderCategory.STT)
        assert meta.id == "test-stt"
        assert meta.category == ProviderCategory.STT


def test_get_provider():
    """Can retrieve a provider by ID."""
    with tempfile.TemporaryDirectory() as tmp:
        reg = ComponentRegistry(Path(tmp))
        reg.register("test-stt", "Test STT", ProviderCategory.STT)
        meta = reg.get("test-stt")
        assert meta is not None
        assert meta.id == "test-stt"


def test_list_providers():
    """Can list all providers."""
    with tempfile.TemporaryDirectory() as tmp:
        reg = ComponentRegistry(Path(tmp))
        reg.register("stt-1", "STT 1", ProviderCategory.STT)
        reg.register("tts-1", "TTS 1", ProviderCategory.TTS)
        all_providers = reg.list_all()
        assert len(all_providers) == 2


def test_list_by_category():
    """Can filter providers by category."""
    with tempfile.TemporaryDirectory() as tmp:
        reg = ComponentRegistry(Path(tmp))
        reg.register("stt-1", "STT 1", ProviderCategory.STT)
        reg.register("stt-2", "STT 2", ProviderCategory.STT)
        reg.register("tts-1", "TTS 1", ProviderCategory.TTS)
        stt_providers = reg.list_all(ProviderCategory.STT)
        assert len(stt_providers) == 2
        assert all(p.category == ProviderCategory.STT for p in stt_providers)


def test_register_defaults():
    """Default providers are registered correctly."""
    with tempfile.TemporaryDirectory() as tmp:
        reg = ComponentRegistry(Path(tmp))
        register_defaults(reg)
        providers = reg.list_all()
        assert len(providers) == 4
        ids = {p.id for p in providers}
        assert ids == {"deepgram", "elevenlabs", "openai", "silero"}


def test_delete_provider():
    """Can delete a provider."""
    with tempfile.TemporaryDirectory() as tmp:
        reg = ComponentRegistry(Path(tmp))
        reg.register("test-stt", "Test STT", ProviderCategory.STT)
        assert reg.delete("test-stt") is True
        assert reg.get("test-stt") is None


def test_provider_persistence():
    """Providers persist across registry instances."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        reg1 = ComponentRegistry(path)
        reg1.register("test-stt", "Test STT", ProviderCategory.STT)
        reg2 = ComponentRegistry(path)
        meta = reg2.get("test-stt")
        assert meta is not None
        assert meta.name == "Test STT"
