"""Migration 0019 — guards module + veto traceability

Ajoute la traçabilité du module guards (M2) :
  - project_decisions.condition_levee : ce qu'il faut produire/valider
                                        pour lever un veto (Text)
  - project_decisions.reversible      : verdict reversibility_guard (Bool)
  - orchestra_runs.veto_severity      : bloquant | reserve | information
  - orchestra_runs.veto_condition_levee : conditions de levée du veto

Revision ID: 0019
Revises: 0018
"""
from alembic import op
import sqlalchemy as sa

revision = "0019"
down_revision = "0018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # project_decisions — enrichissements guards
    op.add_column(
        "project_decisions",
        sa.Column("condition_levee", sa.Text, nullable=True),
    )
    op.add_column(
        "project_decisions",
        sa.Column("reversible", sa.Boolean, nullable=True),
    )

    # orchestra_runs — traçabilité du structured_veto
    op.add_column(
        "orchestra_runs",
        sa.Column("veto_severity", sa.String(16), nullable=True),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("veto_condition_levee", sa.Text, nullable=True),
    )


def downgrade() -> None:
    op.drop_column("orchestra_runs", "veto_condition_levee")
    op.drop_column("orchestra_runs", "veto_severity")
    op.drop_column("project_decisions", "reversible")
    op.drop_column("project_decisions", "condition_levee")
