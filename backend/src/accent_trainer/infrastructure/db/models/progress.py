from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from accent_trainer.infrastructure.db.base import Base, TimestampMixin, UUIDMixin


class ProgressModel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "progress"
    __table_args__ = (UniqueConstraint("user_id", "module_id", name="user_module"),)

    user_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    module_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("modules.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    completed_tasks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tasks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    final_check_passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_attempt_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )