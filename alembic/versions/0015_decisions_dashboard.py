"""Migration 0015 — enrichissement project_decisions + project_tasks + project_observations

Enrichit project_decisions avec les colonnes dashboard (phase, sujet, lot,
agents_impliques, impact_cout, impact_delai, responsable, date_decision,
phase_revision).

Crée les tables :
  - project_tasks        (TABLE 2 — tâches liées à une décision)
  - project_observations (TABLE 3 — entrées terrain Argos)

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
    # ── Enrichissement project_decisions ────────────────────────────
    op.add_column(
        "project_decisions",
        sa.Column("sujet", sa.String(256), nullable=True),
    )
    op.add_column(
        "project_decisions",
        sa.Column("phase", sa.String(16), nullable=True),
    )
    op.add_column(
        "project_decisions",
        sa.Column("lot", sa.String(64), nullable=True),
    )
    op.add_column(
        "project_decisions",
        sa.Column(
            "agents_impliques",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )
    op.add_column(
        "project_decisions",
        sa.Column("impact_cout", sa.Numeric(12, 2), nullable=True),
    )
    op.add_column(
        "project_decisions",
        sa.Column("impact_delai", sa.Integer, nullable=True),
    )
    op.add_column(
        "project_decisions",
        sa.Column("responsable", sa.String(128), nullable=True),
    )
    op.add_column(
        "project_decisions",
        sa.Column("date_decision", sa.Date, nullable=True),
    )
    op.add_column(
        "project_decisions",
        sa.Column("phase_revision", sa.String(16), nullable=True),
    )

    op.create_index("ix_project_decisions_sujet", "project_decisions", ["sujet"])
    op.create_index("ix_project_decisions_lot", "project_decisions", ["lot"])
    op.create_index("ix_project_decisions_phase", "project_decisions", ["phase"])
    op.create_index("ix_project_decisions_statut", "project_decisions", ["statut"])
    op.create_index("ix_project_decisions_criticite", "project_decisions", ["criticite"])

    # ── project_tasks ──────────────────────────────────────────────
    op.create_table(
        "project_tasks",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "affaire_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("affaires.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column(
            "decision_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("project_decisions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("titre", sa.String(256), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("urgence", sa.Integer, nullable=False, server_default=sa.text("3")),
        sa.Column("statut", sa.String(20), nullable=False, server_default="ouvert"),
        sa.Column("responsable", sa.String(128), nullable=True),
        sa.Column("echeance", sa.Date, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_project_tasks_affaire_id", "project_tasks", ["affaire_id"])
    op.create_index("ix_project_tasks_decision_id", "project_tasks", ["decision_id"])
    op.create_index("ix_project_tasks_statut", "project_tasks", ["statut"])

    # Trigger updated_at
    op.execute(
        """
        CREATE TRIGGER trg_project_tasks_updated_at
        BEFORE UPDATE ON project_tasks
        FOR EACH ROW EXECUTE FUNCTION _set_updated_at()
        """
    )

    # ── project_observations ──────────────────────────────────────
    op.create_table(
        "project_observations",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "affaire_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("affaires.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column(
            "decision_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("project_decisions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("source", sa.String(16), nullable=False),
        sa.Column("contenu_brut", sa.Text, nullable=True),
        sa.Column("storage_key", sa.String(1024), nullable=True),
        sa.Column("analyse_argos", sa.Text, nullable=True),
        sa.Column("traitement", sa.String(20), nullable=False, server_default="a_traiter"),
        sa.Column(
            "auteur",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index(
        "ix_project_observations_affaire_id",
        "project_observations",
        ["affaire_id"],
    )
    op.create_index(
        "ix_project_observations_decision_id",
        "project_observations",
        ["decision_id"],
    )
    op.create_index(
        "ix_project_observations_traitement",
        "project_observations",
        ["traitement"],
    )


def downgrade() -> None:
    op.drop_table("project_observations")
    op.execute("DROP TRIGGER IF EXISTS trg_project_tasks_updated_at ON project_tasks")
    op.drop_table("project_tasks")

    op.drop_index("ix_project_decisions_criticite", table_name="project_decisions")
    op.drop_index("ix_project_decisions_statut", table_name="project_decisions")
    op.drop_index("ix_project_decisions_phase", table_name="project_decisions")
    op.drop_index("ix_project_decisions_lot", table_name="project_decisions")
    op.drop_index("ix_project_decisions_sujet", table_name="project_decisions")

    op.drop_column("project_decisions", "phase_revision")
    op.drop_column("project_decisions", "date_decision")
    op.drop_column("project_decisions", "responsable")
    op.drop_column("project_decisions", "impact_delai")
    op.drop_column("project_decisions", "impact_cout")
    op.drop_column("project_decisions", "agents_impliques")
    op.drop_column("project_decisions", "lot")
    op.drop_column("project_decisions", "phase")
    op.drop_column("project_decisions", "sujet")
