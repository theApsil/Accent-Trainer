from __future__ import annotations

from datetime import timedelta
from uuid import UUID, uuid5, NAMESPACE_URL

from fastapi import APIRouter, Depends, status

from accent_trainer.api.deps import get_object_storage, get_tts_service
from accent_trainer.api.v1.schemas.reference import (
    ReferenceAudioResponse,
    SynthesizeRequest,
)
from accent_trainer.application.interfaces.object_storage import ObjectStorage
from accent_trainer.application.interfaces.tts_service import TTSService
from accent_trainer.application.use_cases.get_reference_audio import (
    GetReferenceAudio,
)
from accent_trainer.config import Settings, get_settings
from accent_trainer.infrastructure.auth.users import current_active_user
from accent_trainer.infrastructure.db.models.user import UserModel

router = APIRouter()


@router.post(
    "/synthesize",
    response_model=ReferenceAudioResponse,
    status_code=status.HTTP_200_OK,
    summary="Synthesize (or fetch cached) reference audio for arbitrary text",
)
async def synthesize_reference(
    payload: SynthesizeRequest,
    user: UserModel = Depends(current_active_user),
    storage: ObjectStorage = Depends(get_object_storage),
    tts: TTSService = Depends(get_tts_service),
    settings: Settings = Depends(get_settings),
) -> ReferenceAudioResponse:

    task_id = uuid5(NAMESPACE_URL, f"adhoc/{payload.text}/{payload.voice or ''}")
    use_case = GetReferenceAudio(storage=storage, tts=tts, settings=settings)

    ref = await use_case.execute(
        task_id=task_id,
        text=payload.text,
        voice=payload.voice,
        url_ttl=timedelta(hours=1),
    )
    return ReferenceAudioResponse(
        bucket=ref.bucket, key=ref.key, url=ref.url, cached=ref.cached, task_id=task_id
    )


@router.get(
    "/{task_id}",
    response_model=ReferenceAudioResponse,
    summary="Get cached reference audio URL for a given Task (synthesizes if missing)",
)
async def get_reference_by_task(
    task_id: UUID,
    text: str,  # пока берём текст из query — позже подменим на load by task_id
    voice: str | None = None,
    user: UserModel = Depends(current_active_user),
    storage: ObjectStorage = Depends(get_object_storage),
    tts: TTSService = Depends(get_tts_service),
    settings: Settings = Depends(get_settings),
) -> ReferenceAudioResponse:
    use_case = GetReferenceAudio(storage=storage, tts=tts, settings=settings)
    ref = await use_case.execute(task_id=task_id, text=text, voice=voice)
    return ReferenceAudioResponse(
        bucket=ref.bucket, key=ref.key, url=ref.url, cached=ref.cached, task_id=task_id
    )