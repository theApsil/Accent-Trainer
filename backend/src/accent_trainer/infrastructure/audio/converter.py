from __future__ import annotations

import asyncio
import logging
import tempfile
from pathlib import Path

from accent_trainer.config import Settings
from accent_trainer.core.exceptions import AppError

logger = logging.getLogger(__name__)


class AudioConversionError(AppError):
    """ffmpeg failed or produced no output."""


class AudioConverter:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def to_wav_mono_16k(self, src_path: Path) -> Path:
        """Convert any input audio to 16 kHz mono PCM WAV.

        Returns a path to a temporary file. Caller is responsible for deletion.
        """
        sr = self._settings.audio.target_sample_rate
        binary = self._settings.audio.ffmpeg_binary

        out = Path(
            tempfile.NamedTemporaryFile(
                suffix=".wav", delete=False, prefix="norm_"
            ).name
        )

        cmd = [
            binary,
            "-y",
            "-i", str(src_path),
            "-ac", "1",
            "-ar", str(sr),
            "-acodec", "pcm_s16le",
            str(out),
        ]
        logger.debug("ffmpeg cmd: %s", " ".join(cmd))

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            raise AudioConversionError(
                f"ffmpeg binary not found: {binary}"
            ) from exc

        _, stderr = await proc.communicate()
        if proc.returncode != 0 or not out.exists() or out.stat().st_size == 0:
            out.unlink(missing_ok=True)
            raise AudioConversionError(
                f"ffmpeg failed (rc={proc.returncode}): "
                f"{stderr.decode(errors='ignore')[:500]}"
            )

        return out