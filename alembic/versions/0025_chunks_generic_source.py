"""Migration 0025 — chunks : source générique (courriers, observations, etc.)

Jusqu'ici chunks.document_id était NOT NULL, ce qui interdisait d'indexer
du texte sans passer par la table documents (fichier uploadé dans MinIO).

Cette migration :
  1. Rend document_id nullable  → les chunks sans fichier source sont valides
  2. Ajoute source_type VARCHAR(32)  → "courrier", "observation", "note", etc.
  3. Ajoute source_id UUID           → PK de l'entité source (courrier.id, …)
  4. Index composite (affaire_id, source_type, source_id) pour filtrage rapide

Compatibilité descendante : les chunks existants ont document_id non NULL,
source_type NULL, source_id NULL — aucune migration de données nécessaire.

Revision ID: 0025
Revises: 0024
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0025"
down_revision = "0024"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Rendre document_id nullable
    op.alter_column(
        "chunks",
        "document_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=True,
    )

    # 2. Ajouter source_type et source_id
    op.add_column("chunks", sa.Column("source_type", sa.String(32), nullable=True))
    op.add_column("chunks", sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=True))

    # 3. Index composite pour les lookups par source
    op.create_index(
        "ix_chunks_source",
        "chunks",
        ["affaire_id", "source_type", "source_id"],
        postgresql_where=sa.text("source_type IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("ix_chunks_source", table_name="chunks")
    op.drop_column("chunks", "source_id")
    op.drop_column("chunks", "source_type")
    op.alter_column(
        "chunks",
        "document_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=False,
    )
