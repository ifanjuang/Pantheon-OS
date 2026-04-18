"""
StorageService — wrapper MinIO S3-compatible (§1b).
Bucket unique : arceus-files
Clé : {affaire_id}/{module}/{filename}
"""

import io
import time
from uuid import UUID
from typing import Optional

from minio import Minio
from minio.error import S3Error
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from core.settings import settings
from core.logging import get_logger

log = get_logger("storage_service")


def _build_client() -> Minio:
    return Minio(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        secure=settings.MINIO_SECURE,
    )


class StorageService:
    _client: Optional[Minio] = None

    @classmethod
    def _get_client(cls) -> Minio:
        if cls._client is None:
            cls._client = _build_client()
            cls._ensure_bucket()
        return cls._client

    @classmethod
    def _ensure_bucket(cls) -> None:
        client = cls._client
        if not client.bucket_exists(settings.MINIO_BUCKET):
            client.make_bucket(settings.MINIO_BUCKET)
            log.info("storage.bucket_created", bucket=settings.MINIO_BUCKET)

    @classmethod
    def _key(cls, affaire_id: UUID, module: str, filename: str) -> str:
        return f"{affaire_id}/{module}/{filename}"

    @classmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type((S3Error, ConnectionError, OSError)),
        reraise=True,
    )
    async def upload(
        cls,
        affaire_id: UUID,
        module: str,
        filename: str,
        content: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Upload un fichier et retourne la clé MinIO."""
        t0 = time.monotonic()
        key = cls._key(affaire_id, module, filename)
        cls._get_client().put_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=key,
            data=io.BytesIO(content),
            length=len(content),
            content_type=content_type,
        )
        log.info("storage.upload", key=key, size=len(content), duration_ms=int((time.monotonic() - t0) * 1000))
        return key

    @classmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type((S3Error, ConnectionError, OSError)),
        reraise=True,
    )
    async def download(cls, key: str) -> bytes:
        """Télécharge un fichier depuis MinIO."""
        t0 = time.monotonic()
        response = cls._get_client().get_object(settings.MINIO_BUCKET, key)
        data = response.read()
        response.close()
        log.info("storage.download", key=key, size=len(data), duration_ms=int((time.monotonic() - t0) * 1000))
        return data

    @classmethod
    async def presigned_url(cls, key: str, expires_seconds: int = 3600) -> str:
        """Génère une URL présignée temporaire."""
        from datetime import timedelta

        url = cls._get_client().presigned_get_object(
            settings.MINIO_BUCKET, key, expires=timedelta(seconds=expires_seconds)
        )
        return url

    @classmethod
    async def delete(cls, key: str) -> None:
        cls._get_client().remove_object(settings.MINIO_BUCKET, key)
        log.info("storage.delete", key=key)

    @classmethod
    async def list_files(cls, affaire_id: UUID, module: Optional[str] = None) -> list[dict]:
        """Liste les fichiers d'une affaire (optionnellement filtrés par module)."""
        prefix = f"{affaire_id}/{module}/" if module else f"{affaire_id}/"
        objects = cls._get_client().list_objects(settings.MINIO_BUCKET, prefix=prefix, recursive=True)
        return [{"key": obj.object_name, "size": obj.size, "last_modified": obj.last_modified} for obj in objects]

    @classmethod
    async def ping(cls) -> bool:
        """Vérifie que MinIO est accessible."""
        try:
            cls._get_client().list_buckets()
            return True
        except Exception as e:
            log.warning("storage.ping_failed", error=str(e))
            return False
