from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ProviderCategory(str, Enum):
    STT = "stt"
    TTS = "tts"
    LLM = "llm"
    VAD = "vad"


@dataclass
class ProviderMetadata:
    """Structured metadata for a voice provider."""

    id: str
    name: str
    category: ProviderCategory
    capabilities: dict[str, bool] = field(default_factory=dict)
    performance: dict[str, Any] = field(default_factory=dict)
    economics: dict[str, Any] = field(default_factory=dict)
    integration: dict[str, Any] = field(default_factory=dict)
    constraints: dict[str, Any] = field(default_factory=dict)


@dataclass
class Project:
    """A client project with requirements."""

    id: str
    name: str
    languages: list[str] = field(default_factory=list)
    latency_target_ms: int | None = None
    budget: str | None = None
    use_case: str = ""
    status: str = "active"


@dataclass
class Experiment:
    """A controlled comparison between providers."""

    id: str
    project_id: str
    experiment_type: str
    providers: list[str] = field(default_factory=list)
    configuration: dict[str, Any] = field(default_factory=dict)
    status: str = "defined"
    results: dict[str, Any] = field(default_factory=dict)


@dataclass
class Benchmark:
    """Benchmark result for a provider component."""

    id: str
    experiment_id: str
    provider: str
    component: str
    latency_ms: float | None = None
    quality: float | None = None
    cost: float | None = None
    failure_rate: float | None = None
    raw_result_path: str | None = None


@dataclass
class Decision:
    """Architecture decision record with provenance."""

    id: str
    project_id: str
    requirement: str
    candidates: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    experiment_ids: list[str] = field(default_factory=list)
    evidence: str = ""
    decision: str = ""
    trade_offs: str = ""
    rejected: list[str] = field(default_factory=list)
