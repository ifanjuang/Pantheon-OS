"""Migration 0012 — Traçabilité orchestra + agent_runs + mémoire temporelle

Ajoute les colonnes nécessaires pour exploiter en production les traces
multi-agents et séparer proprement les erreurs des résultats produits.

Enrichit aussi la mémoire des agents avec une dimension temporelle
(valid_until, superseded_by) et une catégorisation (category) inspirée
du pattern MemPalace, implémentée nativement dans PostgreSQL.

Tables impactées :
  - orchestra_runs
      + subtasks         JSONB  — décomposition Zeus persistée (id, pattern, agents, deps)
      + subtask_results  JSONB  — résultats par sous-tâche {task_id: {agent: result}}
      + veto_agent       VARCHAR(64)  — agent ayant émis un veto (themis|hephaistos|...)
      + veto_motif       TEXT         — extrait du motif du veto
      + error_message    TEXT         — séparé de final_answer (échecs distincts du contenu)
  - agent_runs
      + error_message    TEXT         — séparé de result (erreurs distinctes du contenu)
  - agent_memory
      + category         VARCHAR(64)  — catégorisation thématique (technique, planning, budget, contractuel)
      + valid_until      TIMESTAMPTZ  — NULL = toujours valide ; sinon date d'invalidation
      + superseded_by    UUID FK      — pointe vers la leçon qui remplace celle-ci

Tous les ajouts sont nullable ou ont un DEFAULT — aucune lecture existante n'est cassée.

Revision ID: 0012
Revises: 0011
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── orchestra_runs ──────────────────────────────────────────────
    op.add_column(
        "orchestra_runs",
        sa.Column(
            "subtasks",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column(
            "subtask_results",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("veto_agent", sa.String(64), nullable=True),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("veto_motif", sa.Text, nullable=True),
    )
    op.add_column(
        "orchestra_runs",
        sa.Column("error_message", sa.Text, nullable=True),
    )

    op.create_index(
        "ix_orchestra_runs_status",
        "orchestra_runs",
        ["status"],
    )
    op.create_index(
        "ix_orchestra_runs_veto_agent",
        "orchestra_runs",
        ["veto_agent"],
    )

    # ── agent_runs ──────────────────────────────────────────────────
    op.add_column(
        "agent_runs",
        sa.Column("error_message", sa.Text, nullable=True),
    )
    op.create_index(
        "ix_agent_runs_status",
        "agent_runs",
        ["status"],
    )

    # ── agent_memory — mémoire temporelle + catégorisation ──────────
    op.add_column(
        "agent_memory",
        sa.Column("category", sa.String(64), nullable=True),
    )
    op.add_column(
        "agent_memory",
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "agent_memory",
        sa.Column(
            "superseded_by",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("agent_memory.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_agent_memory_category",
        "agent_memory",
        ["category"],
    )
    op.create_index(
        "ix_agent_memory_valid_until",
        "agent_memory",
        ["valid_until"],
    )


def downgrade() -> None:
    op.drop_index("ix_agent_memory_valid_until", table_name="agent_memory")
    op.drop_index("ix_agent_memory_category", table_name="agent_memory")
    op.drop_column("agent_memory", "superseded_by")
    op.drop_column("agent_memory", "valid_until")
    op.drop_column("agent_memory", "category")

    op.drop_index("ix_agent_runs_status", table_name="agent_runs")
    op.drop_column("agent_runs", "error_message")

    op.drop_index("ix_orchestra_runs_veto_agent", table_name="orchestra_runs")
    op.drop_index("ix_orchestra_runs_status", table_name="orchestra_runs")
    op.drop_column("orchestra_runs", "error_message")
    op.drop_column("orchestra_runs", "veto_motif")
    op.drop_column("orchestra_runs", "veto_agent")
    op.drop_column("orchestra_runs", "subtask_results")
    op.drop_column("orchestra_runs", "subtasks")
