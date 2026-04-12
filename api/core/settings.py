from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # ── Base de données ──────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://arceus:changeme@db:5432/arceus"
    DATABASE_URL_SYNC: str = "postgresql://arceus:changeme@db:5432/arceus"
    ASYNCPG_URL: str = "postgresql://arceus:changeme@db:5432/arceus"

    # ── Auth JWT ─────────────────────────────────────────────────
    JWT_SECRET_KEY: str = "changeme-secret-min-32-chars-please"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440
    ADMIN_EMAIL: str = "admin@agence.fr"
    ADMIN_PASSWORD: str = "changeme"

    # ── LLM ──────────────────────────────────────────────────────
    LLM_PROVIDER: str = "ollama"              # "ollama" | "openai"
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "mistral:7b"
    LLM_MODEL: Optional[str] = None           # override si openai
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_BASE_URL: str = "https://api.openai.com/v1"

    # ── Embeddings ───────────────────────────────────────────────
    EMBEDDING_PROVIDER: str = "ollama"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"
    EMBEDDING_MODEL: Optional[str] = None     # override si openai
    EMBEDDING_DIM: int = 768

    # ── MinIO ────────────────────────────────────────────────────
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ROOT_USER: str = "arceus"
    MINIO_ROOT_PASSWORD: str = "changeme-minio"
    MINIO_BUCKET: str = "arceus-files"
    MINIO_SECURE: bool = False

    # ── Notion ───────────────────────────────────────────────────
    NOTION_TOKEN: Optional[str] = None
    NOTION_DATABASE_AFFAIRES: Optional[str] = None
    NOTION_DATABASE_ACTIONS: Optional[str] = None

    # ── API ──────────────────────────────────────────────────────
    API_PORT: int = 8000
    API_WORKERS: int = 1
    DEBUG: bool = True

    # ── Rate limiting ────────────────────────────────────────────
    RATE_LIMIT_LLM: str = "10/minute"
    RATE_LIMIT_STANDARD: str = "100/minute"
    RATE_LIMIT_READ: str = "1000/minute"

    # ── SMTP ─────────────────────────────────────────────────────
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: str = "ARCEUS <notifications@agence.fr>"

    # ── Webhooks / Paperclip ─────────────────────────────────────
    WEBHOOK_SECRET: Optional[str] = None   # Si None → JWT_SECRET_KEY utilisé

    # ── Redis / ARQ ──────────────────────────────────────────────
    REDIS_URL: str = "redis://redis:6379/0"

    # ── Agents ───────────────────────────────────────────────────
    AGENTS_DIR: str = "/agents"

    # ── RAG avancé ────────────────────────────────────────────────
    CONTEXTUAL_RETRIEVAL: bool = True     # enrichissement LLM par chunk à l'ingestion
    RERANK_ENABLED: bool = False          # cross-encoder reranking post-RRF
    RERANK_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    # ── Capture / Whisper ────────────────────────────────────────
    WHISPER_ENDPOINT: Optional[str] = None  # ex: http://whisper:9000/v1/audio/transcriptions

    # ── Telegram ─────────────────────────────────────────────────
    TELEGRAM_TOKEN: Optional[str] = None
    TELEGRAM_DEFAULT_CHAT_ID: Optional[str] = None
    # Chat IDs autorisés, séparés par virgule. Vide = tous autorisés.
    TELEGRAM_ALLOWED_CHAT_IDS: Optional[str] = None

    # ── WhatsApp ─────────────────────────────────────────────────
    WHATSAPP_ENABLED: bool = False
    WHATSAPP_MODE: str = "meta"
    WA_PHONE_ID: Optional[str] = None
    WA_TOKEN: Optional[str] = None
    WA_TEMPLATE_NAME: str = "os_projet_alerte"
    EVOLUTION_API_KEY: str = "changeme-evolution"

    @property
    def effective_llm_model(self) -> str:
        if self.LLM_MODEL:
            return self.LLM_MODEL
        return self.OLLAMA_MODEL

    @property
    def effective_embedding_model(self) -> str:
        if self.EMBEDDING_MODEL:
            return self.EMBEDDING_MODEL
        return self.OLLAMA_EMBEDDING_MODEL


settings = Settings()
