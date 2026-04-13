"""
Modèles wiki — Synthesis cache inspiré de llm-wiki.

Une WikiPage est une synthèse markdown navigable d'une décision validée
(project_decision) ou d'une analyse d'orchestre, réutilisable comme
précédent pour le bonus scoring « +5 déjà validé dans projets passés ».

Deux portées (scope) :
  - 'projet' : page liée à une affaire (historique local)
  - 'agence' : page promue comme précédent transverse (mémoire Mnémosyne)

L'embedding permet une recherche par similarité pour retrouver les
précédents quand on scored une nouvelle décision.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.settings import settings
from database import Base

try:
    from pgvector.sqlalchemy import Vector
    _VECTOR_AVAILABLE = True
except ImportError:  # pgvector non installé en dev local
    Vector = None
    _VECTOR_AVAILABLE = False


def _now() -> datetime:
    return datetime.now(timezone.utc)


# Portées reconnues
SCOPES = ("projet", "agence")


def _build_wiki_page_table():
    """
    Construit WikiPage avec ou sans colonne embedding selon la dispo de pgvector
    (même pattern que documents.Chunk).
    """
    if _VECTOR_AVAILABLE:
        from pgvector.sqlalchemy import Vector as V

        class WikiPage(Base):
            __tablename__ = "wiki_pages"
            __table_args__ = (
                UniqueConstraint("scope", "slug", name="uq_wiki_pages_scope_slug"),
                Index(
                    "ix_wiki_pages_embedding_hnsw",
                    "embedding",
                    postgresql_using="hnsw",
                    postgresql_with={"m": 16, "ef_construction": 64},
                    postgresql_ops={"embedding": "vector_cosine_ops"},
                ),
            )

            id: Mapped[uuid.UUID] = mapped_column(
                UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
            )
            affaire_id: Mapped[uuid.UUID | None] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("affaires.id", ondelete="CASCADE"),
                nullable=True,
                index=True,
            )
            scope: Mapped[str] = mapped_column(String(16), nullable=False, default="projet")
            slug: Mapped[str] = mapped_column(String(256), nullable=False)

            titre: Mapped[str] = mapped_column(String(512), nullable=False)
            sujet_norm: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
            # Forme normalisée (lowercase, accents retirés) pour lookup rapide

            contenu_md: Mapped[str] = mapped_column(Text, nullable=False)
            # Markdown avec wikilinks [[slug]] (pattern llm-wiki)

            tags: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
            # ["lot-3", "etancheite", "DTU-43.1"]

            criticite: Mapped[str | None] = mapped_column(String(2), nullable=True)
            # C1-C5 (reporté depuis la décision source)
            score: Mapped[int | None] = mapped_column(Integer, nullable=True)
            # 0-100 (score final de la décision source)

            decision_id: Mapped[uuid.UUID | None] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("project_decisions.id", ondelete="SET NULL"),
                nullable=True,
                index=True,
            )
            source_run_id: Mapped[uuid.UUID | None] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("orchestra_runs.id", ondelete="SET NULL"),
                nullable=True,
            )

            embedding: Mapped[list[float] | None] = mapped_column(
                V(settings.EMBEDDING_DIM), nullable=True
            )

            citations: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
            # [{"agent": "themis", "extrait": "...", "source": "chunk:<uuid>"}]

            validated_by: Mapped[uuid.UUID | None] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("users.id", ondelete="SET NULL"),
                nullable=True,
            )
            validated_at: Mapped[datetime | None] = mapped_column(
                DateTime(timezone=True), nullable=True
            )
            reuse_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
            # Incrémenté à chaque lookup "précédent" → alimente bonus scoring

            created_at: Mapped[datetime] = mapped_column(
                DateTime(timezone=True), nullable=False, default=_now
            )
            updated_at: Mapped[datetime] = mapped_column(
                DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
            )

            def __repr__(self) -> str:
                return f"<WikiPage {self.scope}:{self.slug}>"

    else:
        class WikiPage(Base):  # type: ignore[no-redef]
            __tablename__ = "wiki_pages"
            __table_args__ = (
                UniqueConstraint("scope", "slug", name="uq_wiki_pages_scope_slug"),
            )

            id: Mapped[uuid.UUID] = mapped_column(
                UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
            )
            affaire_id: Mapped[uuid.UUID | None] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("affaires.id", ondelete="CASCADE"),
                nullable=True,
                index=True,
            )
            scope: Mapped[str] = mapped_column(String(16), nullable=False, default="projet")
            slug: Mapped[str] = mapped_column(String(256), nullable=False)
            titre: Mapped[str] = mapped_column(String(512), nullable=False)
            sujet_norm: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
            contenu_md: Mapped[str] = mapped_column(Text, nullable=False)
            tags: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
            criticite: Mapped[str | None] = mapped_column(String(2), nullable=True)
            score: Mapped[int | None] = mapped_column(Integer, nullable=True)
            decision_id: Mapped[uuid.UUID | None] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("project_decisions.id", ondelete="SET NULL"),
                nullable=True,
                index=True,
            )
            source_run_id: Mapped[uuid.UUID | None] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("orchestra_runs.id", ondelete="SET NULL"),
                nullable=True,
            )
            citations: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
            validated_by: Mapped[uuid.UUID | None] = mapped_column(
                UUID(as_uuid=True),
                ForeignKey("users.id", ondelete="SET NULL"),
                nullable=True,
            )
            validated_at: Mapped[datetime | None] = mapped_column(
                DateTime(timezone=True), nullable=True
            )
            reuse_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
            created_at: Mapped[datetime] = mapped_column(
                DateTime(timezone=True), nullable=False, default=_now
            )
            updated_at: Mapped[datetime] = mapped_column(
                DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
            )

            def __repr__(self) -> str:
                return f"<WikiPage {self.scope}:{self.slug}>"

    return WikiPage


WikiPage = _build_wiki_page_table()
