"""Migration 0023 — module communications

Crée la table `communications_courriers` — registre probatoire des
courriers entrants et sortants d'un projet MOE.

Champs clés :
  - sens          : entrant | sortant
  - type_doc      : courrier | email | lr | mise_en_demeure | bc | devis | pv | cr | autre
  - reference     : numéro de référence libre
  - emetteur/destinataire
  - objet / resume / storage_key (MinIO)
  - dates (emission, reception, delai_reponse, reponse_effective)
  - statut        : recu | en_attente_reponse | traite | sans_suite | archive
  - liens métier  : lot_id, decision_id, observation_id
  - reponse_id    : auto-référence (courrier sortant qui répond à l'entrant)
  - draft_iris    : brouillon Iris (rempli par ARQ)

Revision ID: 0023
Revises: 0022
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0023"
down_revision = "0022"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "communications_courriers",
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
            "decision_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("project_decisions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "observation_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("chantier_observations.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "reponse_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("communications_courriers.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "auteur_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("sens", sa.String(16), nullable=False),
        sa.Column("type_doc", sa.String(32), nullable=False, server_default="courrier"),
        sa.Column("reference", sa.String(128), nullable=True),
        sa.Column("emetteur", sa.String(256), nullable=False),
        sa.Column("destinataire", sa.String(256), nullable=False),
        sa.Column("objet", sa.String(512), nullable=False),
        sa.Column("resume", sa.Text, nullable=True),
        sa.Column("storage_key", sa.String(1024), nullable=True),
        sa.Column("date_emission", sa.Date, nullable=True),
        sa.Column("date_reception", sa.Date, nullable=True),
        sa.Column("delai_reponse", sa.Date, nullable=True),
        sa.Column("date_reponse_effective", sa.Date, nullable=True),
        sa.Column("statut", sa.String(32), nullable=False, server_default="recu"),
        sa.Column("draft_iris", sa.Text, nullable=True),
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
    op.create_index("ix_comm_courriers_affaire_id", "communications_courriers", ["affaire_id"])
    op.create_index("ix_comm_courriers_sens", "communications_courriers", ["sens"])
    op.create_index("ix_comm_courriers_statut", "communications_courriers", ["statut"])
    op.create_index("ix_comm_courriers_type_doc", "communications_courriers", ["type_doc"])
    op.create_index("ix_comm_courriers_delai", "communications_courriers", ["delai_reponse"])


def downgrade() -> None:
    op.drop_table("communications_courriers")
