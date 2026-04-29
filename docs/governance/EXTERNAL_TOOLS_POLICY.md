# EXTERNAL TOOLS POLICY — Pantheon OS

> Governance reference for external services, plugins, skills, frameworks and automation layers.

---

# 1. Purpose

Pantheon OS may use external tools, but external tools must never become Pantheon’s authority.

Core rule:

```text
Pantheon defines and governs.
Hermes executes under policy.
OpenWebUI exposes the interface and Knowledge.
External tools provide bounded capabilities only.
```

This policy exists because external tools can affect files, memory, network access, secrets, shell access, plugins, cost, autonomy, PDF processing, browser automation or remote services.

No external tool may be integrated, installed, executed in production, or exposed to Hermes/OpenWebUI without classification.

---

# 2. Scope

This policy applies to:

- external services;
- Docker containers;
- OpenWebUI extensions;
- Hermes plugins;
- Hermes community skills;
- MCP servers;
- PDF tools;
- OCR tools;
- workflow frameworks;
- memory frameworks;
- self-evolution systems;
- browser automation;
- remote bridges;
- dashboards;
- code-generation or patch-generation tools.

---

# 3. Initial tools to classify

Initial watchlist:

```text
Stirling-PDF
OpenWebUI extensions
Hermes plugins
Hermes community skills
GBrain
BrainAPI2
AgentScope
Hermes self-evolution
OCRmyPDF
Gotenberg
qpdf
```

Additional tools may be added only through this document or a future machine-readable registry.

---

# 4. Classification schema

Every external tool entry must define:

| Field | Required | Purpose |
|---|---:|---|
| `tool_name` | yes | Human-readable name |
| `repository` | yes | Source repository or official source |
| `license` | yes | Declared license |
| `license_status` | yes | `verified`, `unclear`, `conflicting`, `not_checked` |
| `type` | yes | service, plugin, skill, framework, UI, memory, PDF, OCR, MCP, automation |
| `status` | yes | allowed, test, blocked, rejected, watch |
| `maturity` | yes | production, beta, experimental, unknown |
| `data_classification` | yes | public, internal, project, sensitive, secrets |
| `local_only` | yes | whether it must remain local-only |
| `network_exposure` | yes | none, LAN, internet, unknown |
| `auth_required` | yes | authentication requirement |
| `sandbox_required` | yes | whether sandbox is mandatory |
| `file_access` | yes | none, read, write, delete |
| `network_access` | yes | none, limited, broad, unknown |
| `memory_access` | yes | none, read, candidate, write, unknown |
| `secrets_access` | yes | none, required, forbidden, unknown |
| `shell_access` | yes | none, limited, broad, unknown |
| `side_effects` | yes | possible persistent or external effects |
| `approval_level` | yes | C0-C5 from `APPROVALS.md` |
| `allowed_usage` | yes | authorized Pantheon usage |
| `forbidden_usage` | yes | explicitly forbidden usage |
| `rollback_plan` | yes | removal/revert path |
| `review_frequency` | yes | review cadence |
| `last_reviewed` | yes | last review date or null |
| `default_decision` | yes | default action before explicit approval |

---

# 5. Status values

Allowed status values:

```text
allowed
```

Tool may be used inside defined policy and task contracts.

```text
test
```

Tool may be tested in sandbox only. No production use.

```text
blocked
```

Tool is blocked by default. It may be reconsidered only through explicit review.

```text
rejected
```

Tool is rejected for Pantheon use.

```text
watch
```

Tool is tracked as inspiration or future candidate. No execution.

---

# 6. Default policy

Default classification for unknown tools:

```yaml
status: blocked
approval_level: C5
sandbox_required: true
secrets_access: forbidden
shell_access: forbidden
memory_access: none
network_exposure: none
```

Rule:

```text
Unknown external code is blocked until classified.
```

---

# 7. Approval mapping

External tool actions must follow `APPROVALS.md`.

Baseline mapping:

| Action | Default level |
|---|---:|
| tool documentation review | C0 |
| repository read-only audit | C0 |
| sandbox-only conceptual test | C1/C2 |
| local service install | C3 |
| OpenWebUI plugin install | C3 |
| Hermes plugin install | C3 |
| memory plugin install | C4 |
| autonomy plugin install | C5 |
| secrets access | C5 |
| Docker socket access | C5 |
| external side effect | C4/C5 |
| batch install from GitHub | C5 / blocked |
| remote MCP server | C5 / blocked until audited |

---

# 8. Fallback / retry / alternative execution policy

A fallback cannot bypass policy.

If an action fails, is blocked, or is postponed, Pantheon or Hermes may propose an alternative only if:

- the original intent is unchanged;
- the alternative method is declared;
- the tool remains allowlisted or explicitly approved;
- the new risk level is equal or lower, or approval is requested;
- the Evidence Pack records the failed attempt and fallback proposal;
- the fallback does not increase data exposure silently.

Forbidden fallbacks:

- unallowlisted tool;
- destructive action;
- external send;
- secret access;
- Docker socket;
- memory write;
- bypassing blocked plugin policy;
- installing code from GitHub to work around a failure.

Rule:

```text
A blocked path cannot be replaced by an unreviewed path.
```

---

# 9. Remediation Candidate Lane

When a failure, blocker or inconsistency is detected, Pantheon may open a parallel remediation candidate lane.

This lane may:

- analyze the issue;
- identify the affected component;
- propose a fix;
- prepare a patch candidate;
- generate an Evidence Pack;
- propose tests;
- propose rollback.

It must not:

- apply the fix automatically;
- bypass approval;
- bypass allowlist;
- mutate validated memory;
- activate skills;
- change workflows;
- modify runtime configuration;
- access secrets;
- use Docker socket.

Rule:

```text
Detect → document → propose → validate → apply.
```

Not:

```text
Detect → fix automatically.
```

---

# 10. Initial tool decisions

## 10.1 Stirling-PDF

```yaml
tool_name: Stirling-PDF
repository: Stirling-Tools/Stirling-PDF
license: to_verify
license_status: not_checked
type: PDF service
status: test
maturity: production_candidate
data_classification: project_sensitive
local_only: true
network_exposure: LAN_only
auth_required: true
sandbox_required: true
file_access: read_write_copy_only
network_access: limited
memory_access: none
secrets_access: forbidden
shell_access: none
side_effects:
  - creates_processed_pdf_copies
  - may_apply_ocr
  - may_redact_or_transform_pdf
approval_level: C2_or_C3
allowed_usage:
  - pdf_info_check
  - pdf_metadata_check
  - pdf_text_layer_check
  - pdf_ocr_prepare_on_copy
  - pdf_compress_copy
forbidden_usage:
  - overwrite_source_pdf
  - public_exposure_without_auth
  - commit_real_documents_to_repo
  - redaction_without_review
  - knowledge_ingestion_without_evidence_pack
rollback_plan: stop_container_remove_stack_keep_source_files
review_frequency: before_first_install_then_quarterly
last_reviewed: null
default_decision: sandbox_test_only
```

## 10.2 OpenWebUI extensions

```yaml
tool_name: OpenWebUI extensions
repository: Fu-Jie/openwebui-extensions
license: to_verify
license_status: not_checked
type: OpenWebUI plugin collection
status: test
maturity: mixed
data_classification: internal_or_project
local_only: true
network_exposure: LAN_only
auth_required: true
sandbox_required: true
file_access: depends_on_extension
network_access: depends_on_extension
memory_access: none_or_unknown
secrets_access: forbidden
shell_access: forbidden
side_effects:
  - may_transform_messages
  - may_export_files
  - may alter context
approval_level: C3
allowed_usage:
  - Markdown Normalizer test
  - Export to Word test
  - Export to Excel test
  - Smart Mind Map test
  - Smart Infographic test
forbidden_usage:
  - batch_install_plugins_from_github
  - autonomous_agent_pipe
  - unreviewed_context_memory_plugins
rollback_plan: remove_extension_and_restore_openwebui_config
review_frequency: per_extension_before_install
last_reviewed: null
default_decision: test_one_by_one
```

## 10.3 Hermes plugins

```yaml
tool_name: Hermes plugins
repository: external_hermes_plugin_repositories
license: to_verify_per_repository
license_status: not_checked
type: Hermes plugin
status: watch
maturity: mixed
data_classification: internal
local_only: true
network_exposure: none_by_default
auth_required: n/a
sandbox_required: true
file_access: none_by_default
network_access: none_by_default
memory_access: none_by_default
secrets_access: forbidden
shell_access: forbidden
side_effects:
  - may alter execution behavior
  - may access tools
  - may affect memory or autonomy
approval_level: C3_to_C5
allowed_usage:
  - conceptual_review
  - sandbox_review_after_policy
forbidden_usage:
  - production_install_without_allowlist
  - autonomy_plugins
  - memory_write_plugins
  - remote_bridge_plugins
  - secrets_or_docker_access
rollback_plan: remove_plugin_restore_hermes_config
review_frequency: per_plugin_before_test
last_reviewed: null
default_decision: watch_or_blocked
```

## 10.4 AgentScope

```yaml
tool_name: AgentScope
repository: agentscope-ai/agentscope
license: to_verify
license_status: not_checked
type: agent_framework
status: watch
maturity: production_candidate
data_classification: none
local_only: true
network_exposure: none
sandbox_required: true
file_access: none
network_access: none
memory_access: none
secrets_access: forbidden
shell_access: forbidden
side_effects: []
approval_level: C0
allowed_usage:
  - workflow_schema_inspiration
forbidden_usage:
  - integrate_as_pantheon_runtime
  - replace_hermes_runtime
rollback_plan: documentation_only_no_runtime
review_frequency: before_any_code_use
last_reviewed: null
default_decision: conceptual_only
```

## 10.5 Hermes self-evolution

```yaml
tool_name: Hermes self-evolution
repository: NousResearch/hermes-agent-self-evolution
license: to_verify
license_status: not_checked
type: self_evolution_framework
status: watch
maturity: experimental
data_classification: anonymized_only
local_only: true
network_exposure: none_by_default
sandbox_required: true
file_access: candidate_patch_only
network_access: none_by_default
memory_access: candidates_only
secrets_access: forbidden
shell_access: limited_in_sandbox
side_effects:
  - may generate skill variants
  - may generate prompt variants
  - may generate patch candidates
approval_level: C3_to_C5
allowed_usage:
  - candidate_skill_evolution
  - evaluation_design
  - before_after_benchmark
forbidden_usage:
  - auto_merge
  - mutate_active_skill_directly
  - code_evolution_without_policy
  - use_real_non_anonymized_sessions
rollback_plan: discard_candidate_branch_or_patch
review_frequency: before_each_experiment
last_reviewed: null
default_decision: documentation_only_then_sandbox
```

## 10.6 BrainAPI2

```yaml
tool_name: BrainAPI2
repository: Lumen-Labs/brainapi2
license: to_verify
license_status: not_checked
type: memory_framework
status: watch
maturity: experimental_or_unknown
data_classification: none
local_only: true
network_exposure: none
sandbox_required: true
file_access: none
network_access: none
memory_access: none
secrets_access: forbidden
shell_access: forbidden
side_effects: []
approval_level: C0
allowed_usage:
  - memory_event_schema_inspiration
  - provenance_model_inspiration
forbidden_usage:
  - code_copy_without_license_review
  - direct_memory_runtime_integration
rollback_plan: documentation_only_no_runtime
review_frequency: before_any_code_use
last_reviewed: null
default_decision: conceptual_only
```

## 10.7 GBrain

```yaml
tool_name: GBrain
repository: garrytan/gbrain
license: to_verify
license_status: not_checked
type: markdown_truth_and_skill_system
status: watch
maturity: experimental_or_unknown
data_classification: none
local_only: true
network_exposure: none
sandbox_required: false
file_access: none
network_access: none
memory_access: none
secrets_access: forbidden
shell_access: forbidden
side_effects: []
approval_level: C0
allowed_usage:
  - skill_resolver_inspiration
  - conventions_inspiration
  - markdown_truth_inspiration
forbidden_usage:
  - replace_pantheon_document_hierarchy
  - copy_code_without_review
rollback_plan: documentation_only_no_runtime
review_frequency: before_any_code_use
last_reviewed: null
default_decision: conceptual_only
```

---

# 11. Installation rule

Before installing any external tool:

1. classify it in this policy;
2. verify license status;
3. define approval level;
4. define allowed and forbidden usage;
5. define rollback;
6. define sandbox if needed;
7. update task contracts if the tool performs actions;
8. update Evidence Pack requirements if the tool produces outputs;
9. log the intervention by adding an `ai_logs/YYYY-MM-DD-slug.md` entry.

---

# 12. Final rule

```text
External tools are capabilities, not authorities.
External integrations are allowed only through policy, task contract, Evidence Pack and rollback.
```
