"""
CommunicationsService — registre des courriers et pipeline Iris.

process_draft_response(db, courrier_id)
  Construit le contexte complet du courrier entrant (objet, résumé,
  liens métier, historique de l'affaire) et appelle run_agent("iris")
  pour rédiger un brouillon de réponse. Stocke le draft dans
  courrier.draft_iris.
"""

from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.communications.models import Courrier


# ══════════════════════════════════════════════════════════════════════
# CRUD
# ══════════════════════════════════════════════════════════════════════


async def create_courrier(db: AsyncSession, affaire_id: UUID, auteur_id: UUID | None = None, **fields) -> Courrier:
    courrier = Courrier(affaire_id=affaire_id, auteur_id=auteur_id, **fields)
    db.add(courrier)
    await db.flush()
    return courrier


async def get_courrier(db: AsyncSession, courrier_id: UUID) -> Courrier | None:
    return await db.get(Courrier, courrier_id)


async def list_courriers(
    db: AsyncSession,
    affaire_id: UUID,
    sens: str | None = None,
    type_doc: str | None = None,
    statut: str | None = None,
    en_retard_seulement: bool = False,
) -> list[Courrier]:
    today = date.today()
    q = (
        select(Courrier)
        .where(Courrier.affaire_id == affaire_id)
        .order_by(Courrier.date_reception.desc().nulls_last(), Courrier.created_at.desc())
    )
    if sens:
        q = q.where(Courrier.sens == sens)
    if type_doc:
        q = q.where(Courrier.type_doc == type_doc)
    if statut:
        q = q.where(Courrier.statut == statut)
    if en_retard_seulement:
        q = q.where(
            Courrier.delai_reponse < today,
            Courrier.statut.in_(("recu", "en_attente_reponse")),
        )
    result = await db.execute(q)
    return result.scalars().all()


async def update_courrier(db: AsyncSession, courrier: Courrier, data: dict) -> Courrier:
    for k, v in data.items():
        if v is not None:
            setattr(courrier, k, v)
    await db.flush()
    return courrier


async def delete_courrier(db: AsyncSession, courrier: Courrier) -> None:
    await db.delete(courrier)


# ══════════════════════════════════════════════════════════════════════
# PIPELINE IRIS
# ══════════════════════════════════════════════════════════════════════


async def process_draft_response(db: AsyncSession, courrier_id: UUID) -> None:
    """
    Appelé par le job ARQ `draft_courrier_job`.
    Lance Iris pour rédiger un brouillon de réponse au courrier entrant.
    Stocke le résultat dans courrier.draft_iris.
    """
    from apps.agent.service import run_agent  # late import

    courrier = await get_courrier(db, courrier_id)
    if not courrier or courrier.draft_iris:
        return

    parts = [
        "Rédige un projet de réponse à ce courrier entrant.",
        f"Type de document : {courrier.type_doc}",
        f"Émetteur : {courrier.emetteur}",
        f"Destinataire : {courrier.destinataire}",
        f"Objet : {courrier.objet}",
    ]
    if courrier.reference:
        parts.append(f"Référence : {courrier.reference}")
    if courrier.date_reception:
        parts.append(f"Date de réception : {courrier.date_reception}")
    if courrier.delai_reponse:
        parts.append(f"Délai de réponse : {courrier.delai_reponse}")
    if courrier.resume:
        parts.append(f"\nRésumé du courrier :\n{courrier.resume}")
    if courrier.type_doc == "mise_en_demeure":
        parts.append(
            "\nATTENTION : mise en demeure — ton neutre, factuel, prudent. "
            "Ne pas admettre de faute. Accuser réception, indiquer l'instruction au juriste."
        )

    instruction = "\n".join(parts)

    run = await run_agent(
        db=db,
        instruction=instruction,
        affaire_id=courrier.affaire_id,
        user_id=None,
        agent_name="iris",
        max_iterations=4,
    )

    courrier.draft_iris = run.result or ""
    await db.flush()


# ══════════════════════════════════════════════════════════════════════
# PIPELINE RAG — INDEXATION COURRIERS
# ══════════════════════════════════════════════════════════════════════


async def ingest_courrier(db: AsyncSession, courrier_id: UUID) -> int:
    """
    Indexe le contenu textuel d'un courrier dans le RAG.

    Concatène objet + résumé + corps (si disponibles) et appelle
    RagService.ingest_text_direct() avec source_type="courrier".
    Idempotent : une réindexation supprime d'abord les chunks existants.

    Retourne le nombre de chunks créés (0 si aucun texte disponible).
    """
    from core.services.rag_service import RagService  # late import

    courrier = await get_courrier(db, courrier_id)
    if not courrier:
        return 0

    parts: list[str] = []
    if courrier.objet:
        parts.append(f"Objet : {courrier.objet}")
    if courrier.emetteur:
        parts.append(f"De : {courrier.emetteur}")
    if courrier.destinataire:
        parts.append(f"À : {courrier.destinataire}")
    if courrier.date_reception:
        parts.append(f"Date : {courrier.date_reception}")
    if courrier.resume:
        parts.append(f"\nRésumé :\n{courrier.resume}")

    if not parts:
        return 0

    text_content = "\n".join(parts)
    extra_meta = {
        "type_doc": courrier.type_doc,
        "sens": courrier.sens,
        "reference": courrier.reference or "",
    }

    return await RagService.ingest_text_direct(
        db=db,
        text_content=text_content,
        affaire_id=courrier.affaire_id,
        source_type="courrier",
        source_id=courrier_id,
        extra_meta=extra_meta,
    )


# ══════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════


async def get_dashboard(db: AsyncSession, affaire_id: UUID) -> dict:
    today = date.today()
    courriers = await list_courriers(db, affaire_id)

    entrants = sum(1 for c in courriers if c.sens == "entrant")
    sortants = sum(1 for c in courriers if c.sens == "sortant")
    en_attente = sum(1 for c in courriers if c.statut == "en_attente_reponse")
    en_retard = sum(
        1
        for c in courriers
        if c.delai_reponse and c.delai_reponse < today and c.statut in ("recu", "en_attente_reponse")
    )
    mises_en_demeure = sum(1 for c in courriers if c.type_doc == "mise_en_demeure")
    sans_suite = sum(1 for c in courriers if c.statut == "sans_suite")

    return {
        "affaire_id": str(affaire_id),
        "total": len(courriers),
        "entrants": entrants,
        "sortants": sortants,
        "en_attente_reponse": en_attente,
        "en_retard": en_retard,
        "mises_en_demeure": mises_en_demeure,
        "sans_suite": sans_suite,
    }
