"""
FinanceService — suivi financier des marchés de travaux.

get_dashboard() agrège :
  - affaire.budget_moa / honoraires
  - planning_lots.montant_marche (base contractuelle par lot)
  - finance_avenants (modifications contractuelles)
  - finance_situations (réalisé déclaré et validé)

Toutes les valeurs monétaires sont en € HT.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.finance.models import Avenant, SituationTravaux


# ══════════════════════════════════════════════════════════════════════
# AVENANTS
# ══════════════════════════════════════════════════════════════════════


async def create_avenant(db: AsyncSession, affaire_id: UUID, **fields) -> Avenant:
    av = Avenant(affaire_id=affaire_id, **fields)
    db.add(av)
    await db.flush()
    return av


async def get_avenant(db: AsyncSession, av_id: UUID) -> Avenant | None:
    return await db.get(Avenant, av_id)


async def list_avenants(
    db: AsyncSession,
    affaire_id: UUID,
    lot_id: UUID | None = None,
    statut: str | None = None,
) -> list[Avenant]:
    q = select(Avenant).where(Avenant.affaire_id == affaire_id).order_by(Avenant.numero)
    if lot_id:
        q = q.where(Avenant.lot_id == lot_id)
    if statut:
        q = q.where(Avenant.statut == statut)
    result = await db.execute(q)
    return result.scalars().all()


async def update_avenant(db: AsyncSession, av: Avenant, data: dict) -> Avenant:
    for k, v in data.items():
        if v is not None:
            setattr(av, k, v)
    await db.flush()
    return av


async def delete_avenant(db: AsyncSession, av: Avenant) -> None:
    await db.delete(av)


# ══════════════════════════════════════════════════════════════════════
# SITUATIONS DE TRAVAUX
# ══════════════════════════════════════════════════════════════════════


async def create_situation(db: AsyncSession, affaire_id: UUID, **fields) -> SituationTravaux:
    sit = SituationTravaux(affaire_id=affaire_id, **fields)
    db.add(sit)
    await db.flush()
    return sit


async def get_situation(db: AsyncSession, sit_id: UUID) -> SituationTravaux | None:
    return await db.get(SituationTravaux, sit_id)


async def list_situations(
    db: AsyncSession,
    affaire_id: UUID,
    lot_id: UUID | None = None,
    statut: str | None = None,
    entreprise: str | None = None,
) -> list[SituationTravaux]:
    q = (
        select(SituationTravaux)
        .where(SituationTravaux.affaire_id == affaire_id)
        .order_by(SituationTravaux.periode_fin.desc())
    )
    if lot_id:
        q = q.where(SituationTravaux.lot_id == lot_id)
    if statut:
        q = q.where(SituationTravaux.statut == statut)
    if entreprise:
        q = q.where(SituationTravaux.entreprise == entreprise)
    result = await db.execute(q)
    return result.scalars().all()


async def update_situation(db: AsyncSession, sit: SituationTravaux, data: dict) -> SituationTravaux:
    for k, v in data.items():
        if v is not None:
            setattr(sit, k, v)
    await db.flush()
    return sit


async def delete_situation(db: AsyncSession, sit: SituationTravaux) -> None:
    await db.delete(sit)


# ══════════════════════════════════════════════════════════════════════
# DASHBOARD FINANCIER
# ══════════════════════════════════════════════════════════════════════


async def get_dashboard(db: AsyncSession, affaire_id: UUID) -> dict:
    """
    Agrège les données financières de l'affaire :
    base contractuelle (lots) + avenants + situations.
    """
    # Importer les modèles externes ici pour éviter les circulaires
    from apps.affaires.models import Affaire
    from apps.planning.models import Lot

    affaire = await db.get(Affaire, affaire_id)
    budget_moa = float(affaire.budget_moa) if affaire and affaire.budget_moa else None
    honoraires = float(affaire.honoraires) if affaire and affaire.honoraires else None

    # Base contractuelle : somme des montants de marché des lots
    lots_result = await db.execute(select(Lot).where(Lot.affaire_id == affaire_id))
    lots = lots_result.scalars().all()
    montant_marches_initial = sum(float(lot.montant_marche) for lot in lots if lot.montant_marche)

    # Avenants
    avenants = await list_avenants(db, affaire_id)
    avenants_acceptes = sum(float(a.montant_ht) for a in avenants if a.statut == "accepte")
    avenants_en_attente = sum(float(a.montant_ht) for a in avenants if a.statut in ("soumis", "en_preparation"))
    nb_avenants_en_attente = sum(1 for a in avenants if a.statut in ("soumis", "en_preparation"))

    montant_contractuel = montant_marches_initial + avenants_acceptes

    # Situations
    situations = await list_situations(db, affaire_id)
    montant_reclame = sum(
        float(s.montant_demande_ht) for s in situations if s.statut in ("soumise", "en_revision", "validee", "payee")
    )
    montant_valide = sum(
        float(s.montant_valide_ht) for s in situations if s.statut in ("validee", "payee") and s.montant_valide_ht
    )
    montant_paye = sum(float(s.montant_valide_ht) for s in situations if s.statut == "payee" and s.montant_valide_ht)
    nb_situations_en_attente = sum(1 for s in situations if s.statut in ("soumise", "en_revision"))

    # Ratios
    taux_engagement = round(montant_contractuel / budget_moa * 100, 1) if budget_moa and budget_moa > 0 else None
    taux_realisation = round(montant_valide / montant_contractuel * 100, 1) if montant_contractuel > 0 else None
    derive = round(montant_contractuel - budget_moa, 2) if budget_moa is not None else None

    return {
        "affaire_id": str(affaire_id),
        "budget_moa": budget_moa,
        "honoraires_moe": honoraires,
        "montant_marches_initial": round(montant_marches_initial, 2),
        "avenants_acceptes_ht": round(avenants_acceptes, 2),
        "avenants_en_attente_ht": round(avenants_en_attente, 2),
        "nb_avenants_en_attente": nb_avenants_en_attente,
        "montant_contractuel_ht": round(montant_contractuel, 2),
        "montant_reclame_ht": round(montant_reclame, 2),
        "montant_valide_ht": round(montant_valide, 2),
        "montant_paye_ht": round(montant_paye, 2),
        "nb_situations_en_attente": nb_situations_en_attente,
        "taux_engagement": taux_engagement,
        "taux_realisation": taux_realisation,
        "derive_ht": derive,
    }
