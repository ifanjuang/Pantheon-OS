"""Add sources column to agent_runs

Revision ID: 0005
Revises: 0004
Create Date: 2026-04-02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "agent_runs",
        sa.Column("sources", postgresql.JSONB, nullable=False,
                  server_default="[]"),
    )


def downgrade() -> None:
    op.drop_column("agent_runs", "sources")
