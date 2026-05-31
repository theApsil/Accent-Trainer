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


class AnalysisResponse(BaseModel):
    transcript: str
    language: str
    words: list[WordSegmentOut]
    phonemes: list[PhonemeSegmentOut]