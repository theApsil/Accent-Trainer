from __future__ import annotations

import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

import httpx
import pytest


pytestmark = pytest.mark.skipif(
    not shutil.which("piper"),
    reason="piper required to synthesize test audio",
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


def _synthesize_wav(text: str, voices_dir: Path) -> bytes:
    """Use piper directly to generate a tiny test WAV."""
    model = voices_dir / "en_US-lessac-medium.onnx"
    assert model.exists(), f"voice model missing: {model}"

    with tempfile.NamedTemporaryFile(suffix=".wav") as out:
        subprocess.run(
            ["piper", "--model", str(model), "--output_file", out.name],
            input=text.encode(),
            check=True,
            capture_output=True,
        )
        return Path(out.name).read_bytes()


@pytest.mark.asyncio
async def test_analyze_returns_transcript_and_phonemes(
    client: httpx.AsyncClient,
) -> None:
    voices_dir = Path("data/piper_voices").resolve()
    if not (voices_dir / "en_US-lessac-medium.onnx").exists():
        pytest.skip("voice model missing")

    token = await _login(client)
    headers = {"Authorization": f"Bearer {token}"}

    wav = _synthesize_wav("Hello world", voices_dir)
    files = {"file": ("sample.wav", wav, "audio/wav")}
    r = await client.post("/api/v1/analysis/analyze", files=files, headers=headers)
    assert r.status_code == 200, r.text

    body = r.json()
    assert body["language"] == "en"
    assert "hello" in body["transcript"].lower()
    assert len(body["words"]) >= 1
    assert len(body["phonemes"]) >= 2

    for p in body["phonemes"]:
        assert p["end_ms"] > p["start_ms"]
        assert p["phoneme"].isupper()  # ARPAbet


@pytest.mark.asyncio
async def test_analyze_rejects_bad_mime(client: httpx.AsyncClient) -> None:
    token = await _login(client)
    headers = {"Authorization": f"Bearer {token}"}

    files = {"file": ("a.txt", b"hi", "text/plain")}
    r = await client.post("/api/v1/analysis/analyze", files=files, headers=headers)
    assert r.status_code == 400