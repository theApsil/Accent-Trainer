"""LPC-based formant extractor."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import librosa
import numpy as np
from scipy.signal import lfilter

from accent_trainer.application.dto.asr import AlignmentResult
from accent_trainer.application.dto.formants import FormantMeasurement
from accent_trainer.application.interfaces.formant_extractor import (
    FormantExtractor,
)
from accent_trainer.config import Settings
from accent_trainer.core.phonemes import is_vowel

logger = logging.getLogger(__name__)


class LPCFormantExtractor(FormantExtractor):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def extract(
        self,
        audio_path: Path,
        alignment: AlignmentResult,
    ) -> list[FormantMeasurement]:
        return await asyncio.to_thread(self._extract_sync, audio_path, alignment)

    def _extract_sync(
        self,
        audio_path: Path,
        alignment: AlignmentResult,
    ) -> list[FormantMeasurement]:
        sr_target = self._settings.audio.target_sample_rate
        y, sr = librosa.load(str(audio_path), sr=sr_target, mono=True)
        if len(y) == 0:
            return []

        out: list[FormantMeasurement] = []
        for seg in alignment.segments:
            if not is_vowel(seg.phoneme):
                continue

            i0 = int(seg.start_ms / 1000 * sr)
            i1 = int(seg.end_ms / 1000 * sr)
            if i1 <= i0 + 1:
                continue
            frame = y[i0:i1]

            if len(frame) < int(0.025 * sr):
                continue

            try:
                f1, f2, conf = self._estimate_f1_f2(frame, sr)
            except Exception as exc:  # noqa: BLE001
                logger.debug("formant failed for %s: %s", seg.phoneme, exc)
                continue

            if f1 <= 0 or f2 <= 0:
                continue

            out.append(
                FormantMeasurement(
                    word=seg.word,
                    phoneme=seg.phoneme,
                    start_ms=seg.start_ms,
                    end_ms=seg.end_ms,
                    f1_hz=round(float(f1), 1),
                    f2_hz=round(float(f2), 1),
                    confidence=round(float(conf), 3),
                )
            )

        return out

    # ------------------------------------------------------------------ core

    def _estimate_f1_f2(
        self,
        frame: np.ndarray,
        sr: int,
    ) -> tuple[float, float, float]:
        """Estimate F1, F2 via LPC + root analysis.

        Algorithm:
        1. Pre-emphasis (boost high freqs).
        2. Hamming window.
        3. LPC of order `audio_lpc_order` (librosa.lpc).
        4. Roots of LPC polynomial that lie inside the unit circle.
        5. Convert angles to Hz, keep formant candidates in [min_hz, max_hz].
        6. Confidence ~ resonance bandwidth (narrow = sharp peak = high conf).
        """
        cfg = self._settings.audio

        # 1. Pre-emphasis: H(z) = 1 − 0.97 z^-1
        emphasized = lfilter([1.0, -0.97], [1.0], frame.astype(np.float64))

        # 2. Window
        windowed = emphasized * np.hamming(len(emphasized))

        # 3. LPC
        order = cfg.formant_lpc_order
        a = librosa.lpc(windowed, order=order)

        # 4. Roots → angles
        roots = np.roots(a)
        roots = roots[np.imag(roots) >= 0]      # keep upper half-plane
        roots = roots[np.abs(roots) < 1.0]      # inside unit circle (stable)
        if len(roots) == 0:
            return 0.0, 0.0, 0.0

        angles = np.arctan2(np.imag(roots), np.real(roots))
        freqs = angles * (sr / (2.0 * np.pi))

        # Bandwidths: BW = -(sr / pi) * ln(|r|)
        bandwidths = -(sr / np.pi) * np.log(np.abs(roots) + 1e-12)

        # Sort by frequency
        order_idx = np.argsort(freqs)
        freqs = freqs[order_idx]
        bandwidths = bandwidths[order_idx]

        mask = (
            (freqs >= cfg.formant_min_hz)
            & (freqs <= cfg.formant_max_hz)
            & (bandwidths < 400.0)
        )
        candidate_f = freqs[mask]
        candidate_bw = bandwidths[mask]

        if len(candidate_f) < 2:
            return 0.0, 0.0, 0.0

        f1, f2 = float(candidate_f[0]), float(candidate_f[1])
        bw1, bw2 = float(candidate_bw[0]), float(candidate_bw[1])

        # Confidence heuristic: narrower bandwidth ≈ sharper formant.
        # Map BW in [50..400] -> conf in [1.0..0.0].
        def _bw_to_conf(bw: float) -> float:
            return max(0.0, min(1.0, 1.0 - (bw - 50.0) / 350.0))

        conf = (_bw_to_conf(bw1) + _bw_to_conf(bw2)) / 2.0
        return f1, f2, conf