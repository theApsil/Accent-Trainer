from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from accent_trainer.application.dto.asr import TranscriptionResult


class ASRService(ABC):
    @abstractmethod
    async def transcribe(self, audio_path: Path) -> TranscriptionResult:
        """Transcribe audio file into text + word-level timings."""