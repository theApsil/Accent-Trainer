from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Progress:
    id: UUID
    user_id: UUID
    completed_tasks: int
    total_tasks: int
    final_check_passed: bool
    last_attempt_at: datetime | None
    created_at: datetime
    updated_at: datetime

    @property
    def percent(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return min(1.0, self.completed_tasks / self.total_tasks)
