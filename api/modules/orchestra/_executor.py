"""
Orchestra — moteur d'exécution (M3).

Patterns d'exécution :
  _exec_parallel   : agents indépendants en asyncio.gather
  _exec_cascade    : séquence avec contexte cumulatif
  _exec_arena      : compétition parallèle + juge arbitre
  _topological_levels : tri topologique BFS des dépendances entre sous-tâches

Nœuds LangGraph :
  dispatch_subtasks   : niveau par niveau + pattern routing
  execute_complements : exécution des compléments demandés par zeus_judge
"""
import asyncio
from uuid import UUID

from ._shared import (
    OrchestraState,
    VALID_AGENTS,
    _run_agent_isolated,
    log,
)

# ── Prompt arène ─────────────────────────────────────────────────────

_ARENA_JUDGE_PROMPT = """\
Tu arbitres une arène entre {n} agents sur la même question.

## Question
{instruction}

## Propositions des agents
{proposals}

Analyse chaque proposition. Synthétise ou retiens la plus solide.
Structure ta réponse :
1. **Proposition retenue / synthèse** : quelle option et pourquoi
2. **Points forts** : ce qui est solide dans les propositions
3. **Réserves** : ce qui doit être pondéré ou nuancé
4. **Recommandation finale** : ta conclusion opérationnelle
"""


# ── Patterns d'exécution ─────────────────────────────────────────────

def _topological_levels(subtasks: list[dict]) -> list[list[dict]]:
    """Groupe les sous-tâches par niveau d'exécution (tri topologique BFS).
    Les sous-tâches sans dépendances forment le niveau 0, etc."""
    if not subtasks:
        return []
    completed: set[str] = set()
    remaining = list(subtasks)
    levels = []
    while remaining:
        ready = [t for t in remaining if all(dep in completed for dep in t.get("depends_on", []))]
        if not ready:
            # Dépendance circulaire ou manquante → tout exécuter
            ready = remaining
        levels.append(ready)
        completed.update(t["id"] for t in ready)
        remaining = [t for t in remaining if t["id"] not in completed]
    return levels


async def _exec_parallel(
    agents_instructions: dict[str, str],
    affaire_uuid: UUID,
    user_uuid: UUID | None,
    thread_id: str = "",
) -> tuple[dict, list]:
    """Exécute plusieurs agents en parallèle. {agent: instruction} → ({agent: result}, [run_ids])"""
    tasks = [
        _run_agent_isolated(agent, instr, affaire_uuid, user_uuid, thread_id)
        for agent, instr in agents_instructions.items()
    ]
    raw = await asyncio.gather(*tasks, return_exceptions=True)
    results, run_ids = {}, []
    for r in raw:
        if isinstance(r, Exception):
            log.error("orchestra.parallel_failed", error=str(r))
            continue
        agent_name, result_text, run_id = r
        results[agent_name] = result_text
        run_ids.append(run_id)
    return results, run_ids


async def _exec_cascade(
    agents: list[str],
    instruction: str,
    affaire_uuid: UUID,
    user_uuid: UUID | None,
    thread_id: str = "",
) -> tuple[dict, list]:
    """Exécute les agents en séquence — chaque agent reçoit le contexte des précédents."""
    results, run_ids = {}, []
    for agent in agents:
        if results:
            prior = "\n\n".join(f"### {a}\n{r}" for a, r in results.items())
            agent_instruction = (
                f"{instruction}\n\n"
                f"## Contexte — analyses précédentes\n{prior}\n\n"
                f"Appuie ton analyse sur ce qui précède."
            )
        else:
            agent_instruction = instruction
        try:
            _, result_text, run_id = await _run_agent_isolated(
                agent, agent_instruction, affaire_uuid, user_uuid, thread_id
            )
            results[agent] = result_text
            run_ids.append(run_id)
        except Exception as exc:
            log.error("orchestra.cascade_failed", agent=agent, error=str(exc))
    return results, run_ids


async def _exec_arena(
    agents: list[str],
    judge: str,
    instruction: str,
    affaire_uuid: UUID,
    user_uuid: UUID | None,
    thread_id: str = "",
) -> tuple[dict, list]:
    """Round 0 : agents en parallèle sur la même question.
    Round 1 : le juge reçoit toutes les propositions et arbitre."""
    tasks = [_run_agent_isolated(a, instruction, affaire_uuid, user_uuid, thread_id) for a in agents]
    raw = await asyncio.gather(*tasks, return_exceptions=True)
    results, run_ids = {}, []
    for r in raw:
        if isinstance(r, Exception):
            log.error("orchestra.arena_round0_failed", error=str(r))
            continue
        agent_name, result_text, run_id = r
        results[agent_name] = result_text
        run_ids.append(run_id)

    if not results:
        return results, run_ids

    proposals_text = "\n\n".join(
        f"## Proposition {agent}\n{result}"
        for agent, result in results.items()
    )
    judge_instruction = _ARENA_JUDGE_PROMPT.format(
        n=len(results),
        instruction=instruction,
        proposals=proposals_text,
    )
    judge_key = f"{judge}__verdict"
    try:
        _, judge_result, judge_run_id = await _run_agent_isolated(
            judge, judge_instruction, affaire_uuid, user_uuid, thread_id
        )
        results[judge_key] = judge_result
        run_ids.append(judge_run_id)
    except Exception as exc:
        log.error("orchestra.arena_judge_failed", judge=judge, error=str(exc))

    return results, run_ids


# ── Nœuds LangGraph ──────────────────────────────────────────────────

async def dispatch_subtasks(state: OrchestraState) -> dict:
    """Phase 3 — dispatch des sous-tâches selon leur pattern.

    Exécution niveau par niveau (topologique). Au sein d'un niveau,
    les sous-tâches sans dépendance commune tournent en parallèle.
    """
    affaire_uuid = UUID(state["affaire_id"])
    user_uuid = UUID(state["user_id"]) if state.get("user_id") else None
    thread_id = state.get("thread_id", "")

    subtasks = state.get("subtasks", [])

    if not subtasks:
        # Fallback : exécution parallèle simple des assignments
        log.info("orchestra.dispatch_fallback",
                 agents=[a["agent"] for a in state["assignments"]])
        agents_instructions = {a["agent"]: a["instruction"] for a in state["assignments"]}
        results, run_ids = await _exec_parallel(
            agents_instructions, affaire_uuid, user_uuid, thread_id
        )
        return {
            "agent_results": results,
            "subtask_results": {"T1": results},
            "agent_run_ids": run_ids,
        }

    agent_results: dict = {}
    subtask_results: dict = {}
    all_run_ids: list = []

    levels = _topological_levels(subtasks)
    log.info("orchestra.dispatch_levels",
             levels=[[s["id"] for s in lvl] for lvl in levels])

    for level in levels:
        level_tasks = []
        for st in level:
            instruction = st.get("instruction") or state["instruction"]
            pattern = st.get("pattern", "parallel")
            agents = st["agents"]
            judge = st.get("judge", "")

            # Injecter les résultats des dépendances dans l'instruction
            deps_results = {}
            for dep_id in st.get("depends_on", []):
                deps_results.update(subtask_results.get(dep_id, {}))
            if deps_results:
                deps_text = "\n\n".join(f"### {a}\n{r}" for a, r in deps_results.items())
                instruction = (
                    f"{instruction}\n\n"
                    f"## Résultats des sous-tâches précédentes\n{deps_text}"
                )

            if pattern == "cascade":
                level_tasks.append((st["id"], _exec_cascade(
                    agents, instruction, affaire_uuid, user_uuid, thread_id
                )))
            elif pattern == "arena":
                eff_judge = judge if judge in VALID_AGENTS else "apollon"
                level_tasks.append((st["id"], _exec_arena(
                    agents, eff_judge, instruction, affaire_uuid, user_uuid, thread_id
                )))
            elif pattern == "exploration":
                exploration_agents = ["dionysos", "promethee", "apollon"]
                if len(agents) >= 2:
                    exploration_agents = agents
                level_tasks.append((st["id"], _exec_cascade(
                    exploration_agents, instruction, affaire_uuid, user_uuid, thread_id
                )))
            elif pattern == "solo":
                level_tasks.append((st["id"], _exec_parallel(
                    {agents[0]: instruction}, affaire_uuid, user_uuid, thread_id
                )))
            else:  # parallel (default)
                agent_instrs = st.get("_agent_instructions",
                                      {a: instruction for a in agents})
                level_tasks.append((st["id"], _exec_parallel(
                    agent_instrs, affaire_uuid, user_uuid, thread_id
                )))

        level_coros = [coro for _, coro in level_tasks]
        level_ids = [tid for tid, _ in level_tasks]
        level_results = await asyncio.gather(*level_coros, return_exceptions=True)

        for task_id, result in zip(level_ids, level_results):
            if isinstance(result, Exception):
                log.error("orchestra.subtask_failed", task_id=task_id, error=str(result))
                continue
            task_agent_results, task_run_ids = result
            subtask_results[task_id] = task_agent_results
            agent_results.update(task_agent_results)
            all_run_ids.extend(task_run_ids)

    log.info("orchestra.dispatch_done", agents=list(agent_results.keys()))
    return {
        "agent_results": agent_results,
        "subtask_results": subtask_results,
        "agent_run_ids": all_run_ids,
    }


async def execute_complements(state: OrchestraState) -> dict:
    """Phase 3b — exécution des compléments demandés par Zeus."""
    affaire_uuid = UUID(state["affaire_id"])
    user_uuid = UUID(state["user_id"]) if state.get("user_id") else None
    thread_id = state.get("thread_id", "")

    log.info("orchestra.complements", agents=[a["agent"] for a in state["assignments"]])
    tasks = [
        _run_agent_isolated(
            agent=a["agent"],
            instruction=a["instruction"],
            affaire_id=affaire_uuid,
            user_id=user_uuid,
            thread_id=thread_id,
        )
        for a in state["assignments"]
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    agent_results = dict(state["agent_results"])
    agent_run_ids = list(state["agent_run_ids"])
    for r in results:
        if isinstance(r, Exception):
            continue
        agent_name, result_text, run_id = r
        agent_results[agent_name] = result_text
        agent_run_ids.append(run_id)

    return {
        "agent_results": agent_results,
        "agent_run_ids": agent_run_ids,
        "complement_done": True,
    }
