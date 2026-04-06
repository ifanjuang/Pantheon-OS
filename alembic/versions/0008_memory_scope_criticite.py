"""Add memory scope + orchestra criticite + project_decisions table

Revision ID: 0008
Revises: 0007
Create Date: 2026-04-05
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Scope sur agent_memory (agence | projet)
    op.add_column(
        "agent_memory",
        sa.Column("scope", sa.String(20), nullable=False, server_default="agence"),
    )
    op.create_index("ix_agent_memory_scope", "agent_memory", ["scope"])

    # 2. Criticité sur orchestra_runs (C1-C5)
    op.add_column(
        "orchestra_runs",
        sa.Column("criticite", sa.String(2), nullable=False, server_default="C2"),
    )

    # 3. Table project_decisions (dette décisionnelle)
    op.create_table(
        "project_decisions",
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
            index=True,
        ),
        sa.Column(
            "run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("orchestra_runs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("objet", sa.Text, nullable=False),
        sa.Column("contexte", sa.Text, nullable=True),
        sa.Column("constat", sa.Text, nullable=True),
        sa.Column("analyse", sa.Text, nullable=True),
        sa.Column("impacts", sa.Text, nullable=True),
        sa.Column("options", postgresql.JSONB, nullable=True),
        # [{label, description, risque}]
        sa.Column("criticite", sa.String(2), nullable=False, server_default="C2"),
        sa.Column("dette", sa.String(2), nullable=False, server_default="D0"),
        # D0=résolu | D1=suspendu faible urgence | D2=bloquant | D3=critique en retard
        sa.Column("statut", sa.String(20), nullable=False, server_default="ouvert"),
        # ouvert | validé | suspendu | caduc
        sa.Column("agent_source", sa.String(50), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_project_decisions_affaire_id", "project_decisions", ["affaire_id"])
    op.create_index("ix_project_decisions_dette", "project_decisions", ["dette"])


def downgrade() -> None:
    op.drop_table("project_decisions")
    op.drop_column("orchestra_runs", "criticite")
    op.drop_index("ix_agent_memory_scope", table_name="agent_memory")
    op.drop_column("agent_memory", "scope")
