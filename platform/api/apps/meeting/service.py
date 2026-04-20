"""
MeetingService — analyse de CR et génération d'ordres du jour.

Flux CR :
  1. Texte brut ou fichier uploadé → MeetingCR créé (status=pending)
  2. Hermès analyse → JSON structuré {actions, participants, synthèse}
  3. MeetingAction créées en masse depuis les actions extraites
  4. MeetingCR mis à jour (status=completed, synthèse)

Flux Agenda :
  1. Athéna reçoit le contexte projet + actions ouvertes + derniers runs agents
  2. Génère un ordre du jour structuré (JSON)
  3. MeetingAgenda persisté
"""

import json
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.llm_service import LlmService
from core.settings import settings
from apps.meeting.models import MeetingAction, MeetingAgenda, MeetingCR

log = get_logger("meeting.service")

# ── Prompts ──────────────────────────────────────────────────────────────────

_CR_ANALYSIS_PROMPT = """\
Tu es Hermès, assistant MOE spécialisé dans l'analyse de comptes rendus de réunion.

Analyse ce compte rendu et extrais toutes les actions décidées.

## Compte rendu
{contenu}

## Instructions
- Extrais TOUTES les actions, même implicites ("il a été convenu que...", "X devra...")
- Identifie le responsable le plus précisément possible (nom, fonction ou entreprise)
- Déduis l'échéance si une date est mentionnée (sinon null)
- Classe la priorité : "critique" si délai dépassé ou risque fort, "haute" si important, "normale" sinon
- La "synthèse" est un résumé de 2-3 phrases des décisions principales

Réponds en JSON strict (aucun texte en dehors) :
{{
  "titre_reunion": "...",
  "date_reunion": "YYYY-MM-DD ou null",
  "participants": ["Prénom Nom — Rôle/Entreprise"],
  "actions": [
    {{
      "description": "Action concrète et actionnable",
      "responsable": "Prénom Nom ou Entreprise",
      "echeance": "YYYY-MM-DD ou null",
      "priorite": "normale",
      "contexte": "Phrase exacte ou reformulée du CR qui justifie cette action"
    }}
  ],
  "synthese": "Résumé des décisions en 2-3 phrases."
}}
"""

_AGENDA_PROMPT = """\
Tu es Athéna, stratège MOE. Prépare l'ordre du jour de la prochaine réunion de chantier.

## Projet
{affaire_info}

## Actions ouvertes (à suivre ou à lever)
{actions_ouvertes}

## Dernières analyses agents (contexte récent)
{contexte_agents}

{instructions_sup}

## Instructions
- Commence par les points urgents (actions critiques ou en retard)
- Groupe les sujets connexes
- Estime une durée réaliste par point
- Anticipe les décisions à prendre et les documents à préparer
- Les "notes_preparatoires" sont des conseils au MOE avant la réunion

Types de points : "urgence" | "suivi" | "nouveau" | "decision"

Réponds en JSON strict :
{{
  "titre": "Ordre du jour — Réunion de chantier du {date_str}",
  "items": [
    {{
      "ordre": 1,
      "sujet": "Sujet clair et actionnable",
      "type": "suivi",
      "porteur": "Qui anime ce point",
      "duree_min": 10,
      "contexte": "Pourquoi ce point est important"
    }}
  ],
  "notes_preparatoires": "Conseils pour préparer la réunion (documents à avoir, points sensibles)."
}}
"""


# ── Helpers LLM ──────────────────────────────────────────────────────────────


def _parse_json(content: str) -> dict:
    content = content.strip()
    start = content.find("{")
    end = content.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(content[start:end])
        except json.JSONDecodeError:
            pass
    return {}


async def _llm(prompt: str) -> str:
    response = await LlmService._get_client().chat.completions.create(
        model=settings.effective_llm_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=4096,
    )
    return response.choices[0].message.content or ""


# ── Analyse CR ───────────────────────────────────────────────────────────────


async def analyse_cr(db: AsyncSession, cr: MeetingCR) -> MeetingCR:
    """
    Lance l'analyse LLM du CR et crée les actions extraites.
    Met à jour le CR avec synthèse + status.
    """
    if not cr.contenu_brut or len(cr.contenu_brut.strip()) < 20:
        cr.analyse_status = "failed"
        await db.commit()
        return cr

    cr.analyse_status = "running"
    await db.commit()

    try:
        raw = await _llm(_CR_ANALYSIS_PROMPT.format(contenu=cr.contenu_brut[:6000]))
        parsed = _parse_json(raw)

        if not parsed:
            raise ValueError("Réponse LLM non parseable")

        # Mettre à jour les métadonnées du CR
        if parsed.get("titre_reunion") and not cr.titre.startswith("CR —"):
            cr.titre = parsed["titre_reunion"][:256]

        if parsed.get("date_reunion"):
            try:
                cr.date_reunion = date.fromisoformat(parsed["date_reunion"])
            except (ValueError, TypeError):
                pass

        if parsed.get("participants"):
            cr.participants = parsed["participants"][:20]

        cr.synthese = parsed.get("synthese", "")[:1000]

        # Créer les actions
        actions_data = parsed.get("actions", [])
        for a in actions_data:
            if not a.get("description"):
                continue

            echeance = None
            if a.get("echeance"):
                try:
                    echeance = date.fromisoformat(a["echeance"])
                except (ValueError, TypeError):
                    pass

            action = MeetingAction(
                affaire_id=cr.affaire_id,
                cr_id=cr.id,
                description=a["description"][:500],
                responsable=a.get("responsable", "")[:128] or None,
                echeance=echeance,
                priorite=a.get("priorite", "normale"),
                statut="ouvert",
                contexte=a.get("contexte", "")[:500] or None,
            )
            db.add(action)

        cr.analyse_status = "completed"
        log.info(
            "meeting.cr_analysed",
            cr_id=str(cr.id),
            actions=len(actions_data),
            synthese_len=len(cr.synthese),
        )

    except Exception as exc:
        log.error("meeting.analyse_failed", cr_id=str(cr.id), error=str(exc))
        cr.analyse_status = "failed"

    await db.commit()
    await db.refresh(cr)
    return cr


# ── Génération ordre du jour ──────────────────────────────────────────────────


async def generate_agenda(
    db: AsyncSession,
    affaire_id: UUID,
    user_id: UUID | None,
    date_prevue: Optional[date] = None,
    instructions_supplementaires: Optional[str] = None,
) -> MeetingAgenda:
    """
    Athéna génère un ordre du jour basé sur :
    - les actions ouvertes de l'affaire
    - les derniers runs agents (contexte récent)
    - les informations du projet
    """
    from apps.affaires.models import Affaire
    from apps.agent.models import AgentRun

    # Contexte projet
    affaire = await db.get(Affaire, affaire_id)
    affaire_info = (
        (
            f"Projet : {affaire.nom} ({affaire.code})\n"
            f"Statut : {affaire.statut}\n"
            f"Description : {affaire.description or '—'}"
        )
        if affaire
        else "Projet inconnu"
    )

    # Actions ouvertes
    result_actions = await db.execute(
        select(MeetingAction)
        .where(
            MeetingAction.affaire_id == affaire_id,
            MeetingAction.statut.in_(["ouvert", "en_cours"]),
        )
        .order_by(MeetingAction.priorite.desc(), MeetingAction.echeance.asc().nulls_last())
        .limit(20)
    )
    actions = result_actions.scalars().all()
    actions_ids = [str(a.id) for a in actions]

    def _fmt_action(a: MeetingAction) -> str:
        ech = a.echeance.isoformat() if a.echeance else "sans échéance"
        retard = ""
        if a.echeance and a.echeance < date.today() and a.statut != "clos":
            retard = " ⚠️ EN RETARD"
        return f"[{a.priorite.upper()}{retard}] {a.description} — {a.responsable or '?'} (échéance : {ech})"

    actions_text = "\n".join(_fmt_action(a) for a in actions) if actions else "Aucune action ouverte."

    # Derniers runs agents (résumé contexte)
    result_runs = await db.execute(
        select(AgentRun.result, AgentRun.created_at)
        .where(AgentRun.affaire_id == affaire_id, AgentRun.status == "completed")
        .order_by(AgentRun.created_at.desc())
        .limit(3)
    )
    runs = result_runs.all()
    contexte_agents = (
        "\n\n---\n".join(f"[{r.created_at.strftime('%d/%m/%Y')}] {(r.result or '')[:400]}" for r in runs)
        if runs
        else "Aucune analyse récente."
    )

    date_str = date_prevue.strftime("%d/%m/%Y") if date_prevue else "à planifier"
    instructions_sup = (
        f"\n## Instructions supplémentaires\n{instructions_supplementaires}" if instructions_supplementaires else ""
    )

    prompt = _AGENDA_PROMPT.format(
        affaire_info=affaire_info,
        actions_ouvertes=actions_text,
        contexte_agents=contexte_agents,
        date_str=date_str,
        instructions_sup=instructions_sup,
    )

    raw = await _llm(prompt)
    parsed = _parse_json(raw)

    titre = parsed.get("titre", f"Ordre du jour — {date_str}")[:256]
    items = parsed.get("items", [])
    notes = parsed.get("notes_preparatoires", "")[:2000]

    agenda = MeetingAgenda(
        affaire_id=affaire_id,
        created_by=user_id,
        titre=titre,
        date_prevue=date_prevue,
        items=items,
        notes_preparatoires=notes,
        actions_incluses=actions_ids,
    )
    db.add(agenda)
    await db.commit()
    await db.refresh(agenda)

    log.info(
        "meeting.agenda_generated",
        agenda_id=str(agenda.id),
        items=len(items),
        actions_considérées=len(actions),
    )
    return agenda


# ── Export texte ──────────────────────────────────────────────────────────────


def agenda_to_text(agenda: MeetingAgenda) -> str:
    """Formate l'ordre du jour en texte lisible (copier-coller, email)."""
    lines = [
        f"# {agenda.titre}",
        f"Date : {agenda.date_prevue.strftime('%d/%m/%Y') if agenda.date_prevue else 'À définir'}",
        "",
    ]
    for item in agenda.items:
        duree = f"{item.get('duree_min', '?')} min"
        porteur = item.get("porteur", "")
        type_badge = {"urgence": "🔴", "suivi": "🟡", "nouveau": "🔵", "decision": "⚫"}.get(item.get("type", ""), "•")
        lines.append(f"{item.get('ordre', '?')}. {type_badge} {item.get('sujet', '')}  ({duree})")
        if porteur:
            lines.append(f"   Porteur : {porteur}")
        if item.get("contexte"):
            lines.append(f"   → {item['contexte']}")
        lines.append("")

    if agenda.notes_preparatoires:
        lines += ["---", "## Notes préparatoires", agenda.notes_preparatoires]

    return "\n".join(lines)
