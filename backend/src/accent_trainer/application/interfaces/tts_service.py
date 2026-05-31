"""Abstract TTS service interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SynthesisResult:
    audio: bytes          # raw WAV bytes (RIFF header included)
    content_type: str     # always "audio/wav" for Piper
    sample_rate: int


class TTSService(ABC):
    @abstractmethod
    async def synthesize(
        self,
        text: str,
        voice: str | None = None,
    ) -> SynthesisResult:
        """Synthesize given text into a WAV byte payload."""