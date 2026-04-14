"""Migration 0018 — orchestra preprocessing + precheck columns

Ajoute la traçabilité du module preprocessing (Hermès++) :
  - preprocessed_input    : PreprocessedInput.model_dump() (JSONB)
  - precheck_verdict      : approved|trim|upgrade|clarification|blocked
  - precheck_reasoning    : justification du gate

Revision ID: 0018
Revises: 0017
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "0018"
down_revision = "0017"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "orchestra_runs",
        sa.Column("preprocessed_input", JSONB, nullable=True),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("precheck_verdict", sa.String(32), nullable=True),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("precheck_reasoning", sa.Text, nullable=True),
    )


def downgrade() -> None:
    op.drop_column("orchestra_runs", "precheck_reasoning")
    op.drop_column("orchestra_runs", "precheck_verdict")
    op.drop_column("orchestra_runs", "preprocessed_input")
