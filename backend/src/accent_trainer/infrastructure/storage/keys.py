from __future__ import annotations

from datetime import datetime, timezone
from pathlib import PurePosixPath
from uuid import UUID, uuid4


def user_recording_key(user_id: UUID, attempt_id: UUID | None = None, ext: str = "wav") -> str:
    """E.g. users/<uid>/2025/11/03/<attempt_uuid>.wav"""
    aid = attempt_id or uuid4()
    now = datetime.now(timezone.utc)
    return str(
        PurePosixPath("users")
        / str(user_id)
        / f"{now:%Y}"
        / f"{now:%m}"
        / f"{now:%d}"
        / f"{aid}.{ext}"
    )


def reference_audio_key(task_id: UUID, ext: str = "wav") -> str:
    """E.g. tasks/<task_uuid>.wav"""
    return f"tasks/{task_id}.{ext}"


def spectrogram_key(attempt_id: UUID, ext: str = "png") -> str:
    return f"attempts/{attempt_id}.{ext}"