"""
Orchestra — nœuds d'évaluation (M2).

  zeus_judge   : Zeus juge si les résultats couvrent la demande (loop guard intégré)
  veto_check   : veto structuré Thémis/Héphaïstos/Apollon (layer 0 regex + LLM Instructor)
  score_decision : scoring décisionnel 100pts/5axes pour C4/C5
"""

from uuid import UUID

from ._shared import (
    OrchestraState,
    CRITICITE_ROUTING,
    _llm_call,
    _parse_json_response,
    _zeus_system,
    _get_soul,
    get_agent_role,
    log,
)

# ── Prompt Zeus juge ─────────────────────────────────────────────────

_ZEUS_JUDGE_PROMPT = """\
Tu as orchestré une analyse multi-agents. Juge si les résultats couvrent la demande.

## Demande initiale
{instruction}

## Résultats des agents
{results}

Réponds en JSON strict :
{{
  "verdict": "complete",
  "synthesis_instruction": "Instruction pour la synthèse finale",
  "complement_requests": []
}}

Ou si des compléments sont nécessaires (une seule fois !) :
{{
  "verdict": "needs_complement",
  "synthesis_instruction": "",
  "complement_requests": [
    {{"agent": "<nom>", "instruction": "<complément ciblé>", "priority": 1}}
  ]
}}
"""


# ── Veto séquentiel C4/C5 — prompt + helper ──────────────────────────

_SEQUENTIAL_VETO_PROMPT = """\
Une décision de criticité {criticite} est en cours d'arbitrage.
Examine les analyses ci-dessous depuis ton expertise exclusive et émets un veto
FORMEL si tu identifies un blocage relevant de ta compétence.

## Demande originale
{instruction}

## Résultats des agents
{results}

Réponds UNIQUEMENT en JSON strict :
{{
  "veto": true ou false,
  "severity": "bloquant" | "reserve" | "information",
  "motif": "<1-2 phrases si veto=true, sinon chaîne vide>",
  "condition_levee": "<ce qu'il faut produire/valider pour lever le veto>"
}}

Règles :
- Émet un veto "bloquant" uniquement si tu identifies un risque réel relevant de ton domaine
- "reserve" si une précaution s'impose mais ne bloque pas
- "information" si tout est conforme dans ton domaine
- Tout veto "bloquant" DOIT avoir une condition_levee concrète
"""


async def _call_veto_explicit(
    agent_name: str,
    instruction: str,
    results_text: str,
    criticite: str,
):
    """Appel LLM dédié pour un agent veto (pas run_agent — 0 DB, 0 mémoire).

    Utilisé pour la chaîne séquencée C4/C5 : force Thémis et Héphaïstos à
    examiner la décision même s'ils n'étaient pas dans la liste initiale Zeus.
    """
    from apps.guards.schemas import VetoDecision
    from apps.guards.veto_patterns import fast_veto_check

    soul = _get_soul(agent_name)
    prompt = _SEQUENTIAL_VETO_PROMPT.format(
        criticite=criticite,
        instruction=instruction[:2000],
        results=results_text[:4000],
    )

    try:
        raw = await _llm_call(soul, prompt)
    except Exception as exc:
        log.warning("orchestra.sequential_veto_llm_failed", agent=agent_name, error=str(exc))
        return VetoDecision(
            veto=False,
            agent=agent_name,
            severity="information",
            motif="",
            condition_levee="",
        )

    # Couche 0 : fast patterns sur la sortie LLM
    fast = fast_veto_check(agent_name, raw)
    if fast is not None:
        fast.agent = agent_name
        log.info("orchestra.sequential_veto_fast", agent=agent_name, severity=fast.severity)
        return fast

    # Couche 1 : parse JSON
    parsed = _parse_json_response(raw)
    veto = bool(parsed.get("veto", False))
    severity = parsed.get("severity", "information")
    if severity not in ("bloquant", "reserve", "information"):
        severity = "information"

    decision = VetoDecision(
        veto=veto,
        agent=agent_name,
        severity=severity if veto else "information",
        motif=parsed.get("motif", ""),
        condition_levee=parsed.get("condition_levee", ""),
    )
    log.info(
        "orchestra.sequential_veto_done",
        agent=agent_name,
        veto=veto,
        severity=decision.severity,
    )
    return decision


# ── Nœuds LangGraph ──────────────────────────────────────────────────


async def zeus_judge(state: OrchestraState) -> dict:
    """Phase 4a — Zeus juge si les résultats sont complets."""
    results_text = "\n\n".join(f"### {agent}\n{result}" for agent, result in state["agent_results"].items())
    prompt = _ZEUS_JUDGE_PROMPT.format(
        instruction=state["instruction"],
        results=results_text,
    )
    content = await _llm_call(_zeus_system(), prompt)
    parsed = _parse_json_response(content)

    verdict = parsed.get("verdict", "complete")
    complements = parsed.get("complement_requests", [])
    synthesis_instruction = parsed.get("synthesis_instruction", state["instruction"])

    # Loop guard (M2 — guards module) : empêche les boucles
    # d'enrichissement infinies. Le seuil max_complements dépend de la
    # criticité : C1/C2 = 0, C3 = 1, C4 = 2, C5 = 3.
    from apps.guards.service import GuardsService, MAX_COMPLEMENTS_BY_CRITICITE

    _criticite = state.get("criticite", "C3")
    _max = MAX_COMPLEMENTS_BY_CRITICITE.get(_criticite, 1)
    loop_verdict = GuardsService.loop_guard(state, max_complements=_max)
    if not loop_verdict.should_continue and verdict == "needs_complement":
        log.info(
            "orchestra.loop_guard_stop",
            reason=loop_verdict.reason,
            iteration=loop_verdict.iteration,
        )
        verdict = "complete"

    log.info("orchestra.zeus_verdict", verdict=verdict, complements=len(complements))
    return {
        "assignments": complements if verdict == "needs_complement" else state["assignments"],
        "synthesis_agent": state.get("synthesis_agent", "mnemosyne"),
        "instruction": synthesis_instruction if verdict == "complete" else state["instruction"],
        "verdict": verdict,
    }


async def veto_check(state: OrchestraState) -> dict:
    """Nœud veto — chaîne séquencée Thémis → Héphaïstos (+ Apollon si présent).

    C1/C2 : skip.
    C3    : post-analyse des sorties agents existantes via structured_veto.
    C4/C5 : chaîne séquencée explicite — Thémis et Héphaïstos sont appelés
            directement même s'ils n'étaient pas dans la liste initiale Zeus.
            Apollon est ensuite analysé si présent dans agent_results.
            Le veto le plus sévère (bloquant > reserve) déclenche un interrupt
            HITL pour C4/C5.
    """
    import asyncio
    from langgraph.types import interrupt
    from apps.guards.service import GuardsService

    criticite = state.get("criticite", "C2")
    routing = CRITICITE_ROUTING.get(criticite, CRITICITE_ROUTING["C2"])
    if not routing.get("veto_check"):
        log.info("orchestra.veto_skipped", criticite=criticite)
        return {"veto_agent": "", "veto_motif": "", "veto_severity": "", "veto_condition_levee": ""}

    results = state.get("agent_results", {})
    instruction = state["instruction"]
    results_text = "\n\n".join(f"### {a}\n{r}" for a, r in results.items())

    all_verdicts = []

    if criticite in ("C4", "C5"):
        # ── Chaîne séquencée : Thémis puis Héphaïstos en parallèle ──────
        # Appels LLM directs (pas run_agent) — 0 DB, 0 mémoire, ~1 LLM call chacun.
        # Garantit que ces gardiens examinent TOUJOURS les décisions C4/C5.
        themis_task = _call_veto_explicit("themis", instruction, results_text, criticite)
        hephaistos_task = _call_veto_explicit("hephaistos", instruction, results_text, criticite)
        themis_d, hephaistos_d = await asyncio.gather(themis_task, hephaistos_task)

        # Ordre de priorité : Thémis d'abord (juridique > technique)
        for d in (themis_d, hephaistos_d):
            if d.veto:
                all_verdicts.append(d)

        # Apollon (normatif) — uniquement si présent dans les résultats existants
        if results.get("apollon"):
            apollon_d = await GuardsService.structured_veto(
                agent="apollon",
                agent_output=results["apollon"],
                criticite=criticite,
            )
            if apollon_d.veto:
                all_verdicts.append(apollon_d)

    else:
        # C3 — post-analyse des sorties existantes uniquement
        for agent_name in [a for a in ("themis", "hephaistos", "apollon") if results.get(a)]:
            d = await GuardsService.structured_veto(
                agent=agent_name,
                agent_output=results[agent_name],
                criticite=criticite,
            )
            if d.veto:
                all_verdicts.append(d)

    # Sélection du veto le plus sévère : bloquant > reserve
    worst_veto = None
    for v in all_verdicts:
        if v.severity == "bloquant":
            worst_veto = v
            break
        if v.severity == "reserve" and worst_veto is None:
            worst_veto = v

    if worst_veto is None:
        return {"veto_agent": "", "veto_motif": "", "veto_severity": "", "veto_condition_levee": ""}

    update = {
        "veto_agent": worst_veto.agent,
        "veto_motif": worst_veto.motif,
        "veto_severity": worst_veto.severity,
        "veto_condition_levee": worst_veto.condition_levee,
    }

    if worst_veto.severity == "bloquant" and criticite in ("C4", "C5"):
        log.warning(
            "orchestra.veto_blocking",
            agent=worst_veto.agent,
            role=get_agent_role(worst_veto.agent),
            criticite=criticite,
            condition_levee=(worst_veto.condition_levee or "")[:120],
        )
        interrupt(
            {
                "veto_agent": worst_veto.agent,
                "veto_motif": worst_veto.motif,
                "veto_severity": worst_veto.severity,
                "veto_condition_levee": worst_veto.condition_levee,
                "message": (
                    f"⚠️ Veto bloquant émis par {worst_veto.agent.upper()} — "
                    f"validation humaine requise.\n"
                    f"Motif : {worst_veto.motif}\n"
                    f"Condition de levée : {worst_veto.condition_levee or '—'}"
                ),
                "assignments": state.get("assignments", []),
            }
        )
    else:
        log.info(
            "orchestra.veto_traced",
            agent=worst_veto.agent,
            role=get_agent_role(worst_veto.agent),
            severity=worst_veto.severity,
            criticite=criticite,
        )

    return update


def _compute_lightweight_run_score(state: OrchestraState) -> dict:
    """Score multi-critères léger (amélioration 1) — règles et heuristiques, 0 LLM.

    Axes :
      quality    — couverture agents (résultats / attendus)
      coherence  — présence et longueur de la réponse finale
      confidence — verdict precheck (approved > trim > upgrade > clarification)
      risk       — sévérité du veto (aucun = haute confiance)
    """
    results = state.get("agent_results", {})
    n_results = len(results)
    n_initial = max(len(state.get("initial_agents", [1])), 1)

    # Quality : ratio agents ayant répondu / attendus
    quality = min(100, int((n_results / n_initial) * 100))

    # Coherence : longueur de la réponse finale
    final = state.get("final_answer", "")
    if not final:
        coherence = 10
    else:
        coherence = min(100, 20 + len(final) // 30)

    # Confidence : verdict precheck
    precheck = state.get("precheck_verdict", "approved")
    _confidence_map = {"approved": 90, "trim": 72, "upgrade": 60, "clarification": 35, "blocked": 10, "": 80}
    confidence = _confidence_map.get(precheck, 70)

    # Risk : sévérité veto (inversé — risk élevé = mauvais)
    veto_sev = state.get("veto_severity", "")
    _risk_map = {"bloquant": 15, "reserve": 45, "information": 75, "": 90}
    risk = _risk_map.get(veto_sev, 90)

    return {
        "quality": quality,
        "coherence": coherence,
        "confidence": confidence,
        "risk": risk,
    }


async def score_decision(state: OrchestraState) -> dict:
    """Score décisionnel + score multi-critères global (amélioration 1).

    Tous les runs : run_score {quality, coherence, confidence, risk}.
    C4/C5 seulement : ScoringService complet (5 axes / 100 pts) en plus.
    """
    criticite = state.get("criticite", "C2")

    # ── Score multi-critères léger (tous les runs) ────────────────────
    run_score = _compute_lightweight_run_score(state)
    log.info(
        "orchestra.run_score",
        criticite=criticite,
        quality=run_score["quality"],
        coherence=run_score["coherence"],
        confidence=run_score["confidence"],
        risk=run_score["risk"],
    )
    updates: dict = {"run_score": run_score}

    if criticite not in ("C4", "C5"):
        return updates

    # ── Score décisionnel complet C4/C5 (ScoringService) ─────────────
    from apps.scoring.service import ScoringService
    from database import AsyncSessionLocal

    sujet = state["instruction"][:512]
    contexte = "\n\n".join(f"### {agent}\n{result}" for agent, result in state.get("agent_results", {}).items())

    try:
        async with AsyncSessionLocal() as db:
            score = await ScoringService.score_auto(
                db,
                sujet=sujet,
                contexte=contexte,
                affaire_id=UUID(state["affaire_id"]) if state.get("affaire_id") else None,
                certitude=0.7,
                computed_by=UUID(state["user_id"]) if state.get("user_id") else None,
            )
        log.info(
            "orchestra.score_done",
            score_id=str(score.id),
            verdict=score.verdict,
            total=score.total_final,
        )
        updates.update({
            "score_id": str(score.id),
            "score_verdict": score.verdict,
            "score_total": score.total_final,
        })
    except Exception as exc:
        log.error("orchestra.score_failed", error=str(exc))

    return updates
