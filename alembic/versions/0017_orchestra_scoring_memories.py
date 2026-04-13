"""Migration 0017 — orchestra_runs scoring + memories columns

Ajoute les colonnes de traçabilité pour les nœuds score_decision et
write_memories du graphe Zeus :
  - score_id, score_verdict, score_total  (scoring décisionnel)
  - memories_written, wiki_page_id        (mémoires écrites)

Revision ID: 0017
Revises: 0016
"""
from alembic import op
import sqlalchemy as sa

revision = "0017"
down_revision = "0016"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "orchestra_runs",
        sa.Column("score_id", sa.String(64), nullable=True),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("score_verdict", sa.String(16), nullable=True),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("score_total", sa.Integer, nullable=True),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column(
            "memories_written",
            sa.Integer,
            nullable=False,
            server_default=sa.text("0"),
        ),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("wiki_page_id", sa.String(64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("orchestra_runs", "wiki_page_id")
    op.drop_column("orchestra_runs", "memories_written")
    op.drop_column("orchestra_runs", "score_total")
    op.drop_column("orchestra_runs", "score_verdict")
    op.drop_column("orchestra_runs", "score_id")
