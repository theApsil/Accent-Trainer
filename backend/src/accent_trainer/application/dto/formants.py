from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class FormantMeasurement:
    word: str
    phoneme: str
    start_ms: int
    end_ms: int
    f1_hz: float
    f2_hz: float
    confidence: float     # 0.0..1.0 — насколько устойчиво найдены форманты