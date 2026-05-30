from __future__ import annotations

import io
import uuid

import httpx
import pytest


def _wav_bytes() -> bytes:
    """Minimal valid WAV header + tiny payload."""
    return (
        b"RIFF$\x00\x00\x00WAVEfmt "
        b"\x10\x00\x00\x00\x01\x00\x01\x00\x40\x1f\x00\x00\x80\x3e\x00\x00"
        b"\x02\x00\x10\x00data\x00\x00\x00\x00"
    )


async def _register_and_login(client: httpx.AsyncClient) -> str:
    email = f"u{uuid.uuid4().hex[:8]}@example.com"
    password = "Sup3rSecret!"
    r = await client.post(
        "/api/v1/auth/register", json={"email": email, "password": password}
    )
    assert r.status_code == 201, r.text
    r = await client.post(
        "/api/v1/auth/jwt/login",
        data={"username": email, "password": password},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


@pytest.mark.asyncio
async def test_upload_and_presign_roundtrip(client: httpx.AsyncClient) -> None:
    token = await _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    files = {"file": ("sample.wav", io.BytesIO(_wav_bytes()), "audio/wav")}
    r = await client.post("/api/v1/attempts/upload", files=files, headers=headers)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["bucket"]
    assert body["key"].endswith(".wav")
    assert body["size"] > 0

    r = await client.get(
        "/api/v1/attempts/url",
        params={"key": body["key"], "expires_in": 120},
        headers=headers,
    )
    assert r.status_code == 200, r.text
    assert r.json()["url"].startswith("http")


@pytest.mark.asyncio
async def test_upload_rejects_bad_content_type(client: httpx.AsyncClient) -> None:
    token = await _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    files = {"file": ("doc.txt", io.BytesIO(b"hello"), "text/plain")}
    r = await client.post("/api/v1/attempts/upload", files=files, headers=headers)
    assert r.status_code == 400
    assert "Unsupported" in r.json()["detail"]


@pytest.mark.asyncio
async def test_presign_forbids_other_users_keys(client: httpx.AsyncClient) -> None:
    token = await _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    foreign_key = f"users/{uuid.uuid4()}/2025/01/01/{uuid.uuid4()}.wav"
    r = await client.get(
        "/api/v1/attempts/url",
        params={"key": foreign_key},
        headers=headers,
    )
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_presign_404_for_missing_key(client: httpx.AsyncClient) -> None:
    token = await _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    me = await client.get("/api/v1/users/me", headers=headers)
    uid = me.json()["id"]
    missing_key = f"users/{uid}/2025/01/01/{uuid.uuid4()}.wav"

    r = await client.get(
        "/api/v1/attempts/url",
        params={"key": missing_key},
        headers=headers,
    )
    assert r.status_code == 404