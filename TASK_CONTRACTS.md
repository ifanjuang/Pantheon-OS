# TASK CONTRACTS — Pantheon OS

> Reference document for executable task contracts delegated to Hermes or orchestrated by Pantheon workflows.

---

# 1. Purpose

A task contract defines the safe execution frame for a bounded task.

It tells Hermes, Pantheon and OpenWebUI:

- what the task is;
- what inputs are allowed;
- what outputs are expected;
- what tools may be used;
- what tools are forbidden;
- what approval level is required;
- what evidence must be returned;
- whether memory can be affected.

Rule:

```text
No governed task should execute without a task contract when it can mutate files, use tools, affect memory, create candidates or expose external risk.
```

---

# 2. Minimal schema

Each task contract must define:

| Field | Required | Purpose |
|---|---:|---|
| `id` | yes | Stable task identifier |
| `domain` | yes | `general`, `architecture_fr`, `software` or other validated domain |
| `purpose` | yes | Short task objective |
| `mode` | yes | `read_only`, `suggest`, `candidate_patch`, `review`, `execute_with_approval` |
| `inputs` | yes | Required and optional inputs |
| `outputs` | yes | Expected outputs |
| `allowed_tools` | yes | Tools or tool classes allowed |
| `forbidden_tools` | yes | Tools or tool classes forbidden |
| `approval_level` | yes | C0-C5 from `APPROVALS.md` |
| `agents` | yes | Agents involved in review/orchestration |
| `skills` | yes | Skills expected or allowed |
| `memory_impact` | yes | `none`, `candidate_only`, `promotion_review` |
| `evidence_required` | yes | Whether an Evidence Pack is mandatory |

---

# 3. Generic YAML shape

```yaml
task_contract:
  id: example_task
  domain: general
  purpose: "Explain what the task does."
  mode: read_only
  inputs:
    required: []
    optional: []
  outputs:
    required: []
  allowed_tools: []
  forbidden_tools: []
  approval_level: C0
  agents: []
  skills: []
  memory_impact: none
  evidence_required: true
```

---

# 4. Initial task contracts

## 4.1 repo_consistency_audit

```yaml
task_contract:
  id: repo_consistency_audit
  domain: software
  purpose: "Compare reference Markdown files with the current repository state."
  mode: read_only
  inputs:
    required:
      - repository
      - branch
    optional:
      - focus_files
  outputs:
    required:
      - diagnostic
      - inconsistencies
      - documentation_updates_proposed
      - code_updates_proposed_after_documentation
      - evidence_pack
  allowed_tools:
    - read_file
    - search_files
    - git_diff_read
    - test_read
  forbidden_tools:
    - push_main
    - destructive
    - memory_write
    - external_communication
  approval_level: C0
  agents:
    - ZEUS
    - ATHENA
    - THEMIS
    - APOLLO
  skills:
    - repo_md_audit
    - evidence_pack_check
  memory_impact: none
  evidence_required: true
```

## 4.2 quote_vs_cctp_review

```yaml
task_contract:
  id: quote_vs_cctp_review
  domain: architecture_fr
  purpose: "Compare a contractor quote against a CCTP or equivalent technical specification."
  mode: review
  inputs:
    required:
      - quote_document
      - cctp_document
    optional:
      - dpgf_document
      - project_context
  outputs:
    required:
      - matched_items
      - missing_items
      - scope_gaps
      - risk_flags
      - evidence_pack
  allowed_tools:
    - document_read
    - knowledge_search
    - table_extract
  forbidden_tools:
    - external_communication
    - memory_promotion
    - final_contractual_validation
  approval_level: C1
  agents:
    - ZEUS
    - ARGOS
    - HEPHAESTUS
    - DEMETER
    - THEMIS
    - APOLLO
  skills:
    - quote_vs_cctp_consistency
    - contractual_risk_check
    - evidence_pack_check
  memory_impact: candidate_only
  evidence_required: true
```

## 4.3 client_message_review

```yaml
task_contract:
  id: client_message_review
  domain: architecture_fr
  purpose: "Review or draft a client-facing message with risk and responsibility controls."
  mode: suggest
  inputs:
    required:
      - draft_or_intent
    optional:
      - project_context
      - tone
  outputs:
    required:
      - revised_message
      - risk_notes
      - limits
  allowed_tools:
    - text_review
    - knowledge_search
  forbidden_tools:
    - send_email_without_approval
    - external_post_without_approval
  approval_level: C4
  agents:
    - ZEUS
    - THEMIS
    - APOLLO
  skills:
    - client_message_safety
    - approval_risk_check
  memory_impact: none
  evidence_required: true
```

## 4.4 memory_promotion_review

```yaml
task_contract:
  id: memory_promotion_review
  domain: general
  purpose: "Review whether candidate information can become project or system memory."
  mode: review
  inputs:
    required:
      - memory_candidate
    optional:
      - source_documents
  outputs:
    required:
      - decision
      - target_memory_level
      - privacy_check
      - evidence_pack
  allowed_tools:
    - read_candidate
    - source_check
    - privacy_check
  forbidden_tools:
    - auto_promote_memory
    - expose_private_raw_data
  approval_level: C3
  agents:
    - HESTIA
    - MNEMOSYNE
    - THEMIS
    - APOLLO
  skills:
    - memory_promotion_check
    - privacy_check
    - source_check
  memory_impact: promotion_review
  evidence_required: true
```

## 4.5 skill_candidate_review

```yaml
task_contract:
  id: skill_candidate_review
  domain: general
  purpose: "Review a candidate skill before activation or level change."
  mode: review
  inputs:
    required:
      - skill_path
    optional:
      - examples
      - tests
      - updates
  outputs:
    required:
      - review_result
      - blockers
      - approval_level
      - evidence_pack
  allowed_tools:
    - read_file
    - search_files
    - static_review
  forbidden_tools:
    - auto_activate_skill
    - auto_level_up_skill
  approval_level: C3
  agents:
    - ZEUS
    - THEMIS
    - APOLLO
  skills:
    - skill_candidate_review
    - evidence_pack_check
  memory_impact: none
  evidence_required: true
```

## 4.6 legacy_component_audit

```yaml
task_contract:
  id: legacy_component_audit
  domain: software
  purpose: "Classify legacy post-pivot code before keeping, reorienting, archiving or deleting it."
  mode: read_only
  inputs:
    required:
      - component_path
    optional:
      - related_docs
  outputs:
    required:
      - component_status
      - decision_proposed
      - risks
      - next_action
      - evidence_pack
  allowed_tools:
    - read_file
    - search_files
    - dependency_read
  forbidden_tools:
    - delete_file
    - destructive
    - direct_refactor
  approval_level: C0
  agents:
    - ZEUS
    - ATHENA
    - THEMIS
    - APOLLO
  skills:
    - legacy_classification
    - repo_md_audit
  memory_impact: none
  evidence_required: true
```

---

# 5. Final rule

```text
A task contract does not authorize execution by itself.
It defines the frame inside which approval policy can authorize execution.
```
