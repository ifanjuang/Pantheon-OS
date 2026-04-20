"""
Cockpit d'affaire — agrégation transversale de tous les dashboards modules.

Appels parallèles (asyncio.gather) aux services :
  - planning.get_health()
  - chantier.get_dashboard()
  - communications.get_dashboard()
  - finance.get_dashboard()
  - décisions D2/D3 ouvertes (requête directe)

Retourne un dict unifié + liste d'alertes triées par criticité :
  critical > warning > info
"""

import asyncio
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_cockpit(db: AsyncSession, affaire_id: UUID) -> dict:
    from modules.planning.service import get_health as _planning_health
    from modules.chantier.service import get_dashboard as _chantier_dashboard
    from modules.communications.service import get_dashboard as _comms_dashboard
    from modules.finance.service import get_dashboard as _finance_dashboard
    from modules.decisions.models import ProjectDecision

    # ── Appels parallèles ─────────────────────────────────────────────
    planning_res, chantier_res, comms_res, finance_res = await asyncio.gather(
        _planning_health(db, affaire_id),
        _chantier_dashboard(db, affaire_id),
        _comms_dashboard(db, affaire_id),
        _finance_dashboard(db, affaire_id),
        return_exceptions=True,
    )

    def _safe(r):
        return r if not isinstance(r, Exception) else None

    planning = _safe(planning_res)
    chantier = _safe(chantier_res)
    comms = _safe(comms_res)
    finance = _safe(finance_res)

    # ── Décisions D2/D3 ouvertes ──────────────────────────────────────
    d_result = await db.execute(
        select(func.count(ProjectDecision.id)).where(
            ProjectDecision.affaire_id == affaire_id,
            ProjectDecision.dette.in_(("D2", "D3")),
            ProjectDecision.statut == "ouvert",
        )
    )
    nb_decisions_critiques = d_result.scalar() or 0

    alertes = _build_alertes(planning, chantier, comms, finance, nb_decisions_critiques)

    return {
        "affaire_id": str(affaire_id),
        "planning": planning,
        "chantier": chantier,
        "communications": comms,
        "finance": finance,
        "decisions_critiques": nb_decisions_critiques,
        "alertes": alertes,
        "nb_alertes_critical": sum(1 for a in alertes if a["niveau"] == "critical"),
        "nb_alertes_warning": sum(1 for a in alertes if a["niveau"] == "warning"),
    }


def _build_alertes(
    planning: dict | None,
    chantier: dict | None,
    comms: dict | None,
    finance: dict | None,
    nb_decisions_critiques: int,
) -> list[dict]:
    alertes: list[dict] = []

    # ── Décisions ─────────────────────────────────────────────────────
    if nb_decisions_critiques > 0:
        alertes.append(
            {
                "module": "decisions",
                "niveau": "critical",
                "message": f"{nb_decisions_critiques} décision(s) D2/D3 ouverte(s) sans résolution",
                "count": nb_decisions_critiques,
            }
        )

    # ── Planning ──────────────────────────────────────────────────────
    if planning:
        if planning.get("jalons_manques", 0) > 0:
            alertes.append(
                {
                    "module": "planning",
                    "niveau": "critical",
                    "message": f"{planning['jalons_manques']} jalon(s) manqué(s)",
                    "count": planning["jalons_manques"],
                }
            )
        if planning.get("taches_en_retard", 0) > 0:
            alertes.append(
                {
                    "module": "planning",
                    "niveau": "warning",
                    "message": f"{planning['taches_en_retard']} tâche(s) en retard",
                    "count": planning["taches_en_retard"],
                }
            )
        if planning.get("taches_bloquees", 0) > 0:
            alertes.append(
                {
                    "module": "planning",
                    "niveau": "warning",
                    "message": f"{planning['taches_bloquees']} tâche(s) bloquée(s)",
                    "count": planning["taches_bloquees"],
                }
            )

    # ── Chantier ──────────────────────────────────────────────────────
    if chantier:
        if chantier.get("alerte_arret_chantier"):
            alertes.append(
                {
                    "module": "chantier",
                    "niveau": "critical",
                    "message": "Arrêt de chantier requis — NC critique ouverte",
                    "count": 1,
                }
            )
        if chantier.get("nc_en_retard", 0) > 0:
            alertes.append(
                {
                    "module": "chantier",
                    "niveau": "warning",
                    "message": f"{chantier['nc_en_retard']} NC en retard de correction",
                    "count": chantier["nc_en_retard"],
                }
            )
        if chantier.get("observations_a_analyser", 0) > 0:
            alertes.append(
                {
                    "module": "chantier",
                    "niveau": "info",
                    "message": f"{chantier['observations_a_analyser']} observation(s) à analyser",
                    "count": chantier["observations_a_analyser"],
                }
            )

    # ── Communications ────────────────────────────────────────────────
    if comms:
        if comms.get("mises_en_demeure", 0) > 0:
            alertes.append(
                {
                    "module": "communications",
                    "niveau": "critical",
                    "message": f"{comms['mises_en_demeure']} mise(s) en demeure reçue(s)",
                    "count": comms["mises_en_demeure"],
                }
            )
        if comms.get("en_retard", 0) > 0:
            alertes.append(
                {
                    "module": "communications",
                    "niveau": "warning",
                    "message": f"{comms['en_retard']} courrier(s) sans réponse hors délai",
                    "count": comms["en_retard"],
                }
            )
        if comms.get("en_attente_reponse", 0) > 0:
            alertes.append(
                {
                    "module": "communications",
                    "niveau": "info",
                    "message": f"{comms['en_attente_reponse']} courrier(s) en attente de réponse",
                    "count": comms["en_attente_reponse"],
                }
            )

    # ── Finance ───────────────────────────────────────────────────────
    if finance:
        derive = finance.get("derive_ht")
        if derive and derive > 0:
            alertes.append(
                {
                    "module": "finance",
                    "niveau": "warning",
                    "message": f"Dérive budgétaire +{derive:,.0f} € HT",
                    "count": 1,
                }
            )
        if finance.get("nb_avenants_en_attente", 0) > 0:
            alertes.append(
                {
                    "module": "finance",
                    "niveau": "info",
                    "message": f"{finance['nb_avenants_en_attente']} avenant(s) en attente de signature",
                    "count": finance["nb_avenants_en_attente"],
                }
            )
        if finance.get("nb_situations_en_attente", 0) > 0:
            alertes.append(
                {
                    "module": "finance",
                    "niveau": "info",
                    "message": f"{finance['nb_situations_en_attente']} situation(s) de travaux à valider",
                    "count": finance["nb_situations_en_attente"],
                }
            )

    # Tri : critical > warning > info
    _order = {"critical": 0, "warning": 1, "info": 2}
    return sorted(alertes, key=lambda a: _order[a["niveau"]])


async def get_alertes(db: AsyncSession, affaire_id: UUID) -> list[dict]:
    """Raccourci pour les cron jobs — retourne uniquement la liste d'alertes."""
    cockpit = await get_cockpit(db, affaire_id)
    return cockpit["alertes"]
