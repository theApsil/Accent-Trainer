from functools import lru_cache
from typing import Annotated, Literal

from pydantic import BeforeValidator, Field
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


def _split_csv(value: str | list[str]) -> list[str]:
    if isinstance(value, str):
        return [origin.strip() for origin in value.split(",") if origin.strip()]
    return value


CsvList = Annotated[list[str], NoDecode, BeforeValidator(_split_csv)]


class AppSettings(BaseSettings):
    """Application-level settings."""

    name: str = Field(default="accent-trainer", alias="APP_NAME")
    env: Literal["development", "production", "test"] = Field(
        default="development", alias="APP_ENV"
    )
    debug: bool = Field(default=True, alias="APP_DEBUG")
    host: str = Field(default="0.0.0.0", alias="APP_HOST")
    port: int = Field(default=8000, alias="APP_PORT")
    log_level: str = Field(default="INFO", alias="APP_LOG_LEVEL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class ApiSettings(BaseSettings):
    """API-related settings."""

    v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    cors_origins: CsvList = Field(default_factory=list, alias="CORS_ORIGINS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class PostgresSettings(BaseSettings):
    host: str = Field(default="localhost", alias="POSTGRES_HOST")
    port: int = Field(default=5432, alias="POSTGRES_PORT")
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    db: str = Field(alias="POSTGRES_DB")

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class RedisSettings(BaseSettings):
    host: str = Field(default="localhost", alias="REDIS_HOST")
    port: int = Field(default=6379, alias="REDIS_PORT")

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class MinioSettings(BaseSettings):
    endpoint: str = Field(default="localhost:9000", alias="MINIO_ENDPOINT")
    access_key: str = Field(alias="MINIO_ACCESS_KEY")
    secret_key: str = Field(alias="MINIO_SECRET_KEY")
    secure: bool = Field(default=False, alias="MINIO_SECURE")

    bucket_user_recordings: str = Field(alias="MINIO_BUCKET_USER_RECORDINGS")
    bucket_reference_audio: str = Field(alias="MINIO_BUCKET_REFERENCE_AUDIO")
    bucket_spectrograms: str = Field(alias="MINIO_BUCKET_SPECTROGRAMS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class AuthSettings(BaseSettings):
    """Authentication settings."""

    secret: str = Field(alias="AUTH_SECRET")
    jwt_lifetime_seconds: int = Field(default=3600, alias="AUTH_JWT_LIFETIME_SECONDS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class TTSSettings(BaseSettings):
    """Piper TTS settings."""

    piper_binary: str = Field(default="piper", alias="TTS_PIPER_BINARY")
    voices_dir: str = Field(default="data/piper_voices", alias="TTS_VOICES_DIR")
    default_voice: str = Field(
        default="en_US-lessac-medium", alias="TTS_DEFAULT_VOICE"
    )
    sample_rate: int = Field(default=22050, alias="TTS_SAMPLE_RATE")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):
    """Aggregate settings root."""

    app: AppSettings = Field(default_factory=AppSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)  # ← новое
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    minio: MinioSettings = Field(default_factory=MinioSettings)
    tts: TTSSettings = Field(default_factory=TTSSettings)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
