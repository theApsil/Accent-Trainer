from __future__ import annotations

import asyncio
import logging
from functools import lru_cache
from pathlib import Path

from faster_whisper import WhisperModel

from accent_trainer.application.dto.asr import TranscriptionResult, WordSegment
from accent_trainer.application.interfaces.asr_service import ASRService
from accent_trainer.config import Settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_model(name: str, device: str, compute_type: str, download_root: str) -> WhisperModel:
    logger.info(
        "Loading faster-whisper model=%s device=%s compute=%s",
        name, device, compute_type,
    )
    return WhisperModel(
        model_size_or_path=name,
        device=device,
        compute_type=compute_type,
        download_root=download_root,
    )


class FasterWhisperASR(ASRService):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def _model(self) -> WhisperModel:
        a = self._settings.asr
        return _get_model(a.whisper_model, a.whisper_device, a.whisper_compute_type, a.models_dir)

    async def transcribe(self, audio_path: Path) -> TranscriptionResult:
        def _run() -> TranscriptionResult:
            model = self._model()
            segments, info = model.transcribe(
                str(audio_path),
                language=self._settings.asr.language,
                word_timestamps=True,
                vad_filter=False,
            )
            words: list[WordSegment] = []
            text_chunks: list[str] = []
            for seg in segments:
                text_chunks.append(seg.text)
                if seg.words:
                    for w in seg.words:
                        clean = w.word.strip()
                        if not clean:
                            continue
                        words.append(
                            WordSegment(
                                word=clean,
                                start_ms=int((w.start or 0.0) * 1000),
                                end_ms=int((w.end or 0.0) * 1000),
                            )
                        )

            return TranscriptionResult(
                text="".join(text_chunks).strip(),
                language=info.language,
                words=words,
            )

        return await asyncio.to_thread(_run)