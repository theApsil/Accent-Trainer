from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from accent_trainer.application.interfaces.tts_service import (
    SynthesisResult,
    TTSService,
)
from accent_trainer.config import Settings
from accent_trainer.core.exceptions import AppError

logger = logging.getLogger(__name__)


class PiperUnavailableError(AppError):
    """Raised when piper binary or voice model is missing/misconfigured."""


class PiperSynthesisError(AppError):
    """Raised when piper exits with a non-zero status."""


class PiperTTSService(TTSService):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._voices_dir = Path(settings.tts.voices_dir).resolve()
        self._binary = settings.tts.piper_binary

    def _voice_model_path(self, voice: str) -> Path:
        path = self._voices_dir / f"{voice}.onnx"
        if not path.exists():
            raise PiperUnavailableError(
                f"Voice model not found: {path}. "
                f"Download .onnx and .onnx.json into {self._voices_dir}."
            )
        return path

    async def synthesize(
        self,
        text: str,
        voice: str | None = None,
    ) -> SynthesisResult:
        if not text.strip():
            raise PiperSynthesisError("Empty text")

        chosen_voice = voice or self._settings.tts.default_voice
        model_path = self._voice_model_path(chosen_voice)

        cmd = [
            self._binary,
            "--model",
            str(model_path),
            "--output_file",
            "-",          # stdout
        ]

        logger.debug("Running piper: %s", " ".join(cmd))

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            raise PiperUnavailableError(
                f"piper binary not found in PATH (binary={self._binary})"
            ) from exc

        stdout, stderr = await proc.communicate(input=text.encode("utf-8"))
        if proc.returncode != 0:
            raise PiperSynthesisError(
                f"piper failed (rc={proc.returncode}): {stderr.decode(errors='ignore')}"
            )
        if not stdout:
            raise PiperSynthesisError("piper produced empty output")

        return SynthesisResult(
            audio=stdout,
            content_type="audio/wav",
            sample_rate=self._settings.tts.sample_rate,
        )