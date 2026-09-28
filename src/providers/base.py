from __future__ import annotations

from typing import Protocol, Any


class STTProvider(Protocol):
    """Speech-to-Text provider interface."""

    async def transcribe(self, audio: bytes, language: str = "en") -> str:
        """Transcribe audio bytes to text."""
        ...

    async def transcribe_stream(self, audio_stream: Any, language: str = "en"):
        """Transcribe streaming audio to text."""
        ...


class TTSProvider(Protocol):
    """Text-to-Speech provider interface."""

    async def synthesize(self, text: str, voice: str = "default") -> bytes:
        """Synthesize text to audio bytes."""
        ...

    async def synthesize_stream(self, text: str, voice: str = "default"):
        """Synthesize text to streaming audio."""
        ...


class LLMProvider(Protocol):
    """Large Language Model provider interface."""

    async def generate(self, prompt: str, system: str = "", **kwargs) -> str:
        """Generate a response from a prompt."""
        ...

    async def stream(self, prompt: str, system: str = "", **kwargs):
        """Stream a response from a prompt."""
        ...


class VADProvider(Protocol):
    """Voice Activity Detection provider interface."""

    async def detect(self, audio: bytes) -> bool:
        """Detect if audio contains speech."""
        ...

    async def detect_stream(self, audio_stream: Any):
        """Detect speech in streaming audio."""
        ...
