"""Add HITL fields to orchestra_runs

Revision ID: 0006
Revises: 0005
Create Date: 2026-04-02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("orchestra_runs", sa.Column(
        "hitl_enabled", sa.Boolean, nullable=False, server_default="false"
    ))
    op.add_column("orchestra_runs", sa.Column(
        "hitl_payload", postgresql.JSONB, nullable=True
    ))
    op.add_column("orchestra_runs", sa.Column(
        "checkpoint_thread_id", sa.String(64), nullable=True
    ))


def downgrade() -> None:
    op.drop_column("orchestra_runs", "checkpoint_thread_id")
    op.drop_column("orchestra_runs", "hitl_payload")
    op.drop_column("orchestra_runs", "hitl_enabled")
