"""Runtime-facing read-only routes for Pantheon OS."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/runtime", tags=["pantheon-runtime"])


@router.get("/context-pack")
def get_context_pack() -> dict:
    """Return a compact static orientation pack for Hermes and OpenWebUI."""

    return {
        "project": "Pantheon OS",
        "mode": "hermes_backed_domain_layer",
        "status": "planned_interaction_layer_partial_api",
        "doctrine": "Pantheon defines and canonizes. Hermes operates and proposes. OpenWebUI routes, displays and asks for validation.",
        "truth_files": [
            "AI_LOG.md",
            "STATUS.md",
            "README.md",
            "ARCHITECTURE.md",
            "MODULES.md",
            "AGENTS.md",
            "MEMORY.md",
            "ROADMAP.md",
        ],
        "active_rules": [
            "read_ai_log_before_intervention",
            "read_status_before_intervention",
            "docs_before_code",
            "markdown_source_of_truth",
            "no_main_push",
            "branch_required",
            "candidate_before_active",
            "ai_log_required_after_intervention",
            "no_memory_promotion_without_validation",
            "no_skill_level_up_without_review",
        ],
        "domain_packages": [
            "domains/general",
            "domains/architecture_fr",
            "domains/software",
        ],
        "memory_levels": [
            "session",
            "candidates",
            "project",
            "system",
        ],
        "knowledge_rules": [
            "documents_are_knowledge_not_memory",
            "validated_facts_become_memory_candidates",
            "no_cross_project_mixing_without_approval",
            "knowledge_selection_required_for_ambiguous_requests",
        ],
        "planned_components": [
            "OpenWebUI Router Pipe",
            "OpenWebUI Actions",
            "Hermes pantheon-os local skill",
            "ConsultationRequest and ConsultationResult",
            "Evidence Pack",
            "Run Graph",
            "Knowledge Registry",
            "Project Context Resolution",
            "Notion candidate sync policy",
        ],
        "recommended_entrypoint": "Hermes Pantheon Operator",
        "limitations": [
            "static_context_pack",
            "read_only_endpoint",
            "does_not_replace_reference_markdowns",
            "does_not_prove_capability_is_implemented",
        ],
    }
