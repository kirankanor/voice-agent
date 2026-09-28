"""Tests for provider Protocol classes and storage utilities."""

from src.providers.base import STTProvider, TTSProvider, LLMProvider, VADProvider
from src.storage.file_store import read_yaml, write_yaml, read_json, write_json
from src.models.types import ProviderCategory, ProviderMetadata, Project


def test_protocols_importable():
    """Provider protocols can be imported."""
    assert STTProvider is not None
    assert TTSProvider is not None
    assert LLMProvider is not None
    assert VADProvider is not None


def test_models_importable():
    """Data models can be imported."""
    assert ProviderCategory.STT == "stt"
    assert ProviderCategory.TTS == "tts"
    assert ProviderCategory.LLM == "llm"
    assert ProviderCategory.VAD == "vad"


def test_provider_metadata():
    """ProviderMetadata can be created with defaults."""
    meta = ProviderMetadata(
        id="test-stt",
        name="Test STT",
        category=ProviderCategory.STT,
    )
    assert meta.id == "test-stt"
    assert meta.capabilities == {}


def test_project_model():
    """Project model can be created."""
    project = Project(id="p1", name="Test Project", languages=["en", "hi"])
    assert project.id == "p1"
    assert project.status == "active"
