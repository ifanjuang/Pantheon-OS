"""Migration 0020 — classification ERP sur les affaires

Ajoute sur la table `affaires` :
  - erp_type      : type d'établissement recevant du public
                    (J, L, M, N, O, P, R, S, T, U, V, W, X, Y,
                     PA, CTS, SG, OA, GA, EF, REF)
                    NULL si l'affaire n'est pas un ERP
  - erp_categorie : catégorie ERP selon l'effectif du public
                    1 (>1500) | 2 (701-1500) | 3 (301-700)
                    | 4 (≤300) | 5 (seuil réduit)
                    NULL si l'affaire n'est pas un ERP

Revision ID: 0020
Revises: 0019
"""
from alembic import op
import sqlalchemy as sa

revision = "0020"
down_revision = "0019"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "affaires",
        sa.Column("erp_type", sa.String(10), nullable=True),
    )
    op.add_column(
        "affaires",
        sa.Column("erp_categorie", sa.String(2), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("affaires", "erp_categorie")
    op.drop_column("affaires", "erp_type")
