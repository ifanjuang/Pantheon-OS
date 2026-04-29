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
- whether memory can be affected;
- whether fallback is allowed;
- whether remediation may propose a patch candidate.

Rule:

```text
No governed task should execute without a task contract when it can mutate files, use tools, affect memory, create candidates, process private documents or expose external risk.
```

---

# 2. References

Task contracts must follow:

```text
APPROVALS.md
EVIDENCE_PACK.md
EXTERNAL_TOOLS_POLICY.md
HERMES_INTEGRATION.md
KNOWLEDGE_TAXONOMY.md
MEMORY.md
```

A task contract defines a frame. It does not authorize execution by itself.

---

# 3. Minimal schema

Each task contract must define:

| Field | Required | Purpose |
|---|---:|---|
| `id` | yes | Stable task identifier |
| `domain` | yes | `general`, `architecture_fr`, `software` or other validated domain |
| `purpose` | yes | Short task objective |
| `mode` | yes | `read_only`, `suggest`, `candidate_output`, `candidate_patch`, `review`, `execute_with_approval` |
| `inputs` | yes | Required and optional inputs |
| `outputs` | yes | Expected outputs |
| `allowed_tools` | yes | Tools or tool classes allowed |
| `forbidden_tools` | yes | Tools or tool classes forbidden |
| `approval_level` | yes | C0-C5 from `APPROVALS.md` |
| `agents` | yes | Agents involved in review/orchestration |
| `skills` | yes | Skills expected or allowed |
| `memory_impact` | yes | `none`, `candidate_only`, `promotion_review` |
| `evidence_required` | yes | Whether an Evidence Pack is mandatory |
| `fallback_policy` | yes | Retry and alternative-tool rules |
| `remediation_policy` | yes | Patch candidate and issue-correction rules |

---

# 4. Generic YAML shape

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
  fallback_policy:
    retry_allowed: false
    alternative_tool_allowed: false
    max_retries: 0
    require_approval_if_risk_increases: true
    forbidden_fallbacks:
      - unallowlisted_tool
      - destructive_action
      - external_send
      - secret_access
      - docker_socket
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: true
    require_evidence_pack: true
    require_approval_if:
      - file_mutation
      - workflow_change
      - skill_change
      - tool_policy_change
      - memory_change
      - external_action
```

---

# 5. Global fallback policy

Fallback is allowed only inside the contract.

Allowed fallback conditions:

- same intent;
- same or lower risk;
- same or explicitly allowed tool class;
- no increase in data exposure;
- Evidence Pack records the failed attempt;
- task contract allows retry or alternative tool.

Forbidden fallback conditions:

- unallowlisted tool;
- destructive action;
- external send;
- secret access;
- Docker socket;
- memory write;
- plugin installation;
- remote MCP server not audited;
- bypassing a blocked policy.

Rule:

```text
Fallback cannot bypass approval, allowlist, privacy, memory policy or tool policy.
```

---

# 6. Global remediation policy

A remediation candidate lane may be opened when a task fails, blocks or reveals an inconsistency.

It may:

- analyze the issue;
- identify affected component;
- propose a correction;
- prepare a patch candidate;
- propose tests;
- propose rollback;
- generate Evidence Pack.

It must not:

- apply the fix automatically;
- bypass approval;
- mutate validated memory;
- activate skills;
- change workflows;
- alter policies;
- modify runtime configuration;
- access secrets;
- use Docker socket.

Rule:

```text
Detect → document → propose → validate → apply.
```

---

# 7. Initial non-PDF task contracts

## 7.1 repo_consistency_audit

```yaml
task_contract:
  id: repo_consistency_audit
  domain: software
  purpose: "Compare reference Markdown files with the current repository state."
  mode: read_only
  inputs:
    required: [repository, branch]
    optional: [focus_files]
  outputs:
    required:
      - diagnostic
      - inconsistencies
      - documentation_updates_proposed
      - code_updates_proposed_after_documentation
      - evidence_pack
  allowed_tools: [read_file, search_files, git_diff_read, test_read]
  forbidden_tools: [push_main, destructive, memory_write, external_communication]
  approval_level: C0
  agents: [ZEUS, ATHENA, THEMIS, APOLLO]
  skills: [repo_md_audit, evidence_pack_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [unallowlisted_tool, destructive_action, external_send, secret_access, docker_socket]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: true
    require_evidence_pack: true
    require_approval_if: [file_mutation, workflow_change, skill_change, tool_policy_change, memory_change, external_action]
```

## 7.2 quote_vs_cctp_review

```yaml
task_contract:
  id: quote_vs_cctp_review
  domain: architecture_fr
  purpose: "Compare a contractor quote against a CCTP or equivalent technical specification."
  mode: review
  inputs:
    required: [quote_document, cctp_document]
    optional: [dpgf_document, project_context]
  outputs:
    required: [matched_items, missing_items, scope_gaps, risk_flags, evidence_pack]
  allowed_tools: [document_read, knowledge_search, table_extract]
  forbidden_tools: [external_communication, memory_promotion, final_contractual_validation]
  approval_level: C1
  agents: [ZEUS, ARGOS, HEPHAESTUS, DEMETER, THEMIS, APOLLO]
  skills: [quote_vs_cctp_consistency, contractual_risk_check, evidence_pack_check]
  memory_impact: candidate_only
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [cross_project_knowledge, external_send, memory_write, unallowlisted_tool]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: true
    require_evidence_pack: true
    require_approval_if: [skill_change, workflow_change, memory_change, external_action]
```

## 7.3 client_message_review

```yaml
task_contract:
  id: client_message_review
  domain: architecture_fr
  purpose: "Review or draft a client-facing message with risk and responsibility controls."
  mode: suggest
  inputs:
    required: [draft_or_intent]
    optional: [project_context, tone]
  outputs:
    required: [revised_message, risk_notes, limits]
  allowed_tools: [text_review, knowledge_search]
  forbidden_tools: [send_email_without_approval, external_post_without_approval]
  approval_level: C4
  agents: [ZEUS, THEMIS, APOLLO, IRIS]
  skills: [client_message_safety, approval_risk_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [external_send, memory_write, unallowlisted_tool]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [external_action, memory_change]
```

## 7.4 memory_promotion_review

```yaml
task_contract:
  id: memory_promotion_review
  domain: general
  purpose: "Review whether candidate information can become project or system memory."
  mode: review
  inputs:
    required: [memory_candidate]
    optional: [source_documents]
  outputs:
    required: [decision, target_memory_level, privacy_check, evidence_pack]
  allowed_tools: [read_candidate, source_check, privacy_check]
  forbidden_tools: [auto_promote_memory, expose_private_raw_data]
  approval_level: C3
  agents: [HESTIA, MNEMOSYNE, THEMIS, APOLLO]
  skills: [memory_promotion_check, privacy_check, source_check]
  memory_impact: promotion_review
  evidence_required: true
  fallback_policy:
    retry_allowed: false
    alternative_tool_allowed: false
    max_retries: 0
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [memory_write, unallowlisted_tool, external_send, secret_access]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [memory_change, policy_change]
```

## 7.5 skill_candidate_review

```yaml
task_contract:
  id: skill_candidate_review
  domain: general
  purpose: "Review a candidate skill before activation or level change."
  mode: review
  inputs:
    required: [skill_path]
    optional: [examples, tests, updates]
  outputs:
    required: [review_result, blockers, approval_level, evidence_pack]
  allowed_tools: [read_file, search_files, static_review]
  forbidden_tools: [auto_activate_skill, auto_level_up_skill]
  approval_level: C3
  agents: [ZEUS, THEMIS, APOLLO]
  skills: [skill_candidate_review, evidence_pack_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [auto_activate_skill, memory_write, external_send]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: true
    require_evidence_pack: true
    require_approval_if: [file_mutation, skill_change, policy_change]
```

## 7.6 legacy_component_audit

```yaml
task_contract:
  id: legacy_component_audit
  domain: software
  purpose: "Classify legacy post-pivot code before keeping, reorienting, archiving or deleting it."
  mode: read_only
  inputs:
    required: [component_path]
    optional: [related_docs]
  outputs:
    required: [component_status, decision_proposed, risks, next_action, evidence_pack]
  allowed_tools: [read_file, search_files, dependency_read]
  forbidden_tools: [delete_file, destructive, direct_refactor]
  approval_level: C0
  agents: [ZEUS, ATHENA, THEMIS, APOLLO]
  skills: [legacy_classification, repo_md_audit]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [delete_file, destructive_action, direct_refactor, secret_access, docker_socket]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: true
    require_evidence_pack: true
    require_approval_if: [file_mutation, runtime_config_change, workflow_change, skill_change]
```

---

# 8. PDF task contracts

PDF tasks are governed external-tool tasks. They may use Stirling-PDF only when `EXTERNAL_TOOLS_POLICY.md` allows it.

Global PDF rules:

```text
Always work on a copy.
Never overwrite the source PDF.
Never commit real documents to the repository.
Knowledge ingestion requires Evidence Pack and approval.
```

## 8.1 pdf_info_check

```yaml
task_contract:
  id: pdf_info_check
  domain: general
  purpose: "Read basic PDF information before any transformation."
  mode: read_only
  inputs:
    required: [source_pdf]
    optional: []
  outputs:
    required: [page_count, file_size, metadata_summary, evidence_pack]
  allowed_tools: [stirling_pdf_info, pdf_metadata_read]
  forbidden_tools: [overwrite_source_file, delete_source_file, external_send, knowledge_ingestion]
  approval_level: C0
  agents: [ARGOS, THEMIS]
  skills: [pdf_metadata_check, evidence_pack_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [unallowlisted_tool, destructive_action, external_send, secret_access]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [tool_policy_change]
```

## 8.2 pdf_metadata_check

```yaml
task_contract:
  id: pdf_metadata_check
  domain: general
  purpose: "Check PDF metadata for privacy, authorship or source leakage before reuse."
  mode: review
  inputs:
    required: [source_pdf]
    optional: [intended_use]
  outputs:
    required: [metadata_findings, privacy_flags, evidence_pack]
  allowed_tools: [pdf_metadata_read, stirling_pdf_info]
  forbidden_tools: [metadata_write, overwrite_source_file, external_send]
  approval_level: C0_or_C1
  agents: [ARGOS, THEMIS, APOLLO]
  skills: [pdf_metadata_check, privacy_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [unallowlisted_tool, metadata_write, external_send]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [file_mutation, tool_policy_change]
```

## 8.3 pdf_text_layer_check

```yaml
task_contract:
  id: pdf_text_layer_check
  domain: general
  purpose: "Detect whether a PDF has usable selectable text or requires OCR."
  mode: read_only
  inputs:
    required: [source_pdf]
    optional: []
  outputs:
    required: [text_layer_status, scan_likelihood, ocr_recommendation, evidence_pack]
  allowed_tools: [pdf_text_probe, stirling_pdf_info]
  forbidden_tools: [ocr_without_followup_contract, overwrite_source_file, external_send]
  approval_level: C0
  agents: [ARGOS, APOLLO]
  skills: [pdf_text_layer_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [ocr_without_followup_contract, unallowlisted_tool]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [tool_policy_change]
```

## 8.4 pdf_scanned_document_detect

```yaml
task_contract:
  id: pdf_scanned_document_detect
  domain: general
  purpose: "Classify a PDF as scanned, mixed or text-native before OCR or Knowledge ingestion."
  mode: read_only
  inputs:
    required: [source_pdf]
    optional: []
  outputs:
    required: [document_scan_status, confidence, recommended_next_task, evidence_pack]
  allowed_tools: [pdf_text_probe, pdf_info_check]
  forbidden_tools: [ocr_without_followup_contract, overwrite_source_file]
  approval_level: C0
  agents: [ARGOS, APOLLO]
  skills: [pdf_text_layer_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [unallowlisted_tool, file_mutation]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [tool_policy_change]
```

## 8.5 pdf_ocr_prepare

```yaml
task_contract:
  id: pdf_ocr_prepare
  domain: general
  purpose: "Prepare an OCR copy of a scanned PDF for analysis or Knowledge ingestion."
  mode: candidate_output
  inputs:
    required: [source_pdf]
    optional: [target_folder, ocr_language]
  outputs:
    required: [ocr_pdf_copy, pdf_info, evidence_pack]
  allowed_tools: [stirling_pdf_info, stirling_ocr, stirling_compress]
  forbidden_tools: [delete_source_file, overwrite_source_file, external_send, upload_to_public_repo]
  approval_level: C2_or_C3
  agents: [ARGOS, THEMIS, APOLLO]
  skills: [pdf_ocr_prepare, pdf_metadata_check, evidence_pack_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [unallowlisted_tool, overwrite_source_file, delete_source_file, external_send, secret_access]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: true
    require_evidence_pack: true
    require_approval_if: [file_mutation, tool_policy_change, workflow_change]
```

## 8.6 pdf_sanitize_before_knowledge

```yaml
task_contract:
  id: pdf_sanitize_before_knowledge
  domain: general
  purpose: "Prepare a sanitized working copy before OpenWebUI Knowledge ingestion."
  mode: review
  inputs:
    required: [source_pdf, intended_knowledge_collection]
    optional: [redaction_requirements]
  outputs:
    required: [sanitized_pdf_copy, privacy_findings, ingestion_readiness, evidence_pack]
  allowed_tools: [stirling_pdf_info, stirling_redact, stirling_metadata_remove, stirling_compress]
  forbidden_tools: [overwrite_source_file, delete_source_file, external_send, direct_knowledge_ingestion_without_approval]
  approval_level: C3_or_C4
  agents: [ARGOS, THEMIS, APOLLO]
  skills: [pdf_sanitize_check, privacy_check, evidence_pack_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: false
    alternative_tool_allowed: false
    max_retries: 0
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [unallowlisted_tool, external_send, memory_write, direct_knowledge_ingestion_without_approval]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: true
    require_evidence_pack: true
    require_approval_if: [file_mutation, tool_policy_change, workflow_change, external_action]
```

## 8.7 pdf_split_project_documents

```yaml
task_contract:
  id: pdf_split_project_documents
  domain: general
  purpose: "Split a PDF bundle into working copies without altering the source."
  mode: candidate_output
  inputs:
    required: [source_pdf, split_rule]
    optional: [target_folder]
  outputs:
    required: [split_pdf_copies, split_manifest, evidence_pack]
  allowed_tools: [stirling_split, stirling_pdf_info]
  forbidden_tools: [overwrite_source_file, delete_source_file, external_send]
  approval_level: C3
  agents: [ARGOS, THEMIS, APOLLO]
  skills: [pdf_pipeline_design, evidence_pack_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [unallowlisted_tool, overwrite_source_file, external_send]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [file_mutation]
```

## 8.8 pdf_merge_export_bundle

```yaml
task_contract:
  id: pdf_merge_export_bundle
  domain: general
  purpose: "Merge prepared PDFs into an export bundle."
  mode: candidate_output
  inputs:
    required: [prepared_pdf_list]
    optional: [bundle_title, target_folder]
  outputs:
    required: [merged_pdf_bundle, bundle_manifest, evidence_pack]
  allowed_tools: [stirling_merge, stirling_pdf_info]
  forbidden_tools: [overwrite_source_file, external_send_without_approval]
  approval_level: C3
  agents: [ARGOS, THEMIS, APOLLO]
  skills: [pdf_pipeline_design, evidence_pack_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [external_send_without_approval, unallowlisted_tool]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [external_action]
```

## 8.9 pdf_compress_for_email

```yaml
task_contract:
  id: pdf_compress_for_email
  domain: general
  purpose: "Compress a PDF copy for possible email transmission."
  mode: candidate_output
  inputs:
    required: [source_pdf]
    optional: [target_size, target_folder]
  outputs:
    required: [compressed_pdf_copy, compression_summary, evidence_pack]
  allowed_tools: [stirling_compress, stirling_pdf_info]
  forbidden_tools: [overwrite_source_file, send_email_without_approval]
  approval_level: C2_or_C4
  agents: [ARGOS, THEMIS, APOLLO]
  skills: [pdf_metadata_check, pdf_pipeline_design, evidence_pack_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [send_email_without_approval, unallowlisted_tool]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [external_action]
```

## 8.10 pdf_redaction_review

```yaml
task_contract:
  id: pdf_redaction_review
  domain: general
  purpose: "Review whether redaction is required and whether a redacted copy is safe to use."
  mode: review
  inputs:
    required: [source_pdf, intended_use]
    optional: [redaction_targets]
  outputs:
    required: [redaction_findings, redaction_recommendation, evidence_pack]
  allowed_tools: [pdf_metadata_read, visual_review, stirling_redact_candidate]
  forbidden_tools: [external_send_without_approval, overwrite_source_file, final_redaction_without_review]
  approval_level: C3_or_C4
  agents: [ARGOS, THEMIS, APOLLO]
  skills: [privacy_check, pdf_sanitize_check, evidence_pack_check]
  memory_impact: none
  evidence_required: true
  fallback_policy:
    retry_allowed: false
    alternative_tool_allowed: false
    max_retries: 0
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [external_send_without_approval, unallowlisted_tool, memory_write]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [external_action, file_mutation]
```

## 8.11 pdf_archive_prepare

```yaml
task_contract:
  id: pdf_archive_prepare
  domain: general
  purpose: "Prepare a PDF copy and manifest for archive without deleting or overwriting sources."
  mode: candidate_output
  inputs:
    required: [source_pdf, archive_context]
    optional: [target_folder]
  outputs:
    required: [archive_copy, archive_manifest, evidence_pack]
  allowed_tools: [stirling_pdf_info, file_copy]
  forbidden_tools: [delete_source_file, overwrite_source_file, external_send]
  approval_level: C3
  agents: [ARGOS, THEMIS, APOLLO]
  skills: [pdf_metadata_check, evidence_pack_check]
  memory_impact: candidate_only
  evidence_required: true
  fallback_policy:
    retry_allowed: true
    alternative_tool_allowed: false
    max_retries: 1
    require_approval_if_risk_increases: true
    forbidden_fallbacks: [delete_source_file, overwrite_source_file, unallowlisted_tool]
  remediation_policy:
    enabled: true
    parallel_analysis_allowed: true
    auto_fix_allowed: false
    patch_candidate_allowed: false
    require_evidence_pack: true
    require_approval_if: [file_mutation, memory_change]
```

---

# 9. Final rule

```text
A task contract does not authorize execution by itself.
It defines the frame inside which approval policy can authorize execution.
```

Fallbacks and remediation candidates are part of the frame, not loopholes around it.
