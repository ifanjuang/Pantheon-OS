"""
GuardsService — gardes-fous explicites pour l'orchestre Zeus.

Quatre garde-fous :

  criticality_guard(impacts) → CriticalityVerdict
    Règles pures (pas de LLM) pour dériver C1-C5 depuis l'impact
    financier, le délai, la sévérité et l'intent Hermès. Sert de
    filet de sécurité quand l'agent d'analyse (ou l'utilisateur)
    sous-estime la criticité d'une demande.

  reversibility_guard(decision, criticite, impacts) → ReversibilityDecision
    LLM via Instructor. Détermine si la décision peut être défaite
    sans coût majeur. Si non → requires_hitl=True même si la
    criticité est C3 (ex : envoi d'un courrier recommandé, signature
    de bon de commande).

  loop_guard(state, max_complements=1) → LoopGuardVerdict
    Règle pure. Empêche les boucles d'enrichissement infinies dans
    `zeus_judge`. Remplace le `if state.get("complement_done")` inline.

  structured_veto(agent, agent_output, criticite) → VetoDecision
    LLM via Instructor. Remplace la détection keyword `_VETO_KEYWORDS`
    par une analyse structurée de la sortie Thémis / Héphaïstos /
    Apollon. Retourne veto: bool, severity (bloquant|reserve|info),
    motif et condition_levee.

Chaque LLM guard inclut un fallback silencieux : en cas d'échec, on
renvoie une décision permissive (pas de veto, réversible par défaut)
pour ne pas bloquer l'orchestration.
"""
from typing import Any, Optional

from pydantic import BaseModel, Field

from core.logging import get_logger
from core.services.llm_service import LlmService
from modules.guards.schemas import (
    CriticalityImpacts,
    CriticalityVerdict,
    LoopGuardVerdict,
    ReversibilityDecision,
    VetoDecision,
)
from modules.guards.veto_patterns import fast_veto_check

log = get_logger("guards.service")


# ── Seuils loop_guard par criticité ──────────────────────────────────
# C1/C2 (information/question) : pas de boucle d'enrichissement
# C3 (décision locale)         : 1 complément maximum
# C4 (décision engageante)     : 2 compléments maximum
# C5 (risque majeur)           : 3 compléments maximum
MAX_COMPLEMENTS_BY_CRITICITE: dict[str, int] = {
    "C1": 0,
    "C2": 0,
    "C3": 1,
    "C4": 2,
    "C5": 3,
}


# ── Seuils criticality_guard (règles pures) ──────────────────────────

_COST_C5 = 50_000.0   # > 50 k€ → C5
_COST_C4 = 10_000.0   # > 10 k€ → C4
_COST_C3 = 2_000.0    # > 2 k€ → C3

_DELAY_C5 = 30        # > 30 jours → C5
_DELAY_C4 = 10        # > 10 jours → C4
_DELAY_C3 = 3         # > 3 jours → C3

_SEVERITY_C5 = {
    "risque_majeur", "risque majeur", "securite", "sécurité",
    "litige", "peril", "péril", "contentieux", "urgence_vitale",
}
_SEVERITY_C4 = {
    "decision_engageante", "décision_engageante", "engagement",
    "contrat", "signature", "engageant",
}
_SEVERITY_C3 = {
    "decision_locale", "décision_locale", "reversible", "réversible",
}

_INTENT_C4 = {"decision_engageante"}
_INTENT_C3 = {"decision_locale"}
_INTENT_C2 = {"question", "alerte"}


# ── Modèle Instructor (usage interne) ────────────────────────────────

class _CriticalityAI(BaseModel):
    """Réponse Instructor pour la couche AI du criticality_guard_hybrid."""
    criticite: str = Field(..., pattern=r"^C[1-5]$")
    reasoning: str = Field(..., description="Justification courte (1-2 phrases)")


# ── Gamme ambiguë — l'AI n'intervient que si la règle retombe dedans ─

_CRITICALITY_AMBIGUOUS = {"C2", "C3", "C4"}

# ── Prompt couche AI criticality_guard_hybrid ─────────────────────────

_CRITICALITY_HYBRID_PROMPT = """\
Tu es Thémis (réglementation MOE, contrat, déontologie) et Héphaïstos (technique, DTU, faisabilité).

Les règles déterministes ont évalué cette situation et proposent : {current_level}
Raisons identifiées par les règles : {triggers}

Situation MOE décrite par l'utilisateur :
{context}

Ta mission : valider ou remonter la criticité C1-C5. Tu ne peux PAS descendre.

Remonte à C4 si tu détectes :
- Engagement contractuel ou financier non anticipé par les règles
- Avenant requis, responsabilité MOE engagée, délai légal imminente
- Décision difficile à annuler, impact tiers (entreprise, MOA, sous-traitant)

Remonte à C5 si tu détectes :
- Sécurité des personnes (risque physique, péril structurel)
- Litige probable, contentieux, mise en demeure potentielle
- Hors mission MOE évidente, non-conformité DTU grave, infaisabilité technique

En cas de doute → maintiens {current_level}, n'invente pas de risque.
"""

# ── Prompts LLM ──────────────────────────────────────────────────────

_VETO_PROMPT = """\
Tu analyses la sortie d'un agent ARCEUS à la recherche d'un veto structuré.

## Agent
{agent}

## Criticité de la demande
{criticite}

## Sortie agent
{agent_output}

## Objectif
Détermine si cet agent oppose un VETO formel à la décision en cours.

Un veto est légitime si l'agent évoque :
- Thémis    : non-conformité réglementaire, risque juridique, responsabilité MOE
- Héphaïstos: infaisabilité technique, non-conformité DTU, risque structurel
- Apollon   : contradiction normative grave confirmée par sources
- Tout agent: risque majeur non assumé, besoin d'expert externe

Produis un JSON strict :
- veto              : true uniquement si veto réel, pas une simple réserve
- agent             : {agent}
- severity          : "bloquant" (stop orchestration) | "reserve" (trace) | "information" (pas de veto)
- motif             : 1-2 phrases, uniquement si veto=true
- condition_levee   : ce qu'il faut produire/valider pour lever le veto
                      (étude, visa, validation client, document manquant, …)

Règles :
- Simple remarque/réserve → severity=reserve, veto=false
- Formulation "attention à…", "à vérifier" → severity=information
- "Je m'oppose", "bloquant", "infaisable", "hors responsabilité", "veto",
  "refus", "non conforme majeur" → severity=bloquant, veto=true
- Tout veto bloquant DOIT proposer une condition_levee concrète
"""


_REVERSIBILITY_PROMPT = """\
Tu évalues la réversibilité d'une décision MOE.

## Décision envisagée
{decision}

## Criticité actuelle
{criticite}

## Impacts connus
- Coût   : {cout}
- Délai  : {delai} jours

## Objectif
Détermine si cette décision peut être défaite sans coût majeur.

Produis un JSON strict :
- reversible       : true | false
- reasoning        : 1-2 phrases
- rollback_cost    : "null" | "faible" | "modere" | "eleve" | "bloquant"
- requires_hitl    : true si la décision doit passer en validation humaine
                     même si la criticité est faible

Règles :
- Envoi de courrier officiel / notification client / signature → reversible=false
- Commande travaux / engagement financier > 5k€ → reversible=false, requires_hitl=true
- Simple note interne / brouillon / préparation dossier → reversible=true
- Dépôt administratif (PC, DP, déclaration) → reversible=false, requires_hitl=true
- Action réversible coût<5k€ et délai<3j → reversible=true, requires_hitl=false
"""


# ── GuardsService ────────────────────────────────────────────────────

class GuardsService:

    # ── criticality_guard (règle pure) ──────────────────────────────
    @classmethod
    def criticality_guard(cls, impacts: CriticalityImpacts) -> CriticalityVerdict:
        """Dérive C1-C5 depuis impacts financiers/planning/sévérité.

        Logique : on retient la criticité MAX entre toutes les règles
        activées (cost / delay / severity / intent / reversible).
        """
        triggers: list[str] = []
        levels: list[int] = [1]  # minimum C1

        # Règle coût
        if impacts.impact_cout is not None:
            if impacts.impact_cout > _COST_C5:
                levels.append(5)
                triggers.append(f"cout>{_COST_C5:.0f}€")
            elif impacts.impact_cout > _COST_C4:
                levels.append(4)
                triggers.append(f"cout>{_COST_C4:.0f}€")
            elif impacts.impact_cout > _COST_C3:
                levels.append(3)
                triggers.append(f"cout>{_COST_C3:.0f}€")

        # Règle délai
        if impacts.impact_delai is not None:
            if impacts.impact_delai > _DELAY_C5:
                levels.append(5)
                triggers.append(f"delai>{_DELAY_C5}j")
            elif impacts.impact_delai > _DELAY_C4:
                levels.append(4)
                triggers.append(f"delai>{_DELAY_C4}j")
            elif impacts.impact_delai > _DELAY_C3:
                levels.append(3)
                triggers.append(f"delai>{_DELAY_C3}j")

        # Règle sévérité déclarée
        if impacts.severity:
            sev = impacts.severity.lower().strip()
            if sev in _SEVERITY_C5:
                levels.append(5)
                triggers.append(f"severity={sev}")
            elif sev in _SEVERITY_C4:
                levels.append(4)
                triggers.append(f"severity={sev}")
            elif sev in _SEVERITY_C3:
                levels.append(3)
                triggers.append(f"severity={sev}")

        # Règle intent Hermès
        if impacts.intent:
            intent = impacts.intent.lower().strip()
            if intent in _INTENT_C4:
                levels.append(4)
                triggers.append(f"intent={intent}")
            elif intent in _INTENT_C3:
                levels.append(3)
                triggers.append(f"intent={intent}")
            elif intent in _INTENT_C2:
                levels.append(2)
                triggers.append(f"intent={intent}")

        # Règle réversibilité (irréversible → min C4)
        if impacts.reversible is False:
            levels.append(4)
            triggers.append("irreversible")

        level = max(levels)
        verdict = CriticalityVerdict(
            criticite=f"C{level}",
            triggers=triggers or ["default=C1"],
        )
        log.debug(
            "guards.criticality",
            criticite=verdict.criticite,
            triggers=verdict.triggers,
        )
        return verdict

    # ── criticality_guard_hybrid (règles + AI pour cas ambigus) ────────
    @classmethod
    async def criticality_guard_hybrid(
        cls,
        impacts: CriticalityImpacts,
        *,
        context: str = "",
    ) -> CriticalityVerdict:
        """Dérive C1-C5 en deux couches.

        Couche 0+1 (déterministe, 0 token) : règles pures sur coût/délai/
        sévérité/intent. Couvre les cas extrêmes (C1 évident, C5 certain).

        Couche 2 (Thémis + Héphaïstos via Instructor) : activée uniquement
        si la couche règles retourne C2/C3/C4 ET qu'un contexte textuel est
        fourni. L'AI peut seulement maintenir ou monter la criticité — jamais
        descendre.

        Fallback : en cas d'erreur LLM la couche règles fait foi.
        """
        # Couche 0+1 : règles déterministes (toujours exécutées)
        rules_verdict = cls.criticality_guard(impacts)

        # Pas de contexte ou cas extrêmes → les règles suffisent
        if not context.strip() or rules_verdict.criticite not in _CRITICALITY_AMBIGUOUS:
            return rules_verdict

        # Couche 2 : AI pour les cas ambigus (C2 / C3 / C4)
        prompt = _CRITICALITY_HYBRID_PROMPT.format(
            current_level=rules_verdict.criticite,
            triggers=", ".join(rules_verdict.triggers) or "aucune règle déclenchée",
            context=context[:4000],
        )
        try:
            ai: _CriticalityAI = await LlmService.extract(
                messages=[{"role": "user", "content": prompt}],
                response_model=_CriticalityAI,
                temperature=0.1,
            )

            # Sécurité : on ne descend jamais en dessous des règles
            rule_level = int(rules_verdict.criticite[1])
            ai_level = int(ai.criticite[1])
            final_level = max(rule_level, ai_level)
            final_criticite = f"C{final_level}"

            upgraded = final_level > rule_level
            triggers = list(rules_verdict.triggers)
            if upgraded:
                triggers.append(f"ai_upgrade:{rules_verdict.criticite}→{final_criticite}")

            verdict = CriticalityVerdict(
                criticite=final_criticite,
                triggers=triggers,
                ai_reasoning=ai.reasoning,
                source="hybrid",
            )
            log.info(
                "guards.criticality.hybrid",
                rules=rules_verdict.criticite,
                ai=ai.criticite,
                final=final_criticite,
                upgraded=upgraded,
            )
            return verdict

        except Exception as exc:
            log.warning("guards.criticality_hybrid_failed", error=str(exc))
            return rules_verdict

    # ── reversibility_guard (LLM) ───────────────────────────────────
    @classmethod
    async def reversibility_guard(
        cls,
        *,
        decision: str,
        criticite: str = "C3",
        impact_cout: Optional[float] = None,
        impact_delai: Optional[int] = None,
    ) -> ReversibilityDecision:
        """Évalue si une décision est réversible.

        Fallback : en cas d'échec LLM, renvoie reversible=True avec
        requires_hitl=True pour forcer la prudence.
        """
        prompt = _REVERSIBILITY_PROMPT.format(
            decision=decision[:3000],
            criticite=criticite,
            cout=f"{impact_cout:.0f}€" if impact_cout is not None else "—",
            delai=impact_delai if impact_delai is not None else "—",
        )
        try:
            result = await LlmService.extract(
                messages=[{"role": "user", "content": prompt}],
                response_model=ReversibilityDecision,
                temperature=0.1,
            )
            log.info(
                "guards.reversibility",
                reversible=result.reversible,
                rollback_cost=result.rollback_cost,
                requires_hitl=result.requires_hitl,
            )
            return result
        except Exception as exc:
            log.warning("guards.reversibility_failed", error=str(exc))
            return ReversibilityDecision(
                reversible=True,
                reasoning=f"Reversibility LLM indisponible : {exc}",
                rollback_cost="null",
                requires_hitl=criticite in ("C4", "C5"),
            )

    # ── loop_guard (règle pure) ─────────────────────────────────────
    @classmethod
    def loop_guard(
        cls,
        state: dict[str, Any],
        *,
        max_complements: int = 1,
    ) -> LoopGuardVerdict:
        """Empêche les boucles d'enrichissement.

        Règle : on compte le nombre de complements déjà exécutés. Au-delà
        de `max_complements`, on arrête même si Zeus demande encore un
        enrichissement.
        """
        iteration = 0
        if state.get("complement_done"):
            iteration = 1
        # Si un futur compteur existe, le respecter
        if isinstance(state.get("complement_count"), int):
            iteration = state["complement_count"]

        if iteration >= max_complements:
            verdict = LoopGuardVerdict(
                should_continue=False,
                reason=f"max_complements={max_complements} atteint",
                iteration=iteration,
            )
        else:
            verdict = LoopGuardVerdict(
                should_continue=True,
                reason="",
                iteration=iteration,
            )
        log.debug(
            "guards.loop",
            should_continue=verdict.should_continue,
            iteration=verdict.iteration,
        )
        return verdict

    # ── structured_veto (couche 0 déterministe + couche 1 LLM) ────────
    @classmethod
    async def structured_veto(
        cls,
        *,
        agent: str,
        agent_output: str,
        criticite: str = "C3",
    ) -> VetoDecision:
        """Analyse structurée d'un veto agent.

        Couche 0 (déterministe, 0 token) : fast_veto_check — patterns regex
        sur formulations explicites de blocage. Couvre ~80 % des cas évidents
        sans appel LLM.

        Couche 1 (LLM via Instructor) : uniquement si couche 0 ne conclut pas.

        Fallback couche 1 : en cas d'échec LLM, pas de veto (severity=information)
        pour ne pas bloquer l'orchestration sur une erreur réseau.
        """
        if not agent_output or len(agent_output.strip()) < 10:
            return VetoDecision(
                veto=False,
                agent=agent,
                severity="information",
                motif="",
                condition_levee="",
            )

        # Couche 0 — déterministe, instantané
        fast_result = fast_veto_check(agent, agent_output)
        if fast_result is not None:
            log.info(
                "guards.veto.fast",
                agent=agent,
                severity=fast_result.severity,
                motif=fast_result.motif[:160],
            )
            return fast_result

        # Couche 1 — LLM uniquement si couche 0 ne conclut pas
        prompt = _VETO_PROMPT.format(
            agent=agent,
            criticite=criticite,
            agent_output=agent_output[:6000],
        )
        try:
            result = await LlmService.extract(
                messages=[{"role": "user", "content": prompt}],
                response_model=VetoDecision,
                temperature=0.1,
            )
            # Sécurité : on force le champ agent au nom réel émetteur
            result.agent = agent
            log.info(
                "guards.veto",
                agent=agent,
                veto=result.veto,
                severity=result.severity,
                motif=result.motif[:160],
            )
            return result
        except Exception as exc:
            log.warning("guards.veto_failed", agent=agent, error=str(exc))
            return VetoDecision(
                veto=False,
                agent=agent,
                severity="information",
                motif=f"Veto LLM indisponible : {exc}",
                condition_levee="",
            )
