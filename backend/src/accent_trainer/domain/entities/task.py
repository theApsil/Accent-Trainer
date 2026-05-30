from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class Task:
    id: UUID
    exercise_id: UUID
    text: str
    phonemes: list[str] = field(default_factory=list)
    reference_audio_key: str | None = None
    order: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None
