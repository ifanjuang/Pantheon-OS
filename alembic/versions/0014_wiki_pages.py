"""Migration 0013 — wiki_pages (synthesis cache inspiré de llm-wiki)

Crée la table wiki_pages qui matérialise les décisions validées en
pages markdown navigables, réutilisables comme précédents lors du
scoring décisionnel (bonus « +5 déjà validé dans projets passés »).

Colonnes clés :
  - scope + slug    : identifiant humain unique par portée (projet|agence)
  - sujet_norm      : forme normalisée du titre pour lookup rapide
  - contenu_md      : markdown avec wikilinks [[slug]]
  - embedding       : vector(EMBEDDING_DIM) + index HNSW cosine
  - decision_id     : FK nullable vers project_decisions (promotion)
  - reuse_count     : incrémenté à chaque lookup de précédent

Revision ID: 0014
Revises: 0013
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from core.settings import settings

revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "wiki_pages",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "affaire_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("affaires.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("scope", sa.String(16), nullable=False, server_default="projet"),
        sa.Column("slug", sa.String(256), nullable=False),
        sa.Column("titre", sa.String(512), nullable=False),
        sa.Column("sujet_norm", sa.String(512), nullable=False),
        sa.Column("contenu_md", sa.Text, nullable=False),
        sa.Column(
            "tags",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("criticite", sa.String(2), nullable=True),
        sa.Column("score", sa.Integer, nullable=True),
        sa.Column(
            "decision_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("project_decisions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "source_run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("orchestra_runs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        # Colonne vector — placeholder Text remplacé par vector(DIM) plus bas
        sa.Column("embedding", sa.Text, nullable=True),
        sa.Column(
            "citations",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "validated_by",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("validated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "reuse_count",
            sa.Integer,
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("scope", "slug", name="uq_wiki_pages_scope_slug"),
    )

    op.create_index("ix_wiki_pages_affaire_id", "wiki_pages", ["affaire_id"])
    op.create_index("ix_wiki_pages_sujet_norm", "wiki_pages", ["sujet_norm"])
    op.create_index("ix_wiki_pages_scope", "wiki_pages", ["scope"])
    op.create_index("ix_wiki_pages_decision_id", "wiki_pages", ["decision_id"])

    # Conversion Text → vector(EMBEDDING_DIM) natif pgvector
    dim = settings.EMBEDDING_DIM
    op.execute(
        f"ALTER TABLE wiki_pages ALTER COLUMN embedding TYPE vector({dim}) USING NULL"
    )

    # Index HNSW cosine (pgvector ≥ 0.5)
    op.execute(
        "CREATE INDEX ix_wiki_pages_embedding_hnsw ON wiki_pages "
        "USING hnsw (embedding vector_cosine_ops) "
        "WITH (m = 16, ef_construction = 64)"
    )

    # Trigger updated_at (réutilise la fonction _set_updated_at créée en 0001)
    op.execute(
        """
        CREATE TRIGGER trg_wiki_pages_updated_at
        BEFORE UPDATE ON wiki_pages
        FOR EACH ROW EXECUTE FUNCTION _set_updated_at()
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_wiki_pages_updated_at ON wiki_pages")
    op.execute("DROP INDEX IF EXISTS ix_wiki_pages_embedding_hnsw")
    op.drop_index("ix_wiki_pages_decision_id", table_name="wiki_pages")
    op.drop_index("ix_wiki_pages_scope", table_name="wiki_pages")
    op.drop_index("ix_wiki_pages_sujet_norm", table_name="wiki_pages")
    op.drop_index("ix_wiki_pages_affaire_id", table_name="wiki_pages")
    op.drop_table("wiki_pages")
