from __future__ import annotations

import logging
import re

from accent_trainer.application.dto.asr import (
    AlignmentResult,
    PhonemeSegment,
    TranscriptionResult,
)
from accent_trainer.application.interfaces.aligner import Aligner
from accent_trainer.application.interfaces.g2p_service import G2PService

logger = logging.getLogger(__name__)

_PUNCT = re.compile(r"[^\w'-]+")


class ProxyAligner(Aligner):
    async def align(
        self,
        transcription: TranscriptionResult,
        g2p: G2PService,
    ) -> AlignmentResult:
        out: list[PhonemeSegment] = []

        for w in transcription.words:
            word_clean = _PUNCT.sub("", w.word).lower()
            if not word_clean:
                continue
            phonemes = g2p.to_phonemes(word_clean)
            if not phonemes:
                continue

            total = max(w.end_ms - w.start_ms, 1)
            step = total / len(phonemes)

            for i, ph in enumerate(phonemes):
                start = int(w.start_ms + i * step)
                end = int(w.start_ms + (i + 1) * step) if i < len(phonemes) - 1 else w.end_ms
                if end <= start:
                    end = start + 1  # ensure non-zero duration
                out.append(
                    PhonemeSegment(
                        word=word_clean,
                        phoneme=ph,
                        start_ms=start,
                        end_ms=end,
                    )
                )

        return AlignmentResult(segments=out)