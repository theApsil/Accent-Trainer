"""Use case: compare measured formants against normative reference."""

from __future__ import annotations

import math
from dataclasses import dataclass

from accent_trainer.application.dto.formants import FormantMeasurement
from accent_trainer.core.formant_norms import get_norm


@dataclass(slots=True, frozen=True, kw_only=True)
class PhonemeScore:
    word: str
    phoneme: str
    start_ms: int
    end_ms: int
    f1_hz: float
    f2_hz: float
    f1_ref_hz: float | None
    f2_ref_hz: float | None
    distance: float | None            # Euclidean in formant space (Hz)
    score_0_100: float | None         # 100 = perfect, 0 = very far
    confidence: float


# Эмпирический "плохой" порог: ~300 Hz Euclidean -> 0/100
_BAD_THRESHOLD_HZ = 300.0


class CompareToNorm:
    def execute(
        self,
        measurements: list[FormantMeasurement],
    ) -> list[PhonemeScore]:
        scored: list[PhonemeScore] = []
        for m in measurements:
            norm = get_norm(m.phoneme)
            if norm is None:
                scored.append(
                    PhonemeScore(
                        word=m.word,
                        phoneme=m.phoneme,
                        start_ms=m.start_ms,
                        end_ms=m.end_ms,
                        f1_hz=m.f1_hz,
                        f2_hz=m.f2_hz,
                        f1_ref_hz=None,
                        f2_ref_hz=None,
                        distance=None,
                        score_0_100=None,
                        confidence=m.confidence,
                    )
                )
                continue

            dist = math.hypot(m.f1_hz - norm.f1, m.f2_hz - norm.f2)
            score = max(0.0, 100.0 * (1.0 - dist / _BAD_THRESHOLD_HZ))
            scored.append(
                PhonemeScore(
                    word=m.word,
                    phoneme=m.phoneme,
                    start_ms=m.start_ms,
                    end_ms=m.end_ms,
                    f1_hz=m.f1_hz,
                    f2_hz=m.f2_hz,
                    f1_ref_hz=norm.f1,
                    f2_ref_hz=norm.f2,
                    distance=round(dist, 1),
                    score_0_100=round(score, 1),
                    confidence=m.confidence,
                )
            )
        return scored