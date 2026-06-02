from __future__ import annotations

from abc import ABC, abstractmethod

from accent_trainer.application.dto.asr import (
    AlignmentResult,
    TranscriptionResult,
)
from accent_trainer.application.interfaces.g2p_service import G2PService


class Aligner(ABC):
    @abstractmethod
    async def align(
        self,
        transcription: TranscriptionResult,
        g2p: G2PService,
    ) -> AlignmentResult:
        """Map word-level timings to phoneme-level intervals."""