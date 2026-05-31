from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from accent_trainer.application.dto.asr import AlignmentResult
from accent_trainer.application.dto.formants import FormantMeasurement


class FormantExtractor(ABC):
    @abstractmethod
    async def extract(
        self,
        audio_path: Path,
        alignment: AlignmentResult,
    ) -> list[FormantMeasurement]:
        """Return F1/F2 for each vowel phoneme segment."""