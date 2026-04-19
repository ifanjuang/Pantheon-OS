"""
Orchestra — infrastructure partagée.

Ce module contient ce qui est commun à tous les nœuds LangGraph :
  - OrchestraState (TypedDict)
  - Constantes de routing (CRITICITE_ROUTING, VALID_AGENTS, …)
  - Helpers LLM (_llm_call, _parse_json_response, _zeus_system)
  - Helper agent statique (_get_agent_summary — 0 appel LLM)
  - Exécuteur d'agent isolé (_run_agent_isolated)

Importé par _planner, _executor, _evaluator, _synthesizer et service.
"""

import asyncio
import functools
import json
import re
import time
from pathlib import Path
from typing import Optional, TypedDict
from uuid import UUID

import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from core.logging import get_logger
from core.services.llm_service import LlmService
from core.settings import settings
from database import AsyncSessionLocal
from modules.agent.service import run_agent, _build_system_prompt  # noqa: F401 (re-exporté)

log = get_logger("orchestra.service")

# Timeout d'un appel LLM Zeus (secondes) — empêche un Ollama pendu de figer l'orchestration
_LLM_TIMEOUT = 90

_ROOT = Path(__file__).parent.parent.parent.parent
AGENTS_DIR = (
    Path(settings.AGENTS_DIR)
    if hasattr(settings, "AGENTS_DIR")
    else _ROOT / "agents"
)
CORE_DIR = _ROOT / "core"   # meta-agents (zeus, hera, artemis, kairos, hermes, athena)
_REGISTRY_PATH = _ROOT / "config" / "agent_registry.yaml"


@functools.lru_cache(maxsize=1)
def _load_registry() -> dict:
    """Charge config/agent_registry.yaml (LRU cached — source unique de vérité)."""
    try:
        import yaml  # type: ignore[import]
        if _REGISTRY_PATH.exists():
            data = yaml.safe_load(_REGISTRY_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    except Exception:
        pass
    return {}


def get_agent_role(agent_name: str) -> str:
    """Retourne le rôle fonctionnel stable d'un agent depuis le registre."""
    registry = _load_registry()
    entry = registry.get(agent_name.upper(), {})
    return entry.get("role", agent_name.lower())


def get_agent_meta(agent_name: str) -> dict:
    """Retourne {agent, role, layer, class} pour un agent — clé JSON standard."""
    registry = _load_registry()
    entry = registry.get(agent_name.upper(), {})
    return {
        "agent": agent_name.upper(),
        "role": entry.get("role", agent_name.lower()),
        "layer": entry.get("layer", ""),
        "class": entry.get("class", ""),
    }
DEFAULT_AGENTS = ["themis", "athena", "chronos"]
DEFAULT_SYNTHESIS_AGENT = "kairos"  # synthèse finale — remplace mnemosyne dans ce rôle

# ── Limites cognitives par criticité (amélioration 6 — Demeter) ──────
# Empêche la sur-complexité : plus la criticité est faible, moins d'agents.
COGNITIVE_LIMITS: dict[str, dict] = {
    "C1": {"max_agents": 1, "max_subtasks": 1, "max_depth": 1},
    "C2": {"max_agents": 2, "max_subtasks": 2, "max_depth": 1},
    "C3": {"max_agents": 4, "max_subtasks": 3, "max_depth": 2},
    "C4": {"max_agents": 6, "max_subtasks": 5, "max_depth": 3},
    "C5": {"max_agents": 8, "max_subtasks": 6, "max_depth": 3},
}

# ── Activation conditionnelle des agents (amélioration 3) ────────────
# Clé absente = toujours activable. Valeur vide = jamais automatique.
# Valeur = liste des criticités (ou patterns) déclenchant cet agent.
AGENT_TRIGGERS: dict[str, list[str]] = {
    # Agents analyse
    "promethee": ["C4", "C5"],               # contre-analyse : C4/C5 seulement
    "dionysos":  ["C4", "C5", "exploration"], # créativité : C4/C5 ou pattern exploration
    "demeter":   ["C3", "C4", "C5"],         # collecte contexte : planification C3+
    # Agents cadrage / validation
    "themis":    ["C4", "C5"],               # validation légale : C4/C5 uniquement
    "ares":      ["C3", "C4", "C5"],         # sécurité systémique : veto C3+
    # Agents continuité
    "hestia":    ["C3", "C4", "C5"],         # mémoire projet : pas C1/C2
    "mnemosyne": ["C4", "C5"],               # mémoire agence : C4/C5 seulement
    "hades":     ["C4", "C5"],               # mémoire longue durée : criticité haute
    # Agents communication
    "iris":      ["C4", "C5"],               # correspondance formelle : C4/C5
    "aphrodite": [],                         # styliste production — jamais décisionnel auto
    # Agents production
    "dedale":    ["C4", "C5"],               # production dossiers complets : C4/C5
    "hephaistos":["C1", "C2", "C3", "C4", "C5"],  # diagrammes : toujours activable
    # Agents système
    "poseidon":  ["C4", "C5"],               # distribution charge : systèmes complexes
    # Meta-agents Pantheon OS
    "hera":      ["C3", "C4", "C5"],         # supervision : post-synthèse C3+
    "artemis":   ["C1", "C2", "C3", "C4", "C5"],  # filtrage : sur demande Zeus (trim)
    "kairos":    ["C1", "C2", "C3", "C4", "C5"],  # synthèse : toujours activable
    # Agents v2 — incertitude, édition, clarification
    "hecate":        ["C1", "C2", "C3", "C4", "C5"],  # analyse incertitude : always-on
    "metis":         ["C2", "C3", "C4", "C5"],         # révision stylistique
    "iris_clarifier":["C1", "C2", "C3", "C4", "C5"],  # reformulation questions
}

# Routing automatique selon criticité
CRITICITE_ROUTING = {
    "C1": {"hitl": False, "zeus": False, "veto_check": False},
    "C2": {"hitl": False, "zeus": False, "veto_check": False},
    "C3": {"hitl": False, "zeus": True, "veto_check": True},
    "C4": {"hitl": True, "zeus": True, "veto_check": True},
    "C5": {"hitl": True, "zeus": True, "veto_check": True},
}
VALID_AGENTS = {
    # Meta
    "hermes",          # router
    "hera",            # supervisor
    "artemis",         # filter
    "kairos",          # synthesizer
    "apollon",         # validator (meta)
    # Analyse
    "athena",          # planner
    "argos",           # extractor
    "promethee",       # challenger
    "dionysos",        # creative
    "demeter",         # collector
    "hecate",          # uncertainty_resolver
    # Cadrage / Validation
    "themis",          # legal_validator (veto)
    "chronos",         # time_planner
    # Système
    "ares",            # security_guard (veto)
    "poseidon",        # distributor
    # Continuité
    "hestia",          # memory_project
    "mnemosyne",       # memory_agency
    "hades",           # memory_longterm
    # Communication
    "iris",            # communicator
    "iris_clarifier",  # clarifier
    "metis",           # editor
    # Production
    "dedale",          # builder
    "hephaistos",      # diagram_builder
    "aphrodite",       # stylist
}


# ── OrchestraState ──────────────────────────────────────────────────


class OrchestraState(TypedDict):
    instruction: str
    affaire_id: str
    user_id: Optional[str]
    initial_agents: list[str]

    # Phase 1 (legacy — plus écrit par le graphe, conservé pour la compatibilité DB)
    agent_plans: dict  # toujours {} depuis la suppression du nœud plan_agents

    # Résumés statiques des agents (depuis SOUL.md, 0 appel LLM)
    agent_summaries: dict  # {agent_name: "titre — description courte"}

    # Phase 2 — Zeus plan
    zeus_reasoning: str
    subtasks: list  # [{id, pattern, agents, judge?, instruction, depends_on}]
    assignments: list  # [{agent, instruction, priority}] — compat + complements
    synthesis_agent: str

    # Phase 3 — exécution
    agent_results: dict  # {agent_name: result_text} — vue plate pour veto/synthèse
    subtask_results: dict  # {task_id: {agent_name: result_text}} — vue structurée
    agent_run_ids: list  # UUIDs des AgentRun créés

    # Phase 3b — compléments (optionnel, une fois)
    complement_done: bool

    # Phase 4
    final_answer: str

    # Routing interne Zeus
    verdict: str  # "complete" | "needs_complement" | "veto"

    # Criticité C1-C5
    criticite: str  # "C1" | "C2" | "C3" | "C4" | "C5"

    # Veto (Thémis / Héphaïstos) — structured_veto via GuardsService
    veto_agent: str
    veto_motif: str
    veto_severity: str
    veto_condition_levee: str

    # Human-in-the-loop
    hitl_enabled: bool
    hitl_approval: dict  # {approved, feedback, modified_assignments}

    # Scoring décisionnel (C4/C5)
    score_id: str  # UUID du DecisionScore créé
    score_verdict: str  # "robuste" | "acceptable" | "fragile" | "dangereux"
    score_total: int  # total_final /100

    # Mémoires écrites
    memories_written: int
    wiki_page_id: str  # UUID de la page wiki promue (C4/C5)

    # Preprocessing Hermès (nœud preprocess)
    preprocessed_input: dict  # PreprocessedInput.model_dump()

    # Gate Precheck (nœud workflow_precheck)
    precheck_verdict: str  # approved | trim | upgrade | clarification | blocked
    precheck_reasoning: str

    # Mémoire fonctionnelle (M3) — Redis TTL, session
    thread_id: str  # clé de session (checkpoint_thread_id ou externe)

    # Identifiant de l'OrchestraRun en cours (disponible dès le début, passé depuis service.py)
    orchestra_run_id: str  # UUID de l'OrchestraRun — utilisé par write_memories pour lier les décisions

    # ── Améliorations architecturales ───────────────────────────────────

    # Score multi-critères global (amélioration 1 — tous les runs)
    run_score: dict  # {quality: 0-100, coherence: 0-100, confidence: 0-100, risk: 0-100}

    # Supervision HERA (amélioration 4 — séparation exécution/supervision)
    hera_verdict: str  # "aligned" | "misaligned" | "degraded"
    hera_feedback: str

    # Fallback (amélioration 2 — 0=none | 1=simplified | 2=strategy_changed | 3=degraded)
    fallback_level: int


# ── Helpers LLM ────────────────────────────────────────────────────


@functools.lru_cache(maxsize=1)
def _get_domain_context() -> str:
    """Charge le contexte domaine depuis agents/domains/{DOMAIN}.yaml (LRU cached)."""
    try:
        import yaml  # type: ignore[import]
    except ImportError:
        return ""
    domain = getattr(settings, "DOMAIN", "btp")
    overlay_path = AGENTS_DIR / "domains" / f"{domain}.yaml"
    if not overlay_path.exists():
        return ""
    try:
        data = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
        return data.get("context_injection", "") if isinstance(data, dict) else ""
    except Exception:
        return ""


def _resolve_soul_path(agent_name: str) -> Path | None:
    """Résout le chemin SOUL.md — core/ en priorité, agents/ en fallback."""
    name = agent_name.lower()
    core_path = CORE_DIR / name / "SOUL.md"
    if core_path.exists():
        return core_path
    agents_path = AGENTS_DIR / name / "SOUL.md"
    if agents_path.exists():
        return agents_path
    return None


@functools.lru_cache(maxsize=22)
def _get_soul(agent_name: str) -> str:
    """Charge le SOUL.md d'un agent + contexte domaine (LRU, process lifetime). Max 3000 chars."""
    soul_path = _resolve_soul_path(agent_name)
    if soul_path:
        content = soul_path.read_text(encoding="utf-8")
        soul = content[:3000] if len(content) > 3000 else content
    else:
        soul = f"Tu es {agent_name}, expert ARCEUS. Réponds toujours en JSON strict."
    domain_ctx = _get_domain_context()
    if domain_ctx:
        soul = f"{soul}\n\n{domain_ctx}"
    return soul


@functools.lru_cache(maxsize=1)
def _zeus_system() -> str:
    """Charge SOUL.md de Zeus. Mis en cache (process lifetime)."""
    soul_path = AGENTS_DIR / "zeus" / "SOUL.md"
    return (
        soul_path.read_text(encoding="utf-8")
        if soul_path.exists()
        else "Tu es Zeus, orchestrateur. Réponds toujours en JSON strict."
    )


def _parse_json_response(content: str) -> dict:
    """Parse JSON robuste — extraction par accolades équilibrées."""
    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    depth = 0
    start: int | None = None
    for i, ch in enumerate(content):
        if ch == "{":
            if start is None:
                start = i
            depth += 1
        elif ch == "}" and start is not None:
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(content[start : i + 1])
                except json.JSONDecodeError:
                    start = None

    return {"reasoning": content[:300], "assignments": [], "synthesis_agent": "mnemosyne"}


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=8),
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
async def _llm_call(system: str, user: str) -> str:
    from core.circuit_breaker import llm_breaker

    llm_breaker.check()

    try:
        response = await asyncio.wait_for(
            LlmService._get_client().chat.completions.create(
                model=settings.effective_llm_model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=0.2,
                max_tokens=2048,
            ),
            timeout=_LLM_TIMEOUT,
        )
        llm_breaker.record_success()
        return response.choices[0].message.content or ""
    except Exception:
        llm_breaker.record_failure()
        raise


@functools.lru_cache(maxsize=32)
def _get_agent_summary(agent_name: str) -> str:
    """Extrait une description statique de l'agent depuis son SOUL.md.

    Retourne le titre + le premier paragraphe du rôle, tronqué à 280 chars.
    Mis en cache pour la durée du process — aucun appel LLM.
    """
    name = agent_name.lower()
    soul_path = _resolve_soul_path(name)
    if not soul_path:
        return f"{name} — agent spécialisé ARCEUS"

    text = soul_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = name
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    role_text = ""
    in_role = False
    for line in lines:
        if re.match(r"^##\s+R[ôo]le\b", line, re.IGNORECASE):
            in_role = True
            continue
        if in_role:
            stripped = line.strip()
            if stripped.startswith("##"):
                break
            if stripped and not stripped.startswith("#"):
                role_text += " " + stripped
                if len(role_text) > 280:
                    break

    role_text = role_text.strip()
    if len(role_text) > 280:
        truncated = role_text[:280].rsplit(".", 1)
        role_text = truncated[0] + "." if len(truncated) > 1 else role_text[:280]

    return f"{title} — {role_text}" if role_text else title


async def _run_agent_isolated(
    agent: str,
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    thread_id: str = "",
):
    """Exécute un agent avec sa propre session DB."""
    async with AsyncSessionLocal() as session:
        run = await run_agent(
            db=session,
            instruction=instruction,
            affaire_id=affaire_id,
            user_id=user_id,
            agent_name=agent,
            thread_id=thread_id,
        )
        return agent, run.result or "", str(run.id)
