"""Add agent_memory table

Revision ID: 0004
Revises: 0003
Create Date: 2026-04-02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "agent_memory",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("agent_name", sa.String(64), nullable=False),
        sa.Column("affaire_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("affaires.id", ondelete="CASCADE"), nullable=True),
        sa.Column("source_run_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("agent_runs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("lesson", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("ix_agent_memory_agent_affaire",
                    "agent_memory", ["agent_name", "affaire_id"])
    op.create_index("ix_agent_memory_created_at",
                    "agent_memory", ["created_at"])


def downgrade() -> None:
    op.drop_table("agent_memory")
