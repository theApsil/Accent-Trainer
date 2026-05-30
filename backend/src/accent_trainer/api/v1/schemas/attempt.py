from __future__ import annotations

from pydantic import BaseModel, Field


class RecordingUploadedResponse(BaseModel):
    bucket: str = Field(..., examples=["user-recordings"])
    key: str = Field(..., examples=["users/<uuid>/2025/11/03/<uuid>.webm"])
    size: int
    content_type: str


class PresignedUrlResponse(BaseModel):
    url: str
    expires_in_seconds: int