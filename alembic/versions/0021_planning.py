"""Migration 0021 — module planning

Crée les quatre tables du moteur de planification :

  planning_lots
    Lots de travaux (GEO, TCE, ELE, PLOM, CVC, ...) rattachés à une affaire.
    Portent l'entreprise titulaire, les dates prévues et le montant marché.

  planning_taches
    Tâches rattachées à un lot (optionnel).
    Champs dates prévues/réelles, durée nominale, avancement, statut.
    Flag `critique` mis à jour par compute_critical_path().

  planning_jalons
    Jalons contractuels/techniques/administratifs par affaire.
    Liés optionnellement à une tâche de fin.

  planning_liens
    Liens de dépendance inter-tâches : FS | SS | FF | SF + lag en jours.
    Forment le DAG exploité par le CPM.

Revision ID: 0021
Revises: 0020
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0021"
down_revision = "0020"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── planning_lots ────────────────────────────────────────────────
    op.create_table(
        "planning_lots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "affaire_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("affaires.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("code", sa.String(32), nullable=False),
        sa.Column("nom", sa.String(256), nullable=False),
        sa.Column("entreprise", sa.String(256), nullable=True),
        sa.Column("date_debut", sa.Date, nullable=True),
        sa.Column("date_fin", sa.Date, nullable=True),
        sa.Column("statut", sa.String(20), nullable=False, server_default="planifie"),
        sa.Column("montant_marche", sa.Numeric(12, 2), nullable=True),
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
    op.create_index("ix_planning_lots_affaire_id", "planning_lots", ["affaire_id"])

    # ── planning_taches ──────────────────────────────────────────────
    op.create_table(
        "planning_taches",
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
        sa.Column("titre", sa.String(256), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("responsable", sa.String(128), nullable=True),
        sa.Column("date_debut_prevue", sa.Date, nullable=True),
        sa.Column("date_fin_prevue", sa.Date, nullable=True),
        sa.Column("date_debut_reelle", sa.Date, nullable=True),
        sa.Column("date_fin_reelle", sa.Date, nullable=True),
        sa.Column("duree_jours", sa.Integer, nullable=True),
        sa.Column("avancement", sa.Integer, nullable=False, server_default="0"),
        sa.Column("statut", sa.String(20), nullable=False, server_default="planifiee"),
        sa.Column("critique", sa.Boolean, nullable=False, server_default="false"),
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
    op.create_index("ix_planning_taches_affaire_id", "planning_taches", ["affaire_id"])
    op.create_index("ix_planning_taches_lot_id", "planning_taches", ["lot_id"])
    op.create_index("ix_planning_taches_statut", "planning_taches", ["statut"])
    op.create_index("ix_planning_taches_critique", "planning_taches", ["critique"])

    # ── planning_jalons ──────────────────────────────────────────────
    op.create_table(
        "planning_jalons",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "affaire_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("affaires.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "tache_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("planning_taches.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("nom", sa.String(256), nullable=False),
        sa.Column("type", sa.String(32), nullable=False, server_default="technique"),
        sa.Column("date_cible", sa.Date, nullable=False),
        sa.Column("date_reelle", sa.Date, nullable=True),
        sa.Column("statut", sa.String(20), nullable=False, server_default="a_venir"),
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
    op.create_index("ix_planning_jalons_affaire_id", "planning_jalons", ["affaire_id"])
    op.create_index("ix_planning_jalons_date_cible", "planning_jalons", ["date_cible"])

    # ── planning_liens ───────────────────────────────────────────────
    op.create_table(
        "planning_liens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "predecesseur_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("planning_taches.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "successeur_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("planning_taches.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("type", sa.String(4), nullable=False, server_default="FS"),
        sa.Column("delai_jours", sa.Integer, nullable=False, server_default="0"),
    )
    op.create_index(
        "ix_planning_liens_predecesseur", "planning_liens", ["predecesseur_id"]
    )
    op.create_index(
        "ix_planning_liens_successeur", "planning_liens", ["successeur_id"]
    )


def downgrade() -> None:
    op.drop_table("planning_liens")
    op.drop_table("planning_jalons")
    op.drop_table("planning_taches")
    op.drop_table("planning_lots")
