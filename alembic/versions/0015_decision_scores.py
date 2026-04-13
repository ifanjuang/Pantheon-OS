"""Migration 0014 — decision_scores (scoring décisionnel 100 pts)

Crée la table decision_scores qui matérialise le scoring sur 5 axes
(technique/contractuel/planning/cohérence/logique) avec bonus/malus.

Une ligne = un calcul, l'historique est conservé. Le score actif d'une
décision est le plus récent pour decision_id donné.

Revision ID: 0015
Revises: 0014
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0015"
down_revision = "0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "decision_scores",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "decision_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("project_decisions.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column(
            "affaire_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("affaires.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("sujet", sa.String(512), nullable=False),
        sa.Column(
            "axes",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "total_raw",
            sa.Integer,
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "bonus_malus",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "total_final",
            sa.Integer,
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "verdict",
            sa.String(16),
            nullable=False,
            server_default="fragile",
        ),
        sa.Column(
            "certitude",
            sa.Float,
            nullable=False,
            server_default=sa.text("1.0"),
        ),
        sa.Column("dette_snapshot", sa.String(2), nullable=True),
        sa.Column(
            "mode",
            sa.String(16),
            nullable=False,
            server_default="manuel",
        ),
        sa.Column(
            "computed_by",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "computed_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_index(
        "ix_decision_scores_decision_id", "decision_scores", ["decision_id"]
    )
    op.create_index(
        "ix_decision_scores_affaire_id", "decision_scores", ["affaire_id"]
    )
    op.create_index(
        "ix_decision_scores_verdict", "decision_scores", ["verdict"]
    )
    # Index composite pour "dernier score d'une décision"
    op.execute(
        "CREATE INDEX ix_decision_scores_decision_computed "
        "ON decision_scores (decision_id, computed_at DESC)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_decision_scores_decision_computed")
    op.drop_index("ix_decision_scores_verdict", table_name="decision_scores")
    op.drop_index("ix_decision_scores_affaire_id", table_name="decision_scores")
    op.drop_index("ix_decision_scores_decision_id", table_name="decision_scores")
    op.drop_table("decision_scores")
