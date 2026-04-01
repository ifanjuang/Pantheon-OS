"""
Modèles documents — Document, Chunk (RAG)

Chunk.embedding utilise pgvector (Vector) dont la dimension est configurable
via settings.EMBEDDING_DIM (défaut 768 pour nomic-embed-text).
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from core.settings import settings

try:
    from pgvector.sqlalchemy import Vector
    _VECTOR_AVAILABLE = True
except ImportError:  # pgvector pas encore installé en dev local
    Vector = None
    _VECTOR_AVAILABLE = False


def _now() -> datetime:
    return datetime.now(timezone.utc)


# Couches de connaissance (cf. ARCHITECTURE.md §3)
COUCHES = ("public", "agence", "projet", "sensible")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    affaire_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("affaires.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    nom: Mapped[str] = mapped_column(String(512), nullable=False)
    couche: Mapped[str] = mapped_column(String(32), nullable=False, default="projet")
    type_doc: Mapped[str] = mapped_column(String(64), nullable=False, default="pdf")
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False, default="application/pdf")
    taille_octets: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    storage_key: Mapped[str] = mapped_column(String(1024), nullable=False)
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )

    affaire: Mapped["Affaire"] = relationship(back_populates="documents")  # type: ignore[name-defined]
    chunks: Mapped[list["Chunk"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Document {self.nom} [{self.couche}]>"


def _build_chunk_table():
    """
    Construit dynamiquement la classe Chunk selon la disponibilité de pgvector.
    Si pgvector n'est pas disponible (dev local sans la lib), la colonne embedding
    est omise — la migration réelle l'inclura toujours.
    """
    extra_cols = {}
    extra_indexes = []

    if _VECTOR_AVAILABLE:
        from pgvector.sqlalchemy import Vector as V

        class Chunk(Base):
            __tablename__ = "chunks"
            __table_args__ = (
                Index(
                    "ix_chunks_embedding_hnsw",
                    "embedding",
                    postgresql_using="hnsw",
                    postgresql_with={"m": 16, "ef_construction": 64},
                    postgresql_ops={"embedding": "vector_cosine_ops"},
                ),
            )

            id: Mapped[uuid.UUID] = mapped_column(
                UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
            )
            document_id: Mapped[uuid.UUID] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("documents.id", ondelete="CASCADE"),
                nullable=False,
                index=True,
            )
            affaire_id: Mapped[uuid.UUID | None] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("affaires.id", ondelete="CASCADE"),
                nullable=True,
                index=True,
            )
            contenu: Mapped[str] = mapped_column(Text, nullable=False)
            embedding: Mapped[list[float]] = mapped_column(
                V(settings.EMBEDDING_DIM), nullable=True
            )
            chunk_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
            meta: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
            created_at: Mapped[datetime] = mapped_column(
                DateTime(timezone=True), nullable=False, default=_now
            )

            document: Mapped["Document"] = relationship(back_populates="chunks")

            def __repr__(self) -> str:
                return f"<Chunk doc={self.document_id} idx={self.chunk_index}>"

    else:
        class Chunk(Base):  # type: ignore[no-redef]
            __tablename__ = "chunks"

            id: Mapped[uuid.UUID] = mapped_column(
                UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
            )
            document_id: Mapped[uuid.UUID] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("documents.id", ondelete="CASCADE"),
                nullable=False,
                index=True,
            )
            affaire_id: Mapped[uuid.UUID | None] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("affaires.id", ondelete="CASCADE"),
                nullable=True,
                index=True,
            )
            contenu: Mapped[str] = mapped_column(Text, nullable=False)
            chunk_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
            meta: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
            created_at: Mapped[datetime] = mapped_column(
                DateTime(timezone=True), nullable=False, default=_now
            )

            document: Mapped["Document"] = relationship(back_populates="chunks")

            def __repr__(self) -> str:
                return f"<Chunk doc={self.document_id} idx={self.chunk_index}>"

    return Chunk


Chunk = _build_chunk_table()
