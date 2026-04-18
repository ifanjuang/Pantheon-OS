"""Migration 0027 — Généralisation domaine : domain + domain_metadata sur affaires

Ajoute deux colonnes à la table affaires pour supporter n'importe quel domaine
professionnel (btp, droit, audit, conseil, medecine, it, …) :
  - domain       VARCHAR(64) NOT NULL DEFAULT 'btp'
  - domain_metadata JSONB     NULL — métadonnées libres domaine-spécifiques

Revision ID: 0027
Revises: 0026
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "0027"
down_revision = "0026"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "affaires",
        sa.Column(
            "domain",
            sa.String(64),
            nullable=False,
            server_default="btp",
        ),
    )
    op.add_column(
        "affaires",
        sa.Column("domain_metadata", JSONB, nullable=True),
    )


def downgrade() -> None:
    op.drop_column("affaires", "domain_metadata")
    op.drop_column("affaires", "domain")
