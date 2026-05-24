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


@dataclass(slots=True)
class Attempt:
    id: UUID
    user_id: UUID
    task_id: UUID
    audio_key: str   # <- MinIO object key
    status: AttemptStatus
    transcript: str | None
    overall_score: float | None
    spectrogram_key: str | None
    error_message: str | None
    phoneme_reports: list["PhonemeReport"] = field(default_factory=list)
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class PhonemeReport:
    id: UUID
    attempt_id: UUID
    phoneme: str
    start_ms: int
    end_ms: int
    score: float
    f1_hz: float | None
    f2_hz: float | None
    f3_hz: float | None
    f1_ref_hz: float | None
    f2_ref_hz: float | None
    tongue_height: float | None
    tongue_frontness: float | None
    advice_codes: list[str] = field(default_factory=list)
