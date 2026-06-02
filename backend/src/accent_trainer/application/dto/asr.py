from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True, kw_only=True)
class WordSegment:
    word: str
    start_ms: int
    end_ms: int


@dataclass(slots=True, frozen=True, kw_only=True)
class TranscriptionResult:
    text: str
    language: str
    words: list[WordSegment] = field(default_factory=list)


@dataclass(slots=True, frozen=True, kw_only=True)
class PhonemeSegment:
    word: str
    phoneme: str          # ARPAbet without stress digits (e.g. "EH")
    start_ms: int
    end_ms: int


@dataclass(slots=True, frozen=True, kw_only=True)
class AlignmentResult:
    segments: list[PhonemeSegment]