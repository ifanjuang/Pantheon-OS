"""Initial schema — users, affaires, affaire_permissions, documents, chunks

Revision ID: 0001
Revises:
Create Date: 2026-04-01

Tables créées :
  - users
  - affaires
  - affaire_permissions
  - documents
  - chunks  (avec colonne vector(768) et index HNSW cosine)
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── Extensions PostgreSQL ────────────────────────────────────
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    # ── users ────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text("uuid_generate_v4()")),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False, server_default=""),
        sa.Column("role", sa.String(32), nullable=False, server_default="lecteur"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # ── affaires ─────────────────────────────────────────────────
    op.create_table(
        "affaires",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text("uuid_generate_v4()")),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("nom", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("statut", sa.String(32), nullable=False, server_default="actif"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_affaires_code", "affaires", ["code"], unique=True)

    # ── affaire_permissions ──────────────────────────────────────
    op.create_table(
        "affaire_permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("affaire_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("affaires.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role_override", sa.String(32), nullable=True),
        sa.UniqueConstraint("user_id", "affaire_id", name="uq_affaire_permission"),
    )
    op.create_index("ix_affaire_permissions_user_id", "affaire_permissions", ["user_id"])
    op.create_index("ix_affaire_permissions_affaire_id", "affaire_permissions", ["affaire_id"])

    # ── documents ────────────────────────────────────────────────
    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text("uuid_generate_v4()")),
        sa.Column("affaire_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("affaires.id", ondelete="CASCADE"), nullable=True),
        sa.Column("nom", sa.String(512), nullable=False),
        sa.Column("couche", sa.String(32), nullable=False, server_default="projet"),
        sa.Column("type_doc", sa.String(64), nullable=False, server_default="pdf"),
        sa.Column("mime_type", sa.String(128), nullable=False, server_default="application/pdf"),
        sa.Column("taille_octets", sa.Integer, nullable=False, server_default="0"),
        sa.Column("storage_key", sa.String(1024), nullable=False),
        sa.Column("uploaded_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_documents_affaire_id", "documents", ["affaire_id"])

    # ── chunks ───────────────────────────────────────────────────
    op.create_table(
        "chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text("uuid_generate_v4()")),
        sa.Column("document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("affaire_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("affaires.id", ondelete="CASCADE"), nullable=True),
        sa.Column("contenu", sa.Text, nullable=False),
        sa.Column(
            "embedding",
            sa.Text,  # placeholder remplacé ci-dessous par le type vector natif
            nullable=True,
        ),
        sa.Column("chunk_index", sa.Integer, nullable=False, server_default="0"),
        sa.Column("meta", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_chunks_document_id", "chunks", ["document_id"])
    op.create_index("ix_chunks_affaire_id", "chunks", ["affaire_id"])

    # Convertir embedding en type vector(768) natif pgvector
    op.execute("ALTER TABLE chunks ALTER COLUMN embedding TYPE vector(768) USING NULL")

    # Index HNSW pour la similarité cosine (pgvector ≥ 0.5)
    op.execute(
        "CREATE INDEX ix_chunks_embedding_hnsw ON chunks "
        "USING hnsw (embedding vector_cosine_ops) "
        "WITH (m = 16, ef_construction = 64)"
    )

    # Trigger updated_at automatique sur users et affaires
    op.execute("""
        CREATE OR REPLACE FUNCTION _set_updated_at()
        RETURNS TRIGGER LANGUAGE plpgsql AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$
    """)
    for table in ("users", "affaires"):
        op.execute(f"""
            CREATE TRIGGER trg_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW EXECUTE FUNCTION _set_updated_at()
        """)


def downgrade() -> None:
    for table in ("affaires", "users"):
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table}")
    op.execute("DROP FUNCTION IF EXISTS _set_updated_at()")

    op.drop_table("chunks")
    op.drop_table("documents")
    op.drop_table("affaire_permissions")
    op.drop_table("affaires")
    op.drop_table("users")
