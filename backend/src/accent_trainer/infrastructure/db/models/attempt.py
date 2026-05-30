from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Float

from accent_trainer.infrastructure.db.base import Base, TimestampMixin, UUIDMixin


class AttemptModel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "attempts"

    user_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    task_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    audio_key: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="pending", nullable=False)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    spectrogram_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    phoneme_reports: Mapped[list["PhonemeReportModel"]] = relationship(
        back_populates="attempt",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class PhonemeReportModel(Base, UUIDMixin):
    __tablename__ = "phoneme_reports"

    attempt_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("attempts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    phoneme: Mapped[str] = mapped_column(String(8), nullable=False)
    start_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    end_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)

    f1_hz: Mapped[float | None] = mapped_column(Float, nullable=True)
    f2_hz: Mapped[float | None] = mapped_column(Float, nullable=True)
    f3_hz: Mapped[float | None] = mapped_column(Float, nullable=True)
    f1_ref_hz: Mapped[float | None] = mapped_column(Float, nullable=True)
    f2_ref_hz: Mapped[float | None] = mapped_column(Float, nullable=True)
    tongue_height: Mapped[float | None] = mapped_column(Float, nullable=True)
    tongue_frontness: Mapped[float | None] = mapped_column(Float, nullable=True)
    advice_codes: Mapped[list[str]] = mapped_column(
        ARRAY(String(64)), default=list, nullable=False
    )

    attempt: Mapped["AttemptModel"] = relationship(back_populates="phoneme_reports")