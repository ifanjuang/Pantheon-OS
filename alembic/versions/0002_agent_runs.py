"""Add agent_runs table

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "agent_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("affaire_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("affaires.id", ondelete="SET NULL"), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("instruction", sa.Text, nullable=False),
        sa.Column("result", sa.Text, nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="running"),
        sa.Column("steps", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("iterations", sa.Integer, nullable=False, server_default="0"),
        sa.Column("duration_ms", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("ix_agent_runs_affaire_id", "agent_runs", ["affaire_id"])
    op.create_index("ix_agent_runs_created_at", "agent_runs", ["created_at"])


def downgrade() -> None:
    op.drop_table("agent_runs")
