from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class User:
    id: UUID
    email: str
    hashed_password: str
    native_language: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime