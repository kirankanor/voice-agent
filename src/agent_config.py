from __future__ import annotations

from pathlib import Path
from typing import Any

from src.storage.file_store import read_yaml, write_yaml, list_dir


class AgentConfig:
    """Declarative YAML-based agent configuration."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.configs_dir = data_dir / "agents"
        self.configs_dir.mkdir(parents=True, exist_ok=True)

    def create(self, id: str, name: str, languages: list[str] | None = None,
               stt_provider: str | None = None, tts_provider: str | None = None,
               llm_provider: str | None = None, vad_provider: str | None = None,
               conversation: dict[str, Any] | None = None,
               tools: list[str] | None = None,
               evaluation: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new agent configuration."""
        config = {
            "id": id,
            "agent": {"name": name},
            "voice": {"language": languages or ["en"]},
            "stt": {"provider": stt_provider},
            "tts": {"provider": tts_provider},
            "llm": {"provider": llm_provider},
            "vad": {"provider": vad_provider},
            "conversation": conversation or {"interruption": True, "max_turn_duration": 30},
            "tools": tools or [],
            "evaluation": evaluation or {},
        }
        self._save(config)
        return config

    def get(self, id: str) -> dict[str, Any] | None:
        """Get an agent configuration by ID."""
        path = self.configs_dir / f"{id}.yaml"
        data = read_yaml(path)
        return data if data else None

    def list_all(self) -> list[dict[str, Any]]:
        """List all agent configurations."""
        configs = []
        for path in list_dir(self.configs_dir, ".yaml"):
            data = read_yaml(path)
            if data:
                configs.append(data)
        return configs

    def update(self, id: str, **kwargs: Any) -> dict[str, Any] | None:
        """Update an agent configuration."""
        config = self.get(id)
        if not config:
            return None
        for key, value in kwargs.items():
            if key in config:
                config[key] = value
        self._save(config)
        return config

    def delete(self, id: str) -> bool:
        """Delete an agent configuration."""
        path = self.configs_dir / f"{id}.yaml"
        if path.exists():
            path.unlink()
            return True
        return False

    def validate(self, config: dict[str, Any]) -> list[str]:
        """Validate an agent configuration. Returns list of errors."""
        errors = []
        if not config.get("agent", {}).get("name"):
            errors.append("agent.name is required")
        if not config.get("stt", {}).get("provider"):
            errors.append("stt.provider is required")
        if not config.get("tts", {}).get("provider"):
            errors.append("tts.provider is required")
        if not config.get("llm", {}).get("provider"):
            errors.append("llm.provider is required")
        return errors

    def _save(self, config: dict[str, Any]) -> None:
        """Save agent configuration to YAML."""
        path = self.configs_dir / f"{config['id']}.yaml"
        write_yaml(path, config)
