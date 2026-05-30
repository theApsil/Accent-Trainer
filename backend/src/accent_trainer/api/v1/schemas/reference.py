from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class SynthesizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    voice: str | None = None


class ReferenceAudioResponse(BaseModel):
    bucket: str
    key: str
    url: str
    cached: bool
    task_id: UUID | None = None