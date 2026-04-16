"""Migration 0022 — module chantier

Crée les deux tables du module chantier :

  chantier_observations
    Entrées terrain brutes (photo, voix, note, mail) avec localisation,
    entreprise, constat Argos.

  chantier_nonconformites
    Non-conformités et actions correctives liées à une observation,
    un lot, une décision. Inclut le diagnostic Héphaïstos et le flag
    arret_chantier.

Revision ID: 0022
Revises: 0021
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0022"
down_revision = "0021"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── chantier_observations ────────────────────────────────────────
    op.create_table(
        "chantier_observations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "affaire_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("affaires.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "lot_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("planning_lots.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "auteur",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("source", sa.String(16), nullable=False),
        sa.Column("contenu_brut", sa.Text, nullable=True),
        sa.Column("storage_key", sa.String(1024), nullable=True),
        sa.Column("localisation", sa.String(512), nullable=True),
        sa.Column("entreprise", sa.String(256), nullable=True),
        sa.Column("date_constat", sa.Date, nullable=False),
        sa.Column("analyse_argos", sa.Text, nullable=True),
        sa.Column("statut", sa.String(20), nullable=False, server_default="a_analyser"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_chantier_obs_affaire_id", "chantier_observations", ["affaire_id"])
    op.create_index("ix_chantier_obs_lot_id", "chantier_observations", ["lot_id"])
    op.create_index("ix_chantier_obs_statut", "chantier_observations", ["statut"])
    op.create_index("ix_chantier_obs_date", "chantier_observations", ["date_constat"])

    # ── chantier_nonconformites ──────────────────────────────────────
    op.create_table(
        "chantier_nonconformites",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "affaire_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("affaires.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "observation_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("chantier_observations.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "lot_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("planning_lots.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "decision_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("project_decisions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("entreprise", sa.String(256), nullable=True),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("gravite", sa.String(20), nullable=False, server_default="mineure"),
        sa.Column("date_detection", sa.Date, nullable=False),
        sa.Column("date_echeance", sa.Date, nullable=True),
        sa.Column("date_resolution", sa.Date, nullable=True),
        sa.Column("statut", sa.String(20), nullable=False, server_default="ouverte"),
        sa.Column("responsable", sa.String(128), nullable=True),
        sa.Column("action_requise", sa.Text, nullable=True),
        sa.Column("analyse_hephaistos", sa.Text, nullable=True),
        sa.Column("arret_chantier", sa.Boolean, nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_chantier_nc_affaire_id", "chantier_nonconformites", ["affaire_id"])
    op.create_index("ix_chantier_nc_observation_id", "chantier_nonconformites", ["observation_id"])
    op.create_index("ix_chantier_nc_lot_id", "chantier_nonconformites", ["lot_id"])
    op.create_index("ix_chantier_nc_gravite", "chantier_nonconformites", ["gravite"])
    op.create_index("ix_chantier_nc_statut", "chantier_nonconformites", ["statut"])
    op.create_index("ix_chantier_nc_arret", "chantier_nonconformites", ["arret_chantier"])


def downgrade() -> None:
    op.drop_table("chantier_nonconformites")
    op.drop_table("chantier_observations")
