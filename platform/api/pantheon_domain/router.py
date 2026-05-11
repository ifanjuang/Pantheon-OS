"""HTTP routes for the Pantheon OS Domain Operating Layer."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from .contracts import (
    AgentDefinition,
    ApprovalClassification,
    ApprovalClassificationRequest,
    DomainLayerSnapshot,
    GovernanceDocument,
    KnowledgeCollectionDefinition,
    LegacyComponentDefinition,
    MemoryStoreDefinition,
    SkillDefinition,
    WorkflowDefinition,
)
from .governance_docs import (
    find_governance_entry,
    load_governance_document,
    load_governance_index,
)
from .repository import DomainLayerRepository

router = APIRouter(prefix="/domain", tags=["pantheon-domain"])
repository = DomainLayerRepository()


def _load_indexed_doc(relative_path: str) -> GovernanceDocument:
    entry = find_governance_entry(relative_path)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"{relative_path} not in governance index")
    return load_governance_document(entry)


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


@router.get("/role-signals", response_model=GovernanceDocument)
def get_role_signals() -> GovernanceDocument:
    """Expose ROLE_SIGNALS.md as the canonical role-signal doctrine."""
    return _load_indexed_doc("docs/governance/ROLE_SIGNALS.md")


@router.get("/role-signal-profiles", response_model=GovernanceDocument)
def get_role_signal_profiles() -> GovernanceDocument:
    """Expose ROLE_SIGNAL_PROFILES.md as the canonical addressed-role profile registry."""
    return _load_indexed_doc("docs/governance/ROLE_SIGNAL_PROFILES.md")


@router.get("/routing-foundation", response_model=GovernanceDocument)
def get_routing_foundation() -> GovernanceDocument:
    """Expose ROUTING_FOUNDATION.md as the canonical routing taxonomy."""
    return _load_indexed_doc("docs/governance/ROUTING_FOUNDATION.md")


@router.get("/governance-index", response_model=list[GovernanceDocument])
def get_governance_index(
    include_content: bool = Query(
        default=False,
        description="When true, include each document's full content. False by default to keep the index response bounded; callers should fetch full text via per-document endpoints.",
    ),
) -> list[GovernanceDocument]:
    """Expose the canonical governance document index.

    The index mirrors `docs/governance/README.md`. Each entry carries the
    relative path, the canonical title and the lifecycle status. Content is
    omitted unless `include_content=true` is passed, so the listing stays
    cheap and the per-document endpoints remain the canonical way to fetch
    full Markdown for a single doc.
    """
    return load_governance_index(include_content=include_content)
