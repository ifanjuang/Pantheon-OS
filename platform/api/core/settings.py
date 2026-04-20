from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

_WEAK_SECRETS = {"changeme", "devpassword", "secret", "password", "admin", "test", "1234"}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # ── Database ─────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://pantheon:changeme@db:5432/pantheon"
    DATABASE_URL_SYNC: str = "postgresql://pantheon:changeme@db:5432/pantheon"
    ASYNCPG_URL: str = "postgresql://pantheon:changeme@db:5432/pantheon"

    # ── Auth JWT ─────────────────────────────────────────────────
    JWT_SECRET_KEY: str = "changeme-secret-min-32-chars-please"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440
    ADMIN_EMAIL: str = "admin@pantheon.ai"
    ADMIN_PASSWORD: str = "changeme"

    # ── LLM ──────────────────────────────────────────────────────
    LLM_PROVIDER: str = "ollama"  # "ollama" | "openai"
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "mistral:7b"
    LLM_MODEL: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_BASE_URL: str = "https://api.openai.com/v1"

    # ── Embeddings ───────────────────────────────────────────────
    EMBEDDING_PROVIDER: str = "ollama"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"
    EMBEDDING_MODEL: Optional[str] = None
    EMBEDDING_DIM: int = 768

    # ── API ──────────────────────────────────────────────────────
    API_PORT: int = 8000
    API_WORKERS: int = 1
    DEBUG: bool = True

    # ── Rate limiting ────────────────────────────────────────────
    RATE_LIMIT_LLM: str = "20/minute"
    RATE_LIMIT_STANDARD: str = "200/minute"
    RATE_LIMIT_READ: str = "1000/minute"

    # ── Runtime ──────────────────────────────────────────────────
    RUNTIME_DIR: str = "/runtime"
    CONFIG_DIR: str = "/config"

    # ── Domain ───────────────────────────────────────────────────
    DOMAIN: str = "architecture"
    DOMAIN_LABEL: str = "Architecture & Maîtrise d'Œuvre"

    # ── RAG ──────────────────────────────────────────────────────
    RAG_TOP_K: int = 10
    RAG_MIN_SCORE: float = 0.65
    RAG_HYBRID: bool = True
    CONTEXTUAL_RETRIEVAL: bool = False

    # ── SMTP (optional) ──────────────────────────────────────────
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: str = "Pantheon OS <notifications@pantheon.ai>"

    # ── V2 — disabled for MVP (kept for forward compatibility) ───
    REDIS_URL: str = "redis://redis:6379/0"
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ROOT_USER: str = "pantheon"
    MINIO_ROOT_PASSWORD: str = "changeme-minio"
    MINIO_BUCKET: str = "pantheon-files"
    MINIO_SECURE: bool = False

    @model_validator(mode="after")
    def reject_weak_secrets_in_production(self) -> "Settings":
        if self.DEBUG:
            return self
        errors = []
        if self.JWT_SECRET_KEY.lower().strip() in _WEAK_SECRETS or "changeme" in self.JWT_SECRET_KEY.lower():
            errors.append("JWT_SECRET_KEY")
        if self.ADMIN_PASSWORD.lower().strip() in _WEAK_SECRETS or "changeme" in self.ADMIN_PASSWORD.lower():
            errors.append("ADMIN_PASSWORD")
        if errors:
            raise ValueError(
                f"Weak secrets in production: {', '.join(errors)}. "
                "Set strong values in .env before running with DEBUG=false."
            )
        if len(self.JWT_SECRET_KEY) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters.")
        return self

    @property
    def effective_llm_model(self) -> str:
        return self.LLM_MODEL or self.OLLAMA_MODEL

    @property
    def effective_embedding_model(self) -> str:
        return self.EMBEDDING_MODEL or self.OLLAMA_EMBEDDING_MODEL


settings = Settings()
