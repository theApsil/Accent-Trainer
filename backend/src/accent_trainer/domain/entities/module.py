from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Module:
    id: UUID
    course_id: UUID
    slug: str
    title: str
    description: str
    target_phonemes: list[str] = field(default_factory=list)
    order: int = 0
    passing_threshold: float = 0.0
    final_check_sentence: str | None = None
    created_at: datetime | None
    updated_at: datetime | None