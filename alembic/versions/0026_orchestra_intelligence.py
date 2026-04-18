"""Migration 0026 — Orchestra intelligence : score global run, supervision HERA, fallback

6 améliorations architecturales :
  1. Score multi-critères pour TOUS les runs (run_score JSONB)
  2. Fallback intelligent 3 niveaux (fallback_level)
  3. Activation conditionnelle agents — tracé via AGENT_TRIGGERS (logique applicative)
  4. Supervision HERA — cohérence globale (hera_verdict + hera_feedback)
  5. Mémoire des erreurs — via category="erreur" dans agent_memory (logique applicative)
  6. Limites cognitives — via COGNITIVE_LIMITS (logique applicative)

Seules les colonnes DB sont ajoutées ici. Les améliorations purement applicatives
(3, 5, 6) sont dans les modules Python correspondants.

Revision ID: 0026
Revises: 0025
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "0026"
down_revision = "0025"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "orchestra_runs",
        sa.Column("run_score", JSONB, nullable=True, comment="Score multi-critères {quality,coherence,confidence,risk}"),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("hera_verdict", sa.String(16), nullable=True, comment="aligned | misaligned | degraded"),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("hera_feedback", sa.Text, nullable=True, comment="Feedback HERA sur la cohérence"),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("fallback_level", sa.Integer, nullable=False, server_default="0",
                  comment="0=none | 1=simplified | 2=strategy_changed | 3=degraded"),
    )


def downgrade() -> None:
    op.drop_column("orchestra_runs", "fallback_level")
    op.drop_column("orchestra_runs", "hera_feedback")
    op.drop_column("orchestra_runs", "hera_verdict")
    op.drop_column("orchestra_runs", "run_score")
