"""Migration 0024 — module finance

Crée deux tables de suivi financier des marchés de travaux :

  finance_avenants
    Modifications contractuelles au marché d'un lot.
    montant_ht peut être négatif (moins-value).
    Lié optionnellement à une décision (project_decisions).

  finance_situations
    Demandes de paiement périodiques par lot/entreprise.
    Cycle : soumise → en_revision → validee → payee.
    avancement_valide croisable avec planning_taches.avancement.

Note : le budget initial (affaire.budget_moa), les honoraires
(affaire.honoraires) et les montants de marché (planning_lots.montant_marche)
sont déjà dans leurs tables respectives — pas de duplication ici.

Revision ID: 0024
Revises: 0023
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0024"
down_revision = "0023"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── finance_avenants ─────────────────────────────────────────────
    op.create_table(
        "finance_avenants",
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
        sa.Column("numero", sa.String(64), nullable=False),
        sa.Column("objet", sa.String(512), nullable=False),
        sa.Column("montant_ht", sa.Numeric(12, 2), nullable=False),
        sa.Column("impact_delai_jours", sa.Integer, nullable=True),
        sa.Column("statut", sa.String(20), nullable=False, server_default="en_preparation"),
        sa.Column("date_soumission", sa.Date, nullable=True),
        sa.Column("date_acceptation", sa.Date, nullable=True),
        sa.Column("storage_key", sa.String(1024), nullable=True),
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
    op.create_index("ix_finance_avenants_affaire_id", "finance_avenants", ["affaire_id"])
    op.create_index("ix_finance_avenants_lot_id", "finance_avenants", ["lot_id"])
    op.create_index("ix_finance_avenants_statut", "finance_avenants", ["statut"])

    # ── finance_situations ───────────────────────────────────────────
    op.create_table(
        "finance_situations",
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
        sa.Column("entreprise", sa.String(256), nullable=False),
        sa.Column("numero", sa.Integer, nullable=False),
        sa.Column("periode_debut", sa.Date, nullable=False),
        sa.Column("periode_fin", sa.Date, nullable=False),
        sa.Column("montant_demande_ht", sa.Numeric(12, 2), nullable=False),
        sa.Column("montant_valide_ht", sa.Numeric(12, 2), nullable=True),
        sa.Column("avancement_declare", sa.Integer, nullable=False, server_default="0"),
        sa.Column("avancement_valide", sa.Integer, nullable=True),
        sa.Column("statut", sa.String(20), nullable=False, server_default="soumise"),
        sa.Column("date_soumission", sa.Date, nullable=False),
        sa.Column("date_validation", sa.Date, nullable=True),
        sa.Column("date_paiement", sa.Date, nullable=True),
        sa.Column("storage_key", sa.String(1024), nullable=True),
        sa.Column("remarques", sa.Text, nullable=True),
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
    op.create_index("ix_finance_situations_affaire_id", "finance_situations", ["affaire_id"])
    op.create_index("ix_finance_situations_lot_id", "finance_situations", ["lot_id"])
    op.create_index("ix_finance_situations_statut", "finance_situations", ["statut"])
    op.create_index("ix_finance_situations_entreprise", "finance_situations", ["entreprise"])


def downgrade() -> None:
    op.drop_table("finance_situations")
    op.drop_table("finance_avenants")
