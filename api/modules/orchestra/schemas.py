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


class ZeusOrchestration(BaseModel):
    reasoning: str
    assignments: list[AgentAssignment]
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
    hitl: bool = False                  # True = pause avant exécution pour validation humaine


class ApprovalRequest(BaseModel):
    approved: bool
    feedback: Optional[str] = None          # commentaire libre
    modified_assignments: Optional[list[dict]] = None  # si l'humain modifie les rôles


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
    hitl_enabled: bool = False
    hitl_payload: Optional[dict] = None
    duration_ms: Optional[int]
