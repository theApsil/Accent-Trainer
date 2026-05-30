from __future__ import annotations

import asyncio
import io
import logging
from collections.abc import AsyncIterator
from datetime import timedelta
from typing import IO

from minio.error import S3Error

from accent_trainer.application.interfaces.object_storage import ObjectStorage
from accent_trainer.infrastructure.storage.minio_client import get_minio_client

logger = logging.getLogger(__name__)


class MinIOStorage(ObjectStorage):
    """Async-friendly wrapper around the synchronous minio SDK."""

    def __init__(self) -> None:
        self._client = get_minio_client()

    async def put_object(
        self,
        bucket: str,
        key: str,
        data: IO[bytes] | bytes,
        content_type: str,
        length: int | None = None,
    ) -> None:
        if isinstance(data, bytes):
            stream = io.BytesIO(data)
            length = len(data)
        else:
            stream = data  # type: ignore[assignment]
            if length is None:
                raise ValueError("length must be provided when data is a stream")

        def _put() -> None:
            self._client.put_object(
                bucket_name=bucket,
                object_name=key,
                data=stream,
                length=length,  # type: ignore[arg-type]
                content_type=content_type,
            )

        await asyncio.to_thread(_put)
        logger.debug("Uploaded %s/%s (%d bytes, %s)", bucket, key, length, content_type)

    async def get_object(self, bucket: str, key: str) -> bytes:
        def _get() -> bytes:
            response = self._client.get_object(bucket, key)
            try:
                return response.read()
            finally:
                response.close()
                response.release_conn()

        return await asyncio.to_thread(_get)

    async def stream_object(
        self,
        bucket: str,
        key: str,
        chunk_size: int = 64 * 1024,
    ) -> AsyncIterator[bytes]:
        def _open() -> object:
            return self._client.get_object(bucket, key)

        response = await asyncio.to_thread(_open)
        try:
            while True:
                chunk = await asyncio.to_thread(response.read, chunk_size)  # type: ignore[attr-defined]
                if not chunk:
                    break
                yield chunk
        finally:
            await asyncio.to_thread(response.close)  # type: ignore[attr-defined]
            await asyncio.to_thread(response.release_conn)  # type: ignore[attr-defined]

    async def delete_object(self, bucket: str, key: str) -> None:
        def _delete() -> None:
            try:
                self._client.remove_object(bucket, key)
            except S3Error as exc:
                if exc.code != "NoSuchKey":
                    raise

        await asyncio.to_thread(_delete)

    async def object_exists(self, bucket: str, key: str) -> bool:
        def _stat() -> bool:
            try:
                self._client.stat_object(bucket, key)
                return True
            except S3Error as exc:
                if exc.code in {"NoSuchKey", "NoSuchObject", "NoSuchBucket"}:
                    return False
                if getattr(exc, "response", None) is not None:
                    status_code = getattr(exc.response, "status", None)
                    if status_code == 404:
                        return False
                raise

        return await asyncio.to_thread(_stat)

    async def presigned_get_url(
        self,
        bucket: str,
        key: str,
        expires: timedelta = timedelta(hours=1),
    ) -> str:
        def _sign() -> str:
            return self._client.presigned_get_object(bucket, key, expires=expires)

        return await asyncio.to_thread(_sign)