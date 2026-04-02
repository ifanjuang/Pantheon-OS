"""Add orchestra_runs table

Revision ID: 0003
Revises: 0002
Create Date: 2026-04-02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "orchestra_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("affaire_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("affaires.id", ondelete="SET NULL"), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("instruction", sa.Text, nullable=False),
        sa.Column("initial_agents", postgresql.JSONB, nullable=False, server_default="[]"),
        # Phase 1
        sa.Column("agent_plans", postgresql.JSONB, nullable=False, server_default="{}"),
        # Phase 2
        sa.Column("zeus_reasoning", sa.Text, nullable=True),
        sa.Column("assignments", postgresql.JSONB, nullable=False, server_default="[]"),
        # Phase 3
        sa.Column("agent_results", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("agent_run_ids", postgresql.JSONB, nullable=False, server_default="[]"),
        # Phase 4
        sa.Column("final_answer", sa.Text, nullable=True),
        sa.Column("synthesis_agent", sa.String(64), nullable=True),
        # Meta
        sa.Column("status", sa.String(32), nullable=False, server_default="running"),
        sa.Column("duration_ms", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("ix_orchestra_runs_affaire_id", "orchestra_runs", ["affaire_id"])
    op.create_index("ix_orchestra_runs_created_at", "orchestra_runs", ["created_at"])


def downgrade() -> None:
    op.drop_table("orchestra_runs")
