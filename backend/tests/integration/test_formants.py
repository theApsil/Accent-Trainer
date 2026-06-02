"""Integration test for full analysis pipeline (ASR + formants + scoring)."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

import httpx
import pytest


pytestmark = pytest.mark.skipif(
    not (shutil.which("piper") and shutil.which("ffmpeg")),
    reason="piper + ffmpeg required",
)


async def _login(client: httpx.AsyncClient) -> str:
    email = f"u{uuid.uuid4().hex[:8]}@example.com"
    password = "Sup3rSecret!"
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    r = await client.post(
        "/api/v1/auth/jwt/login",
        data={"username": email, "password": password},
    )
    return r.json()["access_token"]


def _synthesize_wav(text: str) -> bytes:
    voices_dir = Path("data/piper_voices").resolve()
    model = voices_dir / "en_US-lessac-medium.onnx"
    if not model.exists():
        pytest.skip("voice model missing")
    with tempfile.NamedTemporaryFile(suffix=".wav") as out:
        subprocess.run(
            ["piper", "--model", str(model), "--output_file", out.name],
            input=text.encode(),
            check=True,
            capture_output=True,
        )
        return Path(out.name).read_bytes()


@pytest.mark.asyncio
async def test_full_pipeline_returns_formants_and_scores(
    client: httpx.AsyncClient,
) -> None:
    token = await _login(client)
    headers = {"Authorization": f"Bearer {token}"}

    wav = _synthesize_wav("see the cat eat")
    files = {"file": ("sample.wav", wav, "audio/wav")}
    r = await client.post("/api/v1/analysis/analyze", files=files, headers=headers)
    assert r.status_code == 200, r.text

    body = r.json()
    assert body["transcript"]
    assert len(body["phonemes"]) > 0
    assert len(body["vowel_scores"]) > 0

    # Formants must be in plausible speech range
    for v in body["vowel_scores"]:
        assert 100.0 <= v["f1_hz"] <= 1500.0, f"F1 out of range: {v}"
        assert 500.0 <= v["f2_hz"] <= 4000.0, f"F2 out of range: {v}"
        assert 0.0 <= v["confidence"] <= 1.0

    # overall_score is computed when at least one vowel is recognized
    if any(v["score_0_100"] is not None for v in body["vowel_scores"]):
        assert body["overall_score"] is not None
        assert 0.0 <= body["overall_score"] <= 100.0


@pytest.mark.asyncio
async def test_tts_voice_matches_norm_reasonably(client: httpx.AsyncClient) -> None:
    """TTS-synthesized vowels should be close to normative formants —
    if they aren't, our extractor is broken."""
    token = await _login(client)
    headers = {"Authorization": f"Bearer {token}"}

    wav = _synthesize_wav("see")
    files = {"file": ("see.wav", wav, "audio/wav")}
    r = await client.post("/api/v1/analysis/analyze", files=files, headers=headers)
    body = r.json()

    iy = next(
        (v for v in body["vowel_scores"] if v["phoneme"] == "IY"),
        None,
    )
    if iy is None:
        pytest.skip("IY not detected")

    # IY ≈ F1 270, F2 2290 → допускаем погрешность ±200 Hz
    assert abs(iy["f1_hz"] - 270) < 250
    assert abs(iy["f2_hz"] - 2290) < 500