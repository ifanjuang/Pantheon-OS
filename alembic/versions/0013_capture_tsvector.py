"""Migration 0013 — capture_sessions + chunks tsvector

Tables créées :
  - capture_sessions : sessions de capture vocale NoobScribe

Modifications :
  - chunks : ajout colonne tsv (tsvector) avec GIN index + trigger auto-update
    Optimise les recherches FTS (évite le LATERAL to_tsvector à chaque requête)

Revision ID: 0013
Revises: 0012
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def upgrade():
    # ── 1. Table capture_sessions ─────────────────────────────────
    op.create_table(
        "capture_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column("affaire_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("affaires.id", ondelete="CASCADE"), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("audio_key", sa.String(1024), nullable=False),
        sa.Column("duration_seconds", sa.Integer, nullable=True),
        sa.Column("transcription", sa.Text, nullable=True),
        sa.Column("structured_output", postgresql.JSONB, nullable=True),
        sa.Column("agent_run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("agent_runs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_capture_sessions_affaire_id", "capture_sessions", ["affaire_id"])
    op.create_index("ix_capture_sessions_status", "capture_sessions", ["status"])

    # ── 2. Colonne tsv (tsvector) sur chunks ──────────────────────
    op.add_column("chunks", sa.Column("tsv", postgresql.TSVECTOR, nullable=True))
    op.create_index("ix_chunks_tsv", "chunks", ["tsv"], postgresql_using="gin")

    # Backfill des chunks existants
    op.execute("UPDATE chunks SET tsv = to_tsvector('french', contenu) WHERE tsv IS NULL")

    # Trigger function pour mise à jour automatique
    op.execute("""
        CREATE OR REPLACE FUNCTION chunks_tsv_update() RETURNS trigger AS $$
        BEGIN
          NEW.tsv := to_tsvector('french', COALESCE(NEW.contenu, ''));
          RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trg_chunks_tsv_update
          BEFORE INSERT OR UPDATE OF contenu ON chunks
          FOR EACH ROW EXECUTE FUNCTION chunks_tsv_update();
    """)


def downgrade():
    # ── Trigger + function ────────────────────────────────────────
    op.execute("DROP TRIGGER IF EXISTS trg_chunks_tsv_update ON chunks")
    op.execute("DROP FUNCTION IF EXISTS chunks_tsv_update()")

    # ── Colonne tsv + index ───────────────────────────────────────
    op.drop_index("ix_chunks_tsv", table_name="chunks")
    op.drop_column("chunks", "tsv")

    # ── Table capture_sessions ────────────────────────────────────
    op.drop_index("ix_capture_sessions_status", table_name="capture_sessions")
    op.drop_index("ix_capture_sessions_affaire_id", table_name="capture_sessions")
    op.drop_table("capture_sessions")
