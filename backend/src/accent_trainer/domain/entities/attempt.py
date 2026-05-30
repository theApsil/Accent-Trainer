from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class AttemptStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True, kw_only=True)
class Attempt:
    id: UUID
    user_id: UUID
    task_id: UUID
    audio_key: str
    status: AttemptStatus
    transcript: str | None = None
    overall_score: float | None = None
    spectrogram_key: str | None = None
    error_message: str | None = None
    phoneme_reports: list["PhonemeReport"] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(slots=True, kw_only=True)
class PhonemeReport:
    id: UUID
    attempt_id: UUID
    phoneme: str
    start_ms: int
    end_ms: int
    score: float
    f1_hz: float | None = None
    f2_hz: float | None = None
    f3_hz: float | None = None
    f1_ref_hz: float | None = None
    f2_ref_hz: float | None = None
    tongue_height: float | None = None
    tongue_frontness: float | None = None
    advice_codes: list[str] = field(default_factory=list)
