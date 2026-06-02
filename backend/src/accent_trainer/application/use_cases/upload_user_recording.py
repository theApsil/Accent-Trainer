from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import IO
from uuid import UUID, uuid4

from accent_trainer.application.interfaces.object_storage import ObjectStorage
from accent_trainer.config import Settings
from accent_trainer.core.exceptions import ValidationError
from accent_trainer.infrastructure.storage.keys import user_recording_key

logger = logging.getLogger(__name__)

ALLOWED_AUDIO_MIME = {
    "audio/wav",
    "audio/x-wav",
    "audio/wave",
    "audio/webm",
    "audio/ogg",
    "audio/mpeg",
}

MAX_AUDIO_BYTES = 25 * 1024 * 1024  # 25 MiB


@dataclass(slots=True)
class UploadedRecording:
    bucket: str
    key: str
    size: int
    content_type: str


class UploadUserRecording:
    def __init__(self, storage: ObjectStorage, settings: Settings) -> None:
        self._storage = storage
        self._settings = settings

    async def execute(
        self,
        user_id: UUID,
        data: IO[bytes],
        content_type: str,
        size: int,
        filename: str | None = None,
    ) -> UploadedRecording:
        if content_type not in ALLOWED_AUDIO_MIME:
            raise ValidationError(
                f"Unsupported audio content-type: {content_type}"
            )
        if size <= 0:
            raise ValidationError("Empty file")
        if size > MAX_AUDIO_BYTES:
            raise ValidationError(
                f"File too large: {size} bytes (max {MAX_AUDIO_BYTES})"
            )

        ext = _guess_extension(content_type, filename)
        attempt_id = uuid4()
        bucket = self._settings.minio.bucket_user_recordings
        key = user_recording_key(user_id=user_id, attempt_id=attempt_id, ext=ext)

        await self._storage.put_object(
            bucket=bucket,
            key=key,
            data=data,
            content_type=content_type,
            length=size,
        )

        logger.info("Stored recording %s/%s (%d bytes)", bucket, key, size)
        return UploadedRecording(
            bucket=bucket,
            key=key,
            size=size,
            content_type=content_type,
        )


def _guess_extension(content_type: str, filename: str | None) -> str:
    if filename and "." in filename:
        return filename.rsplit(".", 1)[-1].lower()
    return {
        "audio/wav": "wav",
        "audio/x-wav": "wav",
        "audio/wave": "wav",
        "audio/webm": "webm",
        "audio/ogg": "ogg",
        "audio/mpeg": "mp3",
    }.get(content_type, "bin")