from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from accent_trainer.application.interfaces.object_storage import ObjectStorage
from accent_trainer.application.interfaces.tts_service import TTSService
from accent_trainer.config import Settings
from accent_trainer.infrastructure.storage.keys import reference_audio_key

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ReferenceAudio:
    bucket: str
    key: str
    url: str
    cached: bool                 # True если был в MinIO, False если только что синтезировано
    content_type: str = "audio/wav"


class GetReferenceAudio:
    """If reference exists in MinIO — return presigned URL.
    Else: synthesize via TTS, upload, then return URL.
    """

    def __init__(
        self,
        storage: ObjectStorage,
        tts: TTSService,
        settings: Settings,
    ) -> None:
        self._storage = storage
        self._tts = tts
        self._settings = settings

    async def execute(
        self,
        task_id: UUID,
        text: str,
        voice: str | None = None,
        url_ttl: timedelta = timedelta(hours=1),
    ) -> ReferenceAudio:
        bucket = self._settings.minio.bucket_reference_audio
        key = reference_audio_key(task_id=task_id, ext="wav")

        if await self._storage.object_exists(bucket, key):
            url = await self._storage.presigned_get_url(bucket, key, expires=url_ttl)
            return ReferenceAudio(bucket=bucket, key=key, url=url, cached=True)

        logger.info("Synthesizing reference for task %s (voice=%s)", task_id, voice)
        result = await self._tts.synthesize(text=text, voice=voice)
        await self._storage.put_object(
            bucket=bucket,
            key=key,
            data=result.audio,
            content_type=result.content_type,
            length=len(result.audio),
        )
        url = await self._storage.presigned_get_url(bucket, key, expires=url_ttl)
        return ReferenceAudio(bucket=bucket, key=key, url=url, cached=False)