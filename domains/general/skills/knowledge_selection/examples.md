# Knowledge Selection — Examples

> Fictional examples only. No real project, client, company, address or private conversation data.

---

# 1. Generic governance question

## Input

```text
Explain how Pantheon approvals work.
```

## Selection report

```yaml
knowledge_selection_report:
  domain: general
  decision: select_sources
  selected_sources:
    - source_id: pantheon_approvals
      openwebui_knowledge_base: pantheon_approvals
      source_tier: T0
      reliability_level: R5
      privacy_level: internal
      project_scope: none
      freshness_policy: static
      limitations: []
  rejected_sources: []
  warnings: []
  memory_impact: none
  approval_required: false
```

---

# 2. Architecture drafting aid

## Input

```text
Draft a generic CCTP structure for an architecture project.
```

## Selection report

```yaml
knowledge_selection_report:
  domain: architecture_fr
  decision: select_sources_with_warnings
  selected_sources:
    - source_id: architecture_fr_cctp_models
      source_tier: T4
      reliability_level: R2
      privacy_level: internal
      project_scope: generic
      freshness_policy: periodic_12_months
      limitations:
        - drafting_aid_only
        - not_project_specific
        - not_normative_source
  rejected_sources: []
  warnings:
    - "Templates can structure the answer but cannot validate quantities, prices or contractual obligations."
  memory_impact: none
  approval_required: false
```

---

# 3. Regulatory current check required

## Input

```text
Prepare a position on an ERP fire-safety requirement.
```

## Selection report

```yaml
knowledge_selection_report:
  domain: architecture_fr
  decision: select_sources_with_warnings
  selected_sources:
    - source_id: architecture_fr_sdis_erp
      source_tier: T3
      reliability_level: R3
      privacy_level: internal
      project_scope: generic
      freshness_policy: regulatory_current
      limitations:
        - current_source_check_required
        - authority_or_control_office_review_may_be_required
  rejected_sources:
    - source_id: architecture_fr_cctp_models
      reason: "CCTP model cannot support a current regulatory position."
      policy_ref: source_tier_policy_T4
  warnings:
    - "Regulatory-current source check required before consequential use."
  required_checks:
    - latest_regulatory_source
    - project_context_if_any
    - authority_review_if_consequential
  memory_impact: none
  approval_required: true
```

---

# 4. Private project scope unclear

## Input

```text
Use the documents from another project to answer this one.
```

## Selection report

```yaml
knowledge_selection_report:
  domain: architecture_fr
  decision: request_user_scope_clarification
  selected_sources: []
  rejected_sources:
    - source_id: project_YYYY_NNN_safe_label
      reason: "Cross-project use requires explicit trace, anonymization and approval."
      policy_ref: project_scope_filter
  warnings:
    - cross_project_reuse_blocked
  required_checks:
    - identify_current_project_scope
    - identify_requested_source_project_scope
    - check_anonymization_need
    - approval_before_reuse
  memory_impact: none
  approval_required: true
```

---

# 5. Software repository audit

## Input

```text
Check whether the repository still contains legacy runtime assumptions.
```

## Selection report

```yaml
knowledge_selection_report:
  domain: software
  decision: select_sources
  selected_sources:
    - source_id: software_repo_docs
      source_tier: T0
      reliability_level: R5
      privacy_level: internal
      project_scope: pantheon_repo
      freshness_policy: project_versioned
      limitations:
        - tree_check_required_before_claiming_implementation_state
    - source_id: code_audit_post_pivot
      source_tier: T0
      reliability_level: R5
      privacy_level: internal
      project_scope: pantheon_repo
      freshness_policy: project_versioned
      limitations: []
  rejected_sources: []
  warnings:
    - "Repository tree or code search evidence is required before implementation claims."
  memory_impact: candidate_only
  approval_required: false
```

---

# 6. Fallback to governance only

## Input

```text
Answer without using any project documents.
```

## Selection report

```yaml
knowledge_selection_report:
  domain: general
  decision: fallback_to_governance_only
  selected_sources:
    - source_id: pantheon_governance
      source_tier: T0
      privacy_level: internal
      project_scope: none
  rejected_sources:
    - source_id: project_YYYY_NNN_safe_label
      reason: "User requested no project documents."
      policy_ref: user_forbidden_sources
  warnings:
    - "Answer must remain generic and must not assert project-specific facts."
  memory_impact: none
  approval_required: false
```

---

# 7. Registry validation required

## Input

```text
Use the OpenWebUI Knowledge Base for the relevant architecture references.
```

## Selection report

```yaml
knowledge_selection_report:
  domain: architecture_fr
  decision: request_registry_validation
  selected_sources:
    - source_id: architecture_fr_notices
      openwebui_knowledge_base: architecture_fr_notices
      status: planned
      limitations:
        - live_openwebui_name_not_verified
  rejected_sources: []
  warnings:
    - "Registry is example-only; live Knowledge Base names must be verified before execution."
  required_checks:
    - live_openwebui_collection_exists
    - collection_scope_matches_registry
    - privacy_level_confirmed
  memory_impact: none
  approval_required: false
```
