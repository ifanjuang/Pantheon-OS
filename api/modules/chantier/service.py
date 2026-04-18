"""
ChantierService — logique métier du module chantier.

CRUD : observations terrain, non-conformités.

Pipeline Argos :
  process_observation_analysis(db, obs_id)
    Construit l'instruction d'analyse, appelle run_agent("argos"),
    stocke le constat dans observation.analyse_argos.

Pipeline Héphaïstos :
  process_nc_qualification(db, nc_id)
    Appelle run_agent("hephaistos") sur la description + constat Argos,
    stocke le diagnostic dans nc.analyse_hephaistos.
    Positionne nc.arret_chantier=True si les mots-clés critiques sont détectés.
"""

from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.chantier.models import NonConformite, ObservationChantier

_ARRET_KEYWORDS = (
    "arrêt de chantier",
    "arret de chantier",
    "expertise structure",
    "risque effondrement",
    "danger structurel",
    "inspection du travail",
)


# ══════════════════════════════════════════════════════════════════════
# OBSERVATIONS
# ══════════════════════════════════════════════════════════════════════


async def create_observation(
    db: AsyncSession, affaire_id: UUID, auteur_id: UUID | None = None, **fields
) -> ObservationChantier:
    obs = ObservationChantier(affaire_id=affaire_id, auteur=auteur_id, **fields)
    db.add(obs)
    await db.flush()
    return obs


async def get_observation(db: AsyncSession, obs_id: UUID) -> ObservationChantier | None:
    return await db.get(ObservationChantier, obs_id)


async def list_observations(
    db: AsyncSession,
    affaire_id: UUID,
    source: str | None = None,
    statut: str | None = None,
    lot_id: UUID | None = None,
) -> list[ObservationChantier]:
    q = (
        select(ObservationChantier)
        .where(ObservationChantier.affaire_id == affaire_id)
        .order_by(ObservationChantier.date_constat.desc())
    )
    if source:
        q = q.where(ObservationChantier.source == source)
    if statut:
        q = q.where(ObservationChantier.statut == statut)
    if lot_id:
        q = q.where(ObservationChantier.lot_id == lot_id)
    result = await db.execute(q)
    return result.scalars().all()


async def update_observation(db: AsyncSession, obs: ObservationChantier, data: dict) -> ObservationChantier:
    for k, v in data.items():
        if v is not None:
            setattr(obs, k, v)
    await db.flush()
    return obs


async def delete_observation(db: AsyncSession, obs: ObservationChantier) -> None:
    await db.delete(obs)


# ══════════════════════════════════════════════════════════════════════
# PIPELINE ARGOS
# ══════════════════════════════════════════════════════════════════════


async def process_observation_analysis(db: AsyncSession, obs_id: UUID) -> None:
    """
    Appelé par le job ARQ `analyze_chantier_obs_job`.
    Lance l'agent Argos sur l'observation et stocke le constat.
    """
    from modules.agent.service import run_agent  # late import — évite circulaire

    obs = await get_observation(db, obs_id)
    if not obs or obs.statut == "analyse":
        return

    obs.statut = "en_cours"
    await db.flush()

    # Construire l'instruction Argos
    parts = [
        "Analyse cette observation de chantier et produis un constat objectif.",
        "",
    ]
    if obs.localisation:
        parts.append(f"Localisation : {obs.localisation}")
    if obs.entreprise:
        parts.append(f"Entreprise concernée : {obs.entreprise}")
    if obs.source == "photo" and obs.storage_key:
        parts.append(f"Photo disponible (clé MinIO) : {obs.storage_key}")
        parts.append("Décris précisément ce que tu observes : géométrie, matériaux, anomalies.")
    if obs.contenu_brut:
        parts.append(f"\nContenu brut :\n{obs.contenu_brut}")

    instruction = "\n".join(parts)

    run = await run_agent(
        db=db,
        instruction=instruction,
        affaire_id=obs.affaire_id,
        user_id=None,
        agent_name="argos",
        max_iterations=5,
    )

    obs.analyse_argos = run.result or ""
    obs.statut = "analyse"
    await db.flush()


# ══════════════════════════════════════════════════════════════════════
# NON-CONFORMITÉS
# ══════════════════════════════════════════════════════════════════════


async def create_nonconformite(db: AsyncSession, affaire_id: UUID, **fields) -> NonConformite:
    nc = NonConformite(affaire_id=affaire_id, **fields)
    # Positionner arret_chantier si gravite le demande
    if fields.get("gravite") == "arret_chantier":
        nc.arret_chantier = True
    db.add(nc)
    await db.flush()
    return nc


async def get_nonconformite(db: AsyncSession, nc_id: UUID) -> NonConformite | None:
    return await db.get(NonConformite, nc_id)


async def list_nonconformites(
    db: AsyncSession,
    affaire_id: UUID,
    gravite: str | None = None,
    statut: str | None = None,
    lot_id: UUID | None = None,
    ouvertes_seulement: bool = False,
) -> list[NonConformite]:
    q = (
        select(NonConformite)
        .where(NonConformite.affaire_id == affaire_id)
        .order_by(NonConformite.date_detection.desc())
    )
    if gravite:
        q = q.where(NonConformite.gravite == gravite)
    if statut:
        q = q.where(NonConformite.statut == statut)
    if lot_id:
        q = q.where(NonConformite.lot_id == lot_id)
    if ouvertes_seulement:
        q = q.where(NonConformite.statut.in_(("ouverte", "en_cours")))
    result = await db.execute(q)
    return result.scalars().all()


async def update_nonconformite(db: AsyncSession, nc: NonConformite, data: dict) -> NonConformite:
    for k, v in data.items():
        if v is not None:
            setattr(nc, k, v)
    # Synchroniser arret_chantier si gravite change
    if data.get("gravite") == "arret_chantier":
        nc.arret_chantier = True
    await db.flush()
    return nc


async def delete_nonconformite(db: AsyncSession, nc: NonConformite) -> None:
    await db.delete(nc)


# ══════════════════════════════════════════════════════════════════════
# PIPELINE HÉPHAÏSTOS
# ══════════════════════════════════════════════════════════════════════


async def process_nc_qualification(db: AsyncSession, nc_id: UUID) -> None:
    """
    Appelé par le job ARQ `qualify_nc_job`.
    Lance Héphaïstos pour qualifier la NC techniquement.
    Détecte automatiquement les mots-clés d'arrêt de chantier.
    """
    from modules.agent.service import run_agent  # late import

    nc = await get_nonconformite(db, nc_id)
    if not nc:
        return

    # Récupérer le constat Argos si disponible
    argos_context = ""
    if nc.observation_id:
        obs = await get_observation(db, nc.observation_id)
        if obs and obs.analyse_argos:
            argos_context = f"\n\nConstat Argos :\n{obs.analyse_argos}"

    instruction = (
        "Qualifie techniquement cette non-conformité de chantier.\n"
        "Identifie les DTU ou règles de l'art potentiellement violés, "
        "évalue la gravité réelle, propose les actions correctives concrètes.\n\n"
        f"Description : {nc.description}\n"
        f"Gravité déclarée : {nc.gravite}\n"
    )
    if nc.entreprise:
        instruction += f"Entreprise : {nc.entreprise}\n"
    instruction += argos_context

    run = await run_agent(
        db=db,
        instruction=instruction,
        affaire_id=nc.affaire_id,
        user_id=None,
        agent_name="hephaistos",
        max_iterations=6,
    )

    analyse = run.result or ""
    nc.analyse_hephaistos = analyse

    # Détection automatique d'arrêt de chantier
    analyse_lower = analyse.lower()
    if any(kw in analyse_lower for kw in _ARRET_KEYWORDS):
        nc.arret_chantier = True
        nc.gravite = "arret_chantier"

    await db.flush()


# ══════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════


async def get_dashboard(db: AsyncSession, affaire_id: UUID) -> dict:
    today = date.today()

    observations = await list_observations(db, affaire_id)
    ncs = await list_nonconformites(db, affaire_id)

    # Observations
    obs_a_analyser = sum(1 for o in observations if o.statut == "a_analyser")
    obs_analysees = sum(1 for o in observations if o.statut == "analyse")

    # NCs
    nc_ouvertes = sum(1 for n in ncs if n.statut == "ouverte")
    nc_en_cours = sum(1 for n in ncs if n.statut == "en_cours")
    nc_resolues = sum(1 for n in ncs if n.statut == "resolue")
    nc_critiques = sum(1 for n in ncs if n.gravite in ("critique", "arret_chantier") or n.arret_chantier)
    nc_en_retard = sum(
        1 for n in ncs if n.date_echeance and n.date_echeance < today and n.statut not in ("resolue", "contestee")
    )
    alerte_arret = any(n.arret_chantier and n.statut in ("ouverte", "en_cours") for n in ncs)

    return {
        "affaire_id": str(affaire_id),
        "total_observations": len(observations),
        "observations_a_analyser": obs_a_analyser,
        "observations_analysees": obs_analysees,
        "total_nc": len(ncs),
        "nc_ouvertes": nc_ouvertes,
        "nc_en_cours": nc_en_cours,
        "nc_resolues": nc_resolues,
        "nc_critiques": nc_critiques,
        "nc_en_retard": nc_en_retard,
        "alerte_arret_chantier": alerte_arret,
    }
