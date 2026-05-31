from __future__ import annotations

import logging
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile, status

from accent_trainer.api.deps import (
    get_aligner,
    get_asr_service,
    get_g2p_service,
)
from accent_trainer.api.v1.schemas.analysis import (
    AnalysisResponse,
    PhonemeSegmentOut,
    WordSegmentOut,
)
from accent_trainer.application.interfaces.aligner import Aligner
from accent_trainer.application.interfaces.asr_service import ASRService
from accent_trainer.application.interfaces.g2p_service import G2PService
from accent_trainer.application.use_cases.analyze_pronunciation import (
    AnalyzePronunciation,
)
from accent_trainer.core.exceptions import ValidationError
from accent_trainer.infrastructure.auth.users import current_active_user
from accent_trainer.infrastructure.db.models.user import UserModel

logger = logging.getLogger(__name__)

router = APIRouter()

_ALLOWED_MIME = {
    "audio/wav", "audio/x-wav", "audio/wave",
    "audio/webm", "audio/ogg", "audio/mpeg",
}


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="ASR + phoneme alignment of an uploaded recording (synchronous)",
)
async def analyze(
    file: UploadFile = File(...),
    user: UserModel = Depends(current_active_user),
    asr: ASRService = Depends(get_asr_service),
    aligner: Aligner = Depends(get_aligner),
    g2p: G2PService = Depends(get_g2p_service),
) -> AnalysisResponse:
    content_type = file.content_type or ""
    if content_type not in _ALLOWED_MIME:
        raise ValidationError(f"Unsupported content-type: {content_type}")

    suffix = "." + (file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else "wav")
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp_path = Path(tmp.name)
        tmp.write(await file.read())

    try:
        use_case = AnalyzePronunciation(asr=asr, aligner=aligner, g2p=g2p)
        result = await use_case.execute(audio_path=tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)

    return AnalysisResponse(
        transcript=result.transcription.text,
        language=result.transcription.language,
        words=[
            WordSegmentOut(word=w.word, start_ms=w.start_ms, end_ms=w.end_ms)
            for w in result.transcription.words
        ],
        phonemes=[
            PhonemeSegmentOut(
                word=p.word, phoneme=p.phoneme,
                start_ms=p.start_ms, end_ms=p.end_ms,
            )
            for p in result.alignment.segments
        ],
    )