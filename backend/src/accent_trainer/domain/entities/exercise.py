from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class ExerciseKind(StrEnum):
    WORD = "word"
    MINIMAL_PAIR = "minimal_pair"
    PHRASE = "phrase"


@dataclass(slots=True)
class Exercise:
    id : UUID
    module: UUID
    kind : ExerciseKind
    title: str
    description: str
    order: int
    created_at: datetime
    updated_at: datetime