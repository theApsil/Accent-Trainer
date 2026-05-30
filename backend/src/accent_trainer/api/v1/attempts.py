from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status

from accent_trainer.api.deps import get_object_storage
from accent_trainer.api.v1.schemas.attempt import (
    PresignedUrlResponse,
    RecordingUploadedResponse,
)
from accent_trainer.application.interfaces.object_storage import ObjectStorage
from accent_trainer.application.use_cases.upload_user_recording import (
    UploadUserRecording,
)
from accent_trainer.config import Settings, get_settings
from accent_trainer.core.exceptions import ValidationError
from accent_trainer.infrastructure.auth.users import current_active_user
from accent_trainer.infrastructure.db.models.user import UserModel

router = APIRouter()


@router.post(
    "/upload",
    response_model=RecordingUploadedResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a raw user recording (no analysis yet)",
)
async def upload_recording(
    file: UploadFile = File(...),
    user: UserModel = Depends(current_active_user),
    storage: ObjectStorage = Depends(get_object_storage),
    settings: Settings = Depends(get_settings),
) -> RecordingUploadedResponse:
    use_case = UploadUserRecording(storage=storage, settings=settings)
    content = await file.read()
    result = await use_case.execute(
        user_id=user.id,
        data=content,
        content_type=file.content_type or "application/octet-stream",
        size=len(content),
        filename=file.filename,
    )
    return RecordingUploadedResponse(
        bucket=result.bucket,
        key=result.key,
        size=result.size,
        content_type=result.content_type,
    )


@router.get(
    "/url",
    response_model=PresignedUrlResponse,
    summary="Get a presigned download URL for an uploaded recording",
)
async def get_recording_url(
    key: str = Query(..., description="Object key inside the user-recordings bucket"),
    expires_in: int = Query(3600, ge=60, le=24 * 3600),
    user: UserModel = Depends(current_active_user),
    storage: ObjectStorage = Depends(get_object_storage),
    settings: Settings = Depends(get_settings),
) -> PresignedUrlResponse:
    bucket = settings.minio.bucket_user_recordings

    # FIXME: Грубая авторизационная проверка: ключ должен начинаться с users/<твой_uuid>/
    expected_prefix = f"users/{user.id}/"
    if not key.startswith(expected_prefix):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not await storage.object_exists(bucket, key):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    url = await storage.presigned_get_url(
        bucket=bucket,
        key=key,
        expires=timedelta(seconds=expires_in),
    )
    return PresignedUrlResponse(url=url, expires_in_seconds=expires_in)