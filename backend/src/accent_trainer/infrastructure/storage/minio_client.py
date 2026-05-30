from __future__ import annotations

import logging
from functools import lru_cache

from minio import Minio

from accent_trainer.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_minio_client() -> Minio:
    settings = get_settings().minio
    return Minio(
        endpoint=settings.endpoint,
        access_key=settings.access_key,
        secret_key=settings.secret_key,
        secure=settings.secure,
    )


def ensure_buckets() -> None:
    """Create required buckets if missing. Useful for app startup."""
    settings = get_settings().minio
    client = get_minio_client()
    for bucket in (
        settings.bucket_user_recordings,
        settings.bucket_reference_audio,
        settings.bucket_spectrograms,
    ):
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
            logger.info("Created MinIO bucket: %s", bucket)