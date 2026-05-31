from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from accent_trainer.application.dto.asr import (
    AlignmentResult,
    TranscriptionResult,
)
from accent_trainer.application.interfaces.aligner import Aligner
from accent_trainer.application.interfaces.asr_service import ASRService
from accent_trainer.application.interfaces.g2p_service import G2PService

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True, kw_only=True)
class PronunciationAnalysis:
    transcription: TranscriptionResult
    alignment: AlignmentResult


class AnalyzePronunciation:
    def __init__(
        self,
        asr: ASRService,
        aligner: Aligner,
        g2p: G2PService,
    ) -> None:
        self._asr = asr
        self._aligner = aligner
        self._g2p = g2p

    async def execute(self, audio_path: Path) -> PronunciationAnalysis:
        transcription = await self._asr.transcribe(audio_path)
        logger.info(
            "ASR: text=%r words=%d", transcription.text, len(transcription.words)
        )
        alignment = await self._aligner.align(transcription, self._g2p)
        logger.info("Alignment: %d phoneme segments", len(alignment.segments))
        return PronunciationAnalysis(
            transcription=transcription,
            alignment=alignment,
        )