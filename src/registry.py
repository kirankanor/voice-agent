from __future__ import annotations

from pathlib import Path
from typing import Any

from src.models.types import ProviderCategory, ProviderMetadata
from src.storage.file_store import read_yaml, write_yaml, list_dir


class ComponentRegistry:
    """Registry of voice providers with structured metadata."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.providers_dir = data_dir / "providers"
        self.providers_dir.mkdir(parents=True, exist_ok=True)

    def register(self, id: str, name: str, category: ProviderCategory,
                 capabilities: dict[str, bool] | None = None,
                 performance: dict[str, Any] | None = None,
                 economics: dict[str, Any] | None = None,
                 integration: dict[str, Any] | None = None,
                 constraints: dict[str, Any] | None = None) -> ProviderMetadata:
        """Register a new provider."""
        meta = ProviderMetadata(
            id=id,
            name=name,
            category=category,
            capabilities=capabilities or {},
            performance=performance or {},
            economics=economics or {},
            integration=integration or {},
            constraints=constraints or {},
        )
        self._save(meta)
        return meta

    def get(self, id: str) -> ProviderMetadata | None:
        """Get a provider by ID."""
        path = self.providers_dir / f"{id}.yaml"
        data = read_yaml(path)
        if not data:
            return None
        data["category"] = ProviderCategory(data["category"])
        return ProviderMetadata(**data)

    def list_all(self, category: ProviderCategory | None = None) -> list[ProviderMetadata]:
        """List all providers, optionally filtered by category."""
        providers = []
        for path in list_dir(self.providers_dir, ".yaml"):
            data = read_yaml(path)
            if data:
                data["category"] = ProviderCategory(data["category"])
                meta = ProviderMetadata(**data)
                if category is None or meta.category == category:
                    providers.append(meta)
        return providers

    def update(self, id: str, **kwargs: Any) -> ProviderMetadata | None:
        """Update a provider's metadata."""
        meta = self.get(id)
        if not meta:
            return None
        for key, value in kwargs.items():
            if hasattr(meta, key):
                setattr(meta, key, value)
        self._save(meta)
        return meta

    def delete(self, id: str) -> bool:
        """Delete a provider."""
        path = self.providers_dir / f"{id}.yaml"
        if path.exists():
            path.unlink()
            return True
        return False

    def _save(self, meta: ProviderMetadata) -> None:
        """Save provider metadata to YAML."""
        path = self.providers_dir / f"{meta.id}.yaml"
        data = {
            "id": meta.id,
            "name": meta.name,
            "category": meta.category.value,
            "capabilities": meta.capabilities,
            "performance": meta.performance,
            "economics": meta.economics,
            "integration": meta.integration,
            "constraints": meta.constraints,
        }
        write_yaml(path, data)


def register_defaults(registry: ComponentRegistry) -> None:
    """Register default V0 providers."""
    registry.register(
        id="deepgram",
        name="Deepgram",
        category=ProviderCategory.STT,
        capabilities={"streaming": True, "multilingual": True, "diarization": False},
        performance={"latency_ms": 320},
        economics={"price_per_minute": 0.0043},
        integration={"sdk": "deepgram-sdk", "python_support": True},
    )
    registry.register(
        id="elevenlabs",
        name="ElevenLabs",
        category=ProviderCategory.TTS,
        capabilities={"streaming": True, "voice_clone": True},
        performance={"latency_ms": 200},
        economics={"price_per_character": 0.00003},
        integration={"sdk": "elevenlabs", "python_support": True},
    )
    registry.register(
        id="openai",
        name="OpenAI",
        category=ProviderCategory.LLM,
        capabilities={"streaming": True, "function_calling": True},
        performance={"latency_ms": 500},
        economics={"price_per_1k_tokens": 0.002},
        integration={"sdk": "openai", "python_support": True},
    )
    registry.register(
        id="silero",
        name="Silero VAD",
        category=ProviderCategory.VAD,
        capabilities={"streaming": True, "real_time": True},
        performance={"latency_ms": 10},
        economics={"price_per_minute": 0},
        integration={"sdk": "silero-vad", "python_support": True},
    )
