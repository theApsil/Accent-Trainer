from __future__ import annotations

from pydantic import BaseModel


class WordSegmentOut(BaseModel):
    word: str
    start_ms: int
    end_ms: int


class PhonemeSegmentOut(BaseModel):
    word: str
    phoneme: str
    start_ms: int
    end_ms: int


class PhonemeScoreOut(BaseModel):
    word: str
    phoneme: str
    start_ms: int
    end_ms: int
    f1_hz: float
    f2_hz: float
    f1_ref_hz: float | None
    f2_ref_hz: float | None
    distance: float | None
    score_0_100: float | None
    confidence: float


class AnalysisResponse(BaseModel):
    transcript: str
    language: str
    words: list[WordSegmentOut]
    phonemes: list[PhonemeSegmentOut]
    vowel_scores: list[PhonemeScoreOut]
    overall_score: float | None