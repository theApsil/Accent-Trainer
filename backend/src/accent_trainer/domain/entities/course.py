from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Course:
    id: UUID
    slug: str
    title: str
    description: str
    target_language: str
    source_language: str | None
    order: int
    created_at: datetime
    updated_at: datetime