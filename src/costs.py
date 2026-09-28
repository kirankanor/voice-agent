from __future__ import annotations

from pathlib import Path
from typing import Any

from src.storage.file_store import read_yaml, write_yaml, list_dir


class CostCalculator:
    """Estimates per-conversation costs across voice components."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.costs_dir = data_dir / "costs"
        self.costs_dir.mkdir(parents=True, exist_ok=True)

    def estimate(self, stt_cost_per_min: float, tts_cost_per_char: float,
                 llm_cost_per_1k_tokens: float, avg_response_tokens: int = 200,
                 avg_chars_per_response: int = 800,
                 conversation_duration_min: float = 5.0,
                 avg_turns: int = 10) -> dict[str, Any]:
        """Estimate total conversation cost."""
        stt = stt_cost_per_min * conversation_duration_min
        tts = tts_cost_per_char * avg_chars_per_response * avg_turns
        llm = (llm_cost_per_1k_tokens / 1000) * avg_response_tokens * avg_turns
        total = stt + tts + llm

        return {
            "stt": round(stt, 4),
            "tts": round(tts, 4),
            "llm": round(llm, 4),
            "total": round(total, 4),
            "per_minute": round(total / conversation_duration_min, 4) if conversation_duration_min > 0 else 0,
            "per_1k_conversations": round(total * 1000, 2),
        }

    def save_estimate(self, id: str, provider_config: dict[str, Any],
                      estimate: dict[str, Any]) -> None:
        """Save a cost estimate."""
        path = self.costs_dir / f"{id}.yaml"
        data = {
            "id": id,
            "providers": provider_config,
            "estimate": estimate,
        }
        write_yaml(path, data)

    def get(self, id: str) -> dict[str, Any] | None:
        """Get a saved cost estimate."""
        path = self.costs_dir / f"{id}.yaml"
        data = read_yaml(path)
        return data if data else None

    def list_all(self) -> list[dict[str, Any]]:
        """List all saved cost estimates."""
        estimates = []
        for path in list_dir(self.costs_dir, ".yaml"):
            data = read_yaml(path)
            if data:
                estimates.append(data)
        return estimates
