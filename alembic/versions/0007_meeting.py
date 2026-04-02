"""Add meeting tables (crs, actions, agendas)

Revision ID: 0007
Revises: 0006
Create Date: 2026-04-02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # meeting_crs
    op.create_table(
        "meeting_crs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("affaire_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("affaires.id", ondelete="CASCADE"), nullable=False),
        sa.Column("uploaded_by", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("titre", sa.String(256), nullable=False),
        sa.Column("date_reunion", sa.Date, nullable=True),
        sa.Column("participants", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("contenu_brut", sa.Text, nullable=True),
        sa.Column("synthese", sa.Text, nullable=True),
        sa.Column("analyse_status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("document_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("documents.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("ix_meeting_crs_affaire_id", "meeting_crs", ["affaire_id"])
    op.create_index("ix_meeting_crs_date_reunion", "meeting_crs", ["date_reunion"])

    # meeting_actions
    op.create_table(
        "meeting_actions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("affaire_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("affaires.id", ondelete="CASCADE"), nullable=False),
        sa.Column("cr_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("meeting_crs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("responsable", sa.String(128), nullable=True),
        sa.Column("echeance", sa.Date, nullable=True),
        sa.Column("priorite", sa.String(32), nullable=False, server_default="normale"),
        sa.Column("statut", sa.String(32), nullable=False, server_default="ouvert"),
        sa.Column("contexte", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("ix_meeting_actions_affaire_id", "meeting_actions", ["affaire_id"])
    op.create_index("ix_meeting_actions_cr_id", "meeting_actions", ["cr_id"])
    op.create_index("ix_meeting_actions_statut", "meeting_actions", ["statut"])
    op.create_index("ix_meeting_actions_echeance", "meeting_actions", ["echeance"])

    # meeting_agendas
    op.create_table(
        "meeting_agendas",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("affaire_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("affaires.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("titre", sa.String(256), nullable=False),
        sa.Column("date_prevue", sa.Date, nullable=True),
        sa.Column("items", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("notes_preparatoires", sa.Text, nullable=True),
        sa.Column("actions_incluses", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("ix_meeting_agendas_affaire_id", "meeting_agendas", ["affaire_id"])


def downgrade() -> None:
    op.drop_table("meeting_agendas")
    op.drop_table("meeting_actions")
    op.drop_table("meeting_crs")
