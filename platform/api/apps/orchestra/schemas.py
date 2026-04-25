from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class AgentPlan(BaseModel):
    plan: str
    needs: list[str] = []
    difficulties: list[str] = []
    expected_output: str


class AgentAssignment(BaseModel):
    agent: str
    instruction: str
    priority: int = 1


class Subtask(BaseModel):
    id: str
    pattern: str = "parallel"  # "solo" | "parallel" | "cascade" | "arena"
    agents: list[str]
    judge: str = ""  # agent arbitre (pattern=arena uniquement)
    instruction: str = ""  # instruction spécifique à cette sous-tâche (optionnel)
    depends_on: list[str] = []  # IDs de sous-tâches prérequises


class ZeusOrchestration(BaseModel):
    reasoning: str
    criticite: str = "C2"
    subtasks: list[Subtask] = []
    # Compat ancien format
    assignments: list[AgentAssignment] = []
    synthesis_agent: str = "mnemosyne"


class ZeusJudgement(BaseModel):
    verdict: str  # "complete" | "needs_complement"
    synthesis_instruction: str = ""
    complement_requests: list[AgentAssignment] = []


# ── HTTP ────────────────────────────────────────────────────────────


class OrchestraRequest(BaseModel):
    instruction: str = Field(..., min_length=5)
    affaire_id: UUID
    agents: Optional[list[str]] = None  # None = Zeus choisit parmi tous
    criticite: str = "C2"  # C1-C5, détermine le routing HITL/veto
    hitl: bool = False  # True = pause avant exécution pour validation humaine


class ApprovalRequest(BaseModel):
    approved: bool
    feedback: Optional[str] = None
    modified_assignments: Optional[list[dict]] = None


class AgentResultSummary(BaseModel):
    agent: str
    result: str


class OrchestraResponse(BaseModel):
    run_id: UUID
    status: str
    instruction: str
    initial_agents: list[str]
    zeus_reasoning: Optional[str]
    assignments: list[dict]
    agent_results: dict
    synthesis_agent: Optional[str]
    final_answer: Optional[str]
    # Traçabilité 0012
    subtasks: list[dict] = []
    subtask_results: dict = {}
    veto_agent: Optional[str] = None
    veto_motif: Optional[str] = None
    error_message: Optional[str] = None
    criticite: str = "C2"
    hitl_enabled: bool = False
    hitl_payload: Optional[dict] = None
    duration_ms: Optional[int]
    # Améliorations architecturales 0026
    run_score: Optional[dict] = None  # {quality, coherence, confidence, risk}
    hera_verdict: Optional[str] = None  # aligned | misaligned | degraded
    hera_feedback: Optional[str] = None
    fallback_level: int = 0  # 0=none | 1=simplified | 2=changed | 3=degraded
