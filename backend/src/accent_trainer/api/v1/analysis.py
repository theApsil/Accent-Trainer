from __future__ import annotations

import logging
import statistics
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile, status

from accent_trainer.api.deps import (
    get_aligner,
    get_asr_service,
    get_audio_converter,
    get_formant_extractor,
    get_g2p_service,
)
from accent_trainer.api.v1.schemas.analysis import (
    AnalysisResponse,
    PhonemeScoreOut,
    PhonemeSegmentOut,
    WordSegmentOut,
)
from accent_trainer.application.interfaces.aligner import Aligner
from accent_trainer.application.interfaces.asr_service import ASRService
from accent_trainer.application.interfaces.formant_extractor import (
    FormantExtractor,
)
from accent_trainer.application.interfaces.g2p_service import G2PService
from accent_trainer.application.use_cases.analyze_pronunciation import (
    AnalyzePronunciation,
)
from accent_trainer.application.use_cases.compare_to_norm import CompareToNorm
from accent_trainer.application.use_cases.extract_formants import ExtractFormants
from accent_trainer.core.exceptions import ValidationError
from accent_trainer.infrastructure.audio.converter import AudioConverter
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
    summary="ASR + phoneme alignment + formant scoring (synchronous)",
)
async def analyze(
    file: UploadFile = File(...),
    user: UserModel = Depends(current_active_user),
    converter: AudioConverter = Depends(get_audio_converter),
    asr: ASRService = Depends(get_asr_service),
    aligner: Aligner = Depends(get_aligner),
    g2p: G2PService = Depends(get_g2p_service),
    formant_extractor: FormantExtractor = Depends(get_formant_extractor),
) -> AnalysisResponse:
    content_type = file.content_type or ""
    if content_type not in _ALLOWED_MIME:
        raise ValidationError(f"Unsupported content-type: {content_type}")

    suffix = "." + (
        file.filename.rsplit(".", 1)[-1].lower()
        if file.filename and "." in file.filename
        else "wav"
    )
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        raw_path = Path(tmp.name)
        tmp.write(await file.read())

    normalized_path: Path | None = None
    try:
        normalized_path = await converter.to_wav_mono_16k(raw_path)

        pron_uc = AnalyzePronunciation(asr=asr, aligner=aligner, g2p=g2p)
        pron = await pron_uc.execute(audio_path=normalized_path)

        fmt_uc = ExtractFormants(extractor=formant_extractor)
        fmt = await fmt_uc.execute(
            audio_path=normalized_path,
            alignment=pron.alignment,
        )

        scores = CompareToNorm().execute(fmt.measurements)

        overall = (
            round(statistics.mean(s.score_0_100 for s in scores if s.score_0_100 is not None), 1)
            if any(s.score_0_100 is not None for s in scores)
            else None
        )

    finally:
        raw_path.unlink(missing_ok=True)
        if normalized_path is not None:
            normalized_path.unlink(missing_ok=True)

    return AnalysisResponse(
        transcript=pron.transcription.text,
        language=pron.transcription.language,
        words=[
            WordSegmentOut(word=w.word, start_ms=w.start_ms, end_ms=w.end_ms)
            for w in pron.transcription.words
        ],
        phonemes=[
            PhonemeSegmentOut(
                word=p.word, phoneme=p.phoneme,
                start_ms=p.start_ms, end_ms=p.end_ms,
            )
            for p in pron.alignment.segments
        ],
        vowel_scores=[
            PhonemeScoreOut(
                word=s.word, phoneme=s.phoneme,
                start_ms=s.start_ms, end_ms=s.end_ms,
                f1_hz=s.f1_hz, f2_hz=s.f2_hz,
                f1_ref_hz=s.f1_ref_hz, f2_ref_hz=s.f2_ref_hz,
                distance=s.distance, score_0_100=s.score_0_100,
                confidence=s.confidence,
            )
            for s in scores
        ],
        overall_score=overall,
    )