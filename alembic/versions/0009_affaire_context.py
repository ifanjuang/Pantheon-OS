"""Add affaire context fields (typology, region, budget, phase, abf, zones)

Revision ID: 0009
Revises: 0008
Create Date: 2026-04-05
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("affaires", sa.Column("typology", sa.String(100), nullable=True))
    # Logement collectif / Maison individuelle / ERP / Industrie / Équipement public / Réhabilitation / Autre

    op.add_column("affaires", sa.Column("region", sa.String(100), nullable=True))

    op.add_column("affaires", sa.Column("budget_moa", sa.Numeric(12, 2), nullable=True))
    # Budget MOA total en € HT

    op.add_column("affaires", sa.Column("honoraires", sa.Numeric(10, 2), nullable=True))
    # Honoraires MOE contractuels en € HT

    op.add_column("affaires", sa.Column("date_debut", sa.Date, nullable=True))
    op.add_column("affaires", sa.Column("date_fin_prevue", sa.Date, nullable=True))

    op.add_column("affaires", sa.Column("phase_courante", sa.String(20), nullable=True))
    # ESQ | APS | APD | PRO | ACT | VISA | DET | AOR

    op.add_column(
        "affaires",
        sa.Column("abf", sa.Boolean, nullable=False, server_default="false"),
    )
    # Secteur Architecte des Bâtiments de France

    op.add_column(
        "affaires",
        sa.Column("zone_risque", postgresql.JSONB, nullable=True),
    )
    # {inondation: bool, sismique: str, archeo: bool, bruit: str, retrait_gonflement: str}


def downgrade() -> None:
    for col in ["typology", "region", "budget_moa", "honoraires",
                "date_debut", "date_fin_prevue", "phase_courante", "abf", "zone_risque"]:
        op.drop_column("affaires", col)
