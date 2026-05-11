"""Static index of canonical governance documents exposed by the Domain API.

This module is read-only by construction. It maps a stable list of governance
Markdown documents to their canonical paths, titles and lifecycle status, then
exposes a helper that reads file content on demand.

The Domain API surface defined in `router.py` uses this module to expose:

* `GET /domain/role-signals`         → full ROLE_SIGNALS.md
* `GET /domain/role-signal-profiles` → full ROLE_SIGNAL_PROFILES.md
* `GET /domain/routing-foundation`   → full ROUTING_FOUNDATION.md
* `GET /domain/governance-index`     → list of indexed governance documents

Doctrine boundary:

* every endpoint is HTTP GET;
* no POST, no PUT, no PATCH, no DELETE;
* no network call, no Hermes call, no OpenWebUI runtime mutation;
* no skill activation, no workflow execution, no memory promotion;
* no scheduler, no agent loop, no message bus.

The list of governance documents intentionally mirrors
`docs/governance/README.md`. Adding or removing a document requires updating
this index and `docs/governance/README.md` in the same PR.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .contracts import ComponentStatus, GovernanceDocument


@dataclass(frozen=True)
class GovernanceEntry:
    """Static metadata for one canonical governance document."""

    path: str  # relative to repo root, e.g. "docs/governance/ROLE_SIGNALS.md"
    title: str
    status: ComponentStatus = ComponentStatus.ACTIVE


# Resolution rule: this file lives at
#   platform/api/pantheon_domain/governance_docs.py
# The repo root is therefore three parents up.
REPO_ROOT: Path = Path(__file__).resolve().parents[3]


# The ordered list below mirrors `docs/governance/README.md`. The index is
# the canonical view exposed by `/domain/governance-index`.
GOVERNANCE_INDEX: tuple[GovernanceEntry, ...] = (
    GovernanceEntry("docs/governance/README.md", "Governance README", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/STATUS.md", "Project Status", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/ROADMAP.md", "Roadmap", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/DEVELOPMENT_PHASES.md", "Development Phases", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/ARCHITECTURE.md", "Architecture", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/HERMES_EXECUTION_MODEL.md", "Hermes Execution Model", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/HERMES_CAPABILITY_MAP.md", "Hermes Capability Map", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/GOVERNANCE_METHODS.md", "Governance Methods", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/MEMORY_STORAGE_MODEL.md", "Memory Storage Model", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/OPENWEBUI_PLUGIN_POLICY.md", "OpenWebUI Plugin Policy", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/MODULES.md", "Modules", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/AGENTS.md", "Agents", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/REQUEST_ORCHESTRATION.md", "Request Orchestration", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/ROUTING_FOUNDATION.md", "Routing Foundation", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/ROLE_SIGNALS.md", "Role Signals", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/ROLE_SIGNAL_PROFILES.md", "Role Signal Profiles", ComponentStatus.ACTIVE),
    GovernanceEntry(
        "docs/governance/DELIVERABLE_OPERATING_MODEL.md",
        "Deliverable Operating Model",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry(
        "docs/governance/GOVERNANCE_ENHANCEMENT_BACKLOG.md",
        "Governance Enhancement Backlog",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry("docs/governance/MEMORY.md", "Memory", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/APPROVALS.md", "Approvals", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/TASK_CONTRACTS.md", "Task Contracts", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/TASK_CONTRACT_REVISIONS.md", "Task Contract Revisions", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/EVIDENCE_PACK.md", "Evidence Pack", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/EPISTEMIC_CONTROL.md", "Epistemic Control", ComponentStatus.ACTIVE),
    GovernanceEntry(
        "docs/governance/EPISTEMIC_CONTROL_PROPAGATION.md",
        "Epistemic Control Propagation",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry("docs/governance/EVALUATION.md", "Evaluation", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/HERMES_INTEGRATION.md", "Hermes Integration", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/OPENWEBUI_INTEGRATION.md", "OpenWebUI Integration", ComponentStatus.ACTIVE),
    GovernanceEntry(
        "docs/governance/OPENWEBUI_DOMAIN_MAPPING.md",
        "OpenWebUI Domain Mapping",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry("docs/governance/MODEL_ROUTING_POLICY.md", "Model Routing Policy", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/EXTERNAL_TOOLS_POLICY.md", "External Tools Policy", ComponentStatus.ACTIVE),
    GovernanceEntry(
        "docs/governance/EXTERNAL_RUNTIME_OPTIONS.md",
        "External Runtime Options",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry(
        "docs/governance/EXTERNAL_RUNTIME_REVIEW_TEMPLATE.md",
        "External Runtime Review Template",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry(
        "docs/governance/EXTERNAL_RUNTIME_OPTION_REVIEWS_KANWAS_AKS_AGENTRQ_OPENCODE_SIX_HATS.md",
        "External Runtime Option Reviews (Kanwas/AKS/AgentRQ/opencode/six-hats)",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry(
        "docs/governance/EXTERNAL_AI_OPTION_REVIEWS.md",
        "External AI Option Reviews",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry(
        "docs/governance/EXTERNAL_HERMES_UI_OPTION_REVIEWS.md",
        "External Hermes UI Option Reviews",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry(
        "docs/governance/EXTERNAL_ECOSYSTEM_REVIEWS.md",
        "External Ecosystem Reviews",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry(
        "docs/governance/EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md",
        "External Memory Runtime Reviews (OpenConcho/Honcho)",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry("docs/governance/EXECUTION_DISCIPLINE.md", "Execution Discipline", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/KNOWLEDGE_TAXONOMY.md", "Knowledge Taxonomy", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/CODE_AUDIT_POST_PIVOT.md", "Code Audit Post-Pivot", ComponentStatus.ACTIVE),
    GovernanceEntry(
        "docs/governance/PRE_REFACTOR_ARCHITECTURE_FINDINGS.md",
        "Pre-Refactor Architecture Findings",
        ComponentStatus.ACTIVE,
    ),
    GovernanceEntry("docs/governance/RUN_GRAPH.md", "Run Graph", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/WORKFLOW_SCHEMA.md", "Workflow Schema", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/WORKFLOW_ADAPTATION.md", "Workflow Adaptation", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/SKILL_LIFECYCLE.md", "Skill Lifecycle", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/MEMORY_EVENT_SCHEMA.md", "Memory Event Schema", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/EXTERNAL_WATCHLIST.md", "External Watchlist", ComponentStatus.ACTIVE),
    GovernanceEntry("docs/governance/VERSIONS.md", "Versions", ComponentStatus.ACTIVE),
    GovernanceEntry(
        "docs/governance/AI_LOG.md",
        "AI Log (deprecated pointer)",
        ComponentStatus.LEGACY,
    ),
)


def find_governance_entry(path: str) -> GovernanceEntry | None:
    """Return the indexed entry for `path` (relative to repo root) or `None`."""
    for entry in GOVERNANCE_INDEX:
        if entry.path == path:
            return entry
    return None


def _read_static_file(relative_path: str) -> str:
    """Read a governance file relative to the repo root, returning '' on failure.

    Read-only: this function never writes, never opens for write, never executes
    shell commands and never calls the network.
    """
    try:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def load_governance_document(entry: GovernanceEntry) -> GovernanceDocument:
    """Materialize one `GovernanceDocument` from a static index entry."""
    return GovernanceDocument(
        path=entry.path,
        title=entry.title,
        status=entry.status,
        content=_read_static_file(entry.path),
        last_known_static_source=entry.path,
    )


def load_governance_index(*, include_content: bool = False) -> list[GovernanceDocument]:
    """Materialize the full governance index.

    By default, content is omitted (empty string) to keep the response bounded.
    Callers wanting full content of one document should call the per-document
    endpoint (`/domain/role-signals`, `/domain/role-signal-profiles`,
    `/domain/routing-foundation`) or set `include_content=True`.
    """
    docs: list[GovernanceDocument] = []
    for entry in GOVERNANCE_INDEX:
        content = _read_static_file(entry.path) if include_content else ""
        docs.append(
            GovernanceDocument(
                path=entry.path,
                title=entry.title,
                status=entry.status,
                content=content,
                last_known_static_source=entry.path,
            )
        )
    return docs
