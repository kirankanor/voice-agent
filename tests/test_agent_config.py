"""Tests for agent configuration module."""

import tempfile
from pathlib import Path

from src.agent_config import AgentConfig


def test_create_config():
    """Can create an agent configuration."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = AgentConfig(Path(tmp))
        config = mgr.create("a1", "support-agent", languages=["en", "hi"],
                           stt_provider="deepgram", tts_provider="elevenlabs",
                           llm_provider="openai", vad_provider="silero")
        assert config["id"] == "a1"
        assert config["agent"]["name"] == "support-agent"
        assert config["voice"]["language"] == ["en", "hi"]


def test_get_config():
    """Can retrieve a configuration by ID."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = AgentConfig(Path(tmp))
        mgr.create("a1", "support-agent")
        config = mgr.get("a1")
        assert config is not None
        assert config["id"] == "a1"


def test_list_configs():
    """Can list all configurations."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = AgentConfig(Path(tmp))
        mgr.create("a1", "agent-1")
        mgr.create("a2", "agent-2")
        configs = mgr.list_all()
        assert len(configs) == 2


def test_update_config():
    """Can update a configuration."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = AgentConfig(Path(tmp))
        mgr.create("a1", "agent-1")
        updated = mgr.update("a1", tools=["lookup", "transfer"])
        assert updated is not None
        assert updated["tools"] == ["lookup", "transfer"]


def test_delete_config():
    """Can delete a configuration."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = AgentConfig(Path(tmp))
        mgr.create("a1", "agent-1")
        assert mgr.delete("a1") is True
        assert mgr.get("a1") is None


def test_validate_config():
    """Validation catches missing required fields."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = AgentConfig(Path(tmp))
        errors = mgr.validate({})
        assert len(errors) > 0
        assert "agent.name is required" in errors


def test_validate_complete_config():
    """Valid config passes validation."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = AgentConfig(Path(tmp))
        config = mgr.create("a1", "agent-1", stt_provider="deepgram",
                           tts_provider="elevenlabs", llm_provider="openai")
        errors = mgr.validate(config)
        assert len(errors) == 0


def test_config_persistence():
    """Configurations persist across manager instances."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        mgr1 = AgentConfig(path)
        mgr1.create("a1", "support-agent")
        mgr2 = AgentConfig(path)
        config = mgr2.get("a1")
        assert config is not None
        assert config["agent"]["name"] == "support-agent"
