from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from accent_trainer.application.dto.asr import AlignmentResult
from accent_trainer.application.dto.formants import FormantMeasurement
from accent_trainer.application.interfaces.formant_extractor import (
    FormantExtractor,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True, kw_only=True)
class FormantAnalysis:
    measurements: list[FormantMeasurement]


class ExtractFormants:
    def __init__(self, extractor: FormantExtractor) -> None:
        self._extractor = extractor

    async def execute(
        self,
        audio_path: Path,
        alignment: AlignmentResult,
    ) -> FormantAnalysis:
        measurements = await self._extractor.extract(audio_path, alignment)
        logger.info("Extracted formants for %d vowels", len(measurements))
        return FormantAnalysis(measurements=measurements)