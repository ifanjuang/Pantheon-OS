"""HTTP routes for the Pantheon OS Domain Operating Layer."""

from __future__ import annotations

from fastapi import APIRouter

from .contracts import (
    AgentDefinition,
    ApprovalClassification,
    ApprovalClassificationRequest,
    DomainLayerSnapshot,
    KnowledgeCollectionDefinition,
    LegacyComponentDefinition,
    MemoryStoreDefinition,
    SkillDefinition,
    WorkflowDefinition,
)
from .repository import DomainLayerRepository

router = APIRouter(prefix="/domain", tags=["pantheon-domain"])
repository = DomainLayerRepository()


@router.get("/health")
def domain_health() -> dict[str, str]:
    return {
        "status": "ok",
        "mode": "hermes_backed_domain_layer",
        "doctrine": "Pantheon defines. Hermes executes. OpenWebUI exposes and retrieves.",
    }


@router.get("/snapshot", response_model=DomainLayerSnapshot)
def get_snapshot() -> DomainLayerSnapshot:
    return repository.snapshot()


@router.get("/agents", response_model=list[AgentDefinition])
def list_agents() -> list[AgentDefinition]:
    return repository.agents()


@router.get("/skills", response_model=list[SkillDefinition])
def list_skills() -> list[SkillDefinition]:
    return repository.skills()


@router.get("/workflows", response_model=list[WorkflowDefinition])
def list_workflows() -> list[WorkflowDefinition]:
    return repository.workflows()


@router.get("/memory", response_model=list[MemoryStoreDefinition])
def list_memory_stores() -> list[MemoryStoreDefinition]:
    return repository.memory_stores()


@router.get("/knowledge", response_model=list[KnowledgeCollectionDefinition])
def list_knowledge_collections() -> list[KnowledgeCollectionDefinition]:
    return repository.knowledge_collections()


@router.get("/legacy", response_model=list[LegacyComponentDefinition])
def list_legacy_components() -> list[LegacyComponentDefinition]:
    return repository.legacy_components()


@router.post("/approval/classify", response_model=ApprovalClassification)
def classify_approval(request: ApprovalClassificationRequest) -> ApprovalClassification:
    return repository.classify_approval(request)
