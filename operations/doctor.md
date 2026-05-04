# Pantheon Doctor — Operations Checklist

> Read-only operational checklist for checking Pantheon Next repository coherence before refactor, deployment or external-tool testing.
>
> Doctor observes and reports. Doctor does not repair.

This document is inspired by AI configuration scoring, path-grounding and execution-discipline patterns, but it remains Pantheon-governed.

It does not install Caliber, AnimoCerebro, Symphony, Graphify, CTX, Langflow, Promptfoo, Instructor, Outlines, Warp, Recursive-Language-Models or any other external tool.

---

## 1. Purpose

Pantheon Doctor is a manual or future-scriptable checklist.

Its role is to verify that the repository still follows the active operating model:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

Doctor may report:

```text
PASS
WARN
FAIL
NOT_APPLICABLE
TO_VERIFY
BLOCKED_BY_POLICY
```

Doctor must not automatically fix anything.

---

## 2. Authority and approval level

Default mode:

```text
C0 read-only diagnostic
```

Allowed:

```text
read files
list paths
check text references
check file existence
run safe local read-only commands
call local read-only health endpoints if already running
produce a report
```

Forbidden:

```text
create files automatically
modify files automatically
install dependencies
run migrations
start containers
stop containers
read secrets
print secrets
push branches
merge PRs
call external services
mutate OpenWebUI
mutate Hermes
promote memory
activate skills
canonize workflows
execute Task Contracts
```

Any remediation must become a separate C3 patch candidate.

---

## 3. Output format

Doctor output should use this table:

| Check | Status | Evidence | Risk | Next action |
|---|---|---|---|---|
| governance_docs_exist | PASS | paths found | low | none |
| forbidden_paths_absent | WARN | `domains/architecture` found | medium | classify or rename |

Each `FAIL` must include:

```text
file or path involved
expected state
actual state
risk
recommended next action
approval level for fix
```

Each `BLOCKED_BY_POLICY` must include:

```text
blocked action
policy reference
why it is blocked
safe alternative
```

---

## 4. Severity model

| Status | Meaning |
|---|---|
| `PASS` | Expected state verified |
| `WARN` | Incomplete, stale or ambiguous but not an immediate doctrine violation |
| `FAIL` | Missing required file, contradiction, policy violation or unsafe active target |
| `NOT_APPLICABLE` | Check does not apply to the current repo state |
| `TO_VERIFY` | Manual/live environment verification required |
| `BLOCKED_BY_POLICY` | Requested or discovered action is forbidden by governance |

Risk scale:

```text
low
medium
high
critical
```

A `critical` risk means one of these may be happening:

```text
Pantheon runtime drift
approval bypass
secret exposure
memory auto-promotion
external action without approval
Docker socket / destructive access
unclassified external tool use
private project/client data committed
```

---

## 5. Baseline checks

### 5.1 Root entry points

Required:

```text
README.md
CLAUDE.md
CHANGELOG.md
VERSION
```

Expected:

```text
README.md uses Pantheon Next naming.
README.md references the OpenWebUI / Hermes / Pantheon split.
CLAUDE.md is aligned with Pantheon Next governance.
VERSION exists and is readable.
```

Failure mode:

```text
WARN if optional entry is missing.
FAIL if README.md is missing.
FAIL if README.md contradicts the Hermes-backed pivot.
```

---

### 5.2 AI logs

Required:

```text
ai_logs/README.md
```

Expected:

```text
One intervention = one dated log file.
No direct main mutation is documented as allowed.
No private client/project data is written into logs.
Each significant PR has a matching ai_logs entry.
```

Doctor should verify recent log naming:

```text
ai_logs/YYYY-MM-DD-slug.md
```

Failure mode:

```text
WARN if logs exist but naming is inconsistent.
WARN if a recent PR has no corresponding log.
FAIL if ai_logs/README.md is missing.
FAIL if real private project/client data appears in logs.
```

---

## 6. Governance document checks

Required under `docs/governance/`:

```text
README.md
STATUS.md
ROADMAP.md
ARCHITECTURE.md
MODULES.md
AGENTS.md
MEMORY.md
APPROVALS.md
TASK_CONTRACTS.md
TASK_CONTRACT_REVISIONS.md
EVIDENCE_PACK.md
HERMES_INTEGRATION.md
OPENWEBUI_INTEGRATION.md
OPENWEBUI_DOMAIN_MAPPING.md
MODEL_ROUTING_POLICY.md
EXTERNAL_TOOLS_POLICY.md
EXTERNAL_RUNTIME_OPTIONS.md
EXTERNAL_AI_OPTION_REVIEWS.md
EXECUTION_DISCIPLINE.md
EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md
KNOWLEDGE_TAXONOMY.md
CODE_AUDIT_POST_PIVOT.md
WORKFLOW_SCHEMA.md
WORKFLOW_ADAPTATION.md
SKILL_LIFECYCLE.md
MEMORY_EVENT_SCHEMA.md
VERSIONS.md
```

Expected:

```text
docs/governance/README.md indexes every required governance document.
STATUS.md matches current completed documents.
ROADMAP.md does not resurrect Pantheon autonomous runtime.
ARCHITECTURE.md states that Pantheon governs and Hermes executes.
TASK_CONTRACT_REVISIONS.md is treated as an addendum, not runtime implementation.
EXECUTION_DISCIPLINE.md preserves single-role before workflow.
```

Failure mode:

```text
FAIL if a required governance document is missing.
WARN if it exists but is not indexed.
WARN if STATUS.md or ROADMAP.md appear stale.
FAIL if any governance doc makes Pantheon the executor instead of Hermes.
```

---

## 7. Doctrine coherence checks

Doctor must verify the canonical split appears consistently:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

Expected authority mapping:

| Layer | Allowed authority |
|---|---|
| OpenWebUI | cockpit, chat, Knowledge display, validation UI |
| Hermes Agent | execution runtime under Task Contract |
| Pantheon Next | governance, source of truth, domains, approvals, memory policy |

Failure mode:

```text
FAIL if OpenWebUI is described as canonical memory.
FAIL if Hermes is allowed to bypass approvals.
FAIL if Pantheon is described as autonomous execution runtime.
WARN if wording is ambiguous and could imply runtime drift.
```

---

## 8. Forbidden drift checks

Doctor must detect forbidden or suspicious paths:

```text
domains/architecture
skills/generic
workflows/generic
memory/agency
```

Expected canonical replacements:

```text
domains/architecture_fr
domains/general/skills
domains/general/workflows
memory/system
```

Failure mode:

```text
WARN if forbidden path exists and is classified as legacy.
FAIL if forbidden path exists and is unclassified.
```

Doctor must also detect risky terminology in active governance docs:

```text
Pantheon runtime
Execution Engine
Agent Runtime
Tool Runtime
LLM Provider Router
scheduler
memory auto-promotion
self-evolution auto-merge
LangGraph central orchestrator
workflow runtime hidden inside Pantheon
```

Interpretation:

```text
PASS if terms appear only in forbidden-drift, rejection, legacy or external runtime sections.
WARN if terms appear ambiguously.
FAIL if terms are described as active Pantheon target architecture.
```

---

## 9. Domain checks

Required canonical domain folders:

```text
domains/general
domains/architecture_fr
domains/software
```

Expected minimum files per domain:

```text
domain.md
rules.md
knowledge_policy.md
output_formats.md
```

Expected optional folders:

```text
skills/
workflows/
templates/
```

Current interpretation:

```text
domains/general = started
domains/architecture_fr = in review if PR not merged
domains/software = targeted / to verify
```

Failure mode:

```text
PASS if folder and minimum files exist.
WARN if folder exists but minimum files are incomplete.
TO_VERIFY if STATUS.md marks the domain as targeted but not started.
FAIL if docs claim the domain is active but folder is missing.
```

---

## 10. Skill and workflow checks

Candidate skills should follow:

```text
domains/{domain}/skills/{skill_id}/SKILL.md
domains/{domain}/skills/{skill_id}/manifest.yaml
domains/{domain}/skills/{skill_id}/examples.md
domains/{domain}/skills/{skill_id}/tests.md
domains/{domain}/skills/{skill_id}/UPDATES.md
```

Expected candidate skills currently referenced by STATUS:

```text
domains/general/skills/adaptive_orchestration/
domains/general/skills/project_context_resolution/
domains/general/skills/knowledge_selection/
```

Doctor should verify:

```text
SKILL.md exists
manifest exists or absence is explicitly acceptable at current maturity
status is draft/candidate/active/deprecated/rejected
approval level is declared
memory impact is declared
Hermes mapping is explicit or null
skill is not marked active without lifecycle evidence
```

Workflow checks:

```text
workflow templates remain templates
session workflows remain session scoped
workflow candidates are not canonical by default
dependency graph terminology matches WORKFLOW_SCHEMA.md and WORKFLOW_ADAPTATION.md
```

Failure mode:

```text
WARN if candidate skill folder is incomplete.
WARN if workflow docs are missing examples.
FAIL if a skill is marked active without lifecycle evidence.
FAIL if workflow canonization is automatic.
```

---

## 11. Single-role versus workflow checks

Required doctrine:

```text
EXECUTION_DISCIPLINE.md
WORKFLOW_SCHEMA.md
WORKFLOW_ADAPTATION.md
TASK_CONTRACT_REVISIONS.md
```

Expected rules:

```text
single_role_path before workflow
solo before dependency_graph
workflow escalation only when complexity/risk/source reconciliation requires it
Task Contract revision required when risk/frame changes
resume_policy required before resumed execution
```

Doctor should check that no document implies:

```text
every question requires full workflow
Hermes may revise its own contract silently
execution may resume after C4/C5 escalation without approval
single-role can hide external/contractual risk
```

Failure mode:

```text
WARN if single-role doctrine is missing from one of the main workflow docs.
FAIL if a doc says Hermes may continue after escalation without revised contract or approval.
```

---

## 12. Task Contract checks

Required:

```text
docs/governance/TASK_CONTRACTS.md
docs/governance/TASK_CONTRACT_REVISIONS.md
```

Expected concepts:

```text
task_contract
single_role_task_contract
single_role_escalation
workflow_revision_signal
zeus_arbitration
task_contract_revision
resume_policy
reset_to_baseline
```

Expected rules:

```text
Task Contract defines the execution frame.
A contract revision changes the frame.
A resume policy controls continuation.
Hermes executes only the approved current frame.
```

Failure mode:

```text
WARN if TASK_CONTRACTS.md lacks a cross-reference to TASK_CONTRACT_REVISIONS.md.
FAIL if Task Contract revision is described as implemented runtime when it is documentation-only.
FAIL if resume behavior allows approval bypass.
```

---

## 13. Evidence Pack checks

Required:

```text
docs/governance/EVIDENCE_PACK.md
```

Expected for consequential outputs:

```text
files_read
sources_used
knowledge_bases_consulted
tools_used
commands_run
assumptions
limitations
unsupported_claims
approval_required
next_safe_action
```

Additional expected fields for adaptive workflows and contract revisions:

```text
workflow_adaptations
parallel_groups
join_policy
source_signal
arbitration_result
resume_policy
outputs_preserved
outputs_discarded
```

Failure mode:

```text
WARN if Evidence Pack schema lacks adaptive/revision fields.
FAIL if consequential outputs are allowed without proof/evidence.
```

---

## 14. OpenWebUI checks

Required docs/config:

```text
docs/governance/OPENWEBUI_INTEGRATION.md
docs/governance/OPENWEBUI_DOMAIN_MAPPING.md
operations/openwebui_manual_setup.md
config/openwebui_domain_mapping.example.yaml
```

Expected rules:

```text
OpenWebUI is cockpit only.
OpenWebUI Knowledge is not Pantheon memory.
OpenWebUI Workspace Models are presets, not Pantheon agents.
OpenWebUI Skills are operator aids, not active Pantheon skills.
OpenWebUI must point to Hermes Gateway, not Pantheon API, unless a compliant model gateway is explicitly added later.
```

Failure mode:

```text
FAIL if docs instruct OpenWebUI to point directly to Pantheon API as OpenAI-compatible backend.
WARN if Knowledge Base names are used without source tier or privacy level.
TO_VERIFY if live OpenWebUI Knowledge names have not been checked.
```

---

## 15. Model routing checks

Required:

```text
docs/governance/MODEL_ROUTING_POLICY.md
config/model_routing.example.yaml
```

Expected:

```text
single_ollama_instance mode documented
multi_ollama_instance mode documented
fallback C0-C5 documented
agent-role model preferences documented
Evidence Pack trace for model substitution documented
```

Forbidden:

```text
Pantheon LLM Provider Router as active component
silent fallback for C4/C5
remote model use for private data without policy
```

Failure mode:

```text
WARN if config exists but lacks fallback policy.
FAIL if Pantheon is described as active LLM provider router.
FAIL if C4/C5 fallback is silent.
```

---

## 16. Hermes checks

Required docs/templates:

```text
docs/governance/HERMES_INTEGRATION.md
hermes/templates/pantheon-os/
hermes/context/
```

Expected API/context paths:

```text
GET /runtime/context-pack
GET /domain/snapshot
GET /domain/approval/classify
```

Expected rules:

```text
Hermes executes.
Pantheon provides Task Contract, Context Pack, policies and Evidence requirements.
Hermes outputs remain candidates until approved.
Hermes does not canonize memory.
Hermes does not mutate governance Markdown without approval.
Hermes emits revision signals instead of silently changing execution frame.
```

Failure mode:

```text
WARN if Hermes template exists but is not installed locally.
WARN if Hermes context exports are present but live consumption is not verified.
FAIL if docs allow Hermes to bypass approvals.
FAIL if Hermes may rewrite its own Task Contract silently.
```

---

## 17. API checks

If the Pantheon API is running locally, safe checks may include:

```text
GET /health
GET /runtime/context-pack
GET /domain/snapshot
GET /domain/agents
GET /domain/skills
GET /domain/workflows
GET /domain/memory
GET /domain/knowledge
GET /domain/legacy
GET /domain/approval/classify
```

Rules:

```text
read-only requests only
no POST except documented classify endpoint if test payload is non-sensitive
no secrets
no external network dependency
no mutation
```

Failure mode:

```text
NOT_APPLICABLE if API is not running.
WARN if endpoint exists but returns stale/static data.
FAIL if endpoint mutates state unexpectedly.
FAIL if endpoint exposes secret-like content.
```

---

## 18. README diagram asset checks

Required registry:

```text
docs/assets/README.md
```

Expected export files when README diagrams are integrated:

```text
docs/assets/pantheon-next-overview.png
docs/assets/pantheon-governed-flow.png
docs/assets/pantheon-hermes-contract.png
docs/assets/pantheon-agent-roles.png
docs/assets/pantheon-knowledge-vs-memory.png
docs/assets/pantheon-repository-map.png
```

Expected rules:

```text
No README image link should point to a missing local export.
No Lucid direct link replaces a local export in README.md.
Diagrams are reading aids only.
Governance Markdown remains source of truth.
```

Failure mode:

```text
WARN if assets are registered but not yet exported.
FAIL if README.md embeds missing images.
FAIL if diagrams visually or textually imply that Pantheon executes tools directly.
```

---

## 19. External tool and runtime checks

Required:

```text
docs/governance/EXTERNAL_TOOLS_POLICY.md
docs/governance/EXTERNAL_RUNTIME_OPTIONS.md
docs/governance/EXTERNAL_AI_OPTION_REVIEWS.md
docs/governance/EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md
```

Expected classifications include:

```text
Stirling-PDF
SearXNG
n8n
OpenWebUI extensions
Hermes plugins
Cycles / runcycles
Omnigraph
RAGFlow
Thoth
kontext-brain-ts
Kanwas
AKS Reference Server
AgentRQ
opencode-loop
six-hats-skill
OpenConcho
Honcho
LangChain / LangGraph
Langflow
OpenClaw
OpenAI Symphony
Graphify
Layer Infinite / Layer
CTX
Binderly
NeverWrite
AnimoCerebro
Caliber / ai-setup
Andrej Karpathy Skills
Promptfoo
Instructor
Outlines
Guidance
DSPy
Brainlid LangChain
Recursive-Language-Models
Warp / Oz
```

Expected rules:

```text
unknown tools are blocked until classified
external runtimes may assist Pantheon but must not become Pantheon
evaluation tools may measure but not govern
structured-output tools may constrain but not approve
developer tools may assist but not become runtime
n8n may detect and notify but not execute Hermes or send externally by default
Caliber is test_read_only / rejected_for_core
AnimoCerebro is blocked_until_reviewed / rejected_for_core
Recursive-Language-Models is watch_test_only / sandbox_only
Warp is developer_tool_optional / blocked_for_core
```

Failure mode:

```text
WARN if a discussed tool lacks classification.
FAIL if an external tool is installed or configured without policy entry.
FAIL if an external runtime is described as Pantheon authority.
```

---

## 20. n8n checks

Required docs:

```text
operations/n8n_email_automation.md
operations/n8n_workflows/email_received_operator_notification.md
```

Expected rules:

```text
n8n may detect and notify.
n8n must not govern.
n8n must not remember.
n8n must not execute Hermes by default.
n8n must not reply externally without approval.
n8n workflows remain disabled/spec-only unless explicitly reviewed.
```

Failure mode:

```text
WARN if n8n docs are present but no live config is verified.
FAIL if n8n is used as scheduler/runtime/approval authority.
FAIL if n8n sends external emails without C4 approval path.
```

---

## 21. Knowledge checks

Required:

```text
docs/governance/KNOWLEDGE_TAXONOMY.md
config/openwebui_domain_mapping.example.yaml
operations/openwebui_manual_setup.md
knowledge/registry.example.yaml
```

Planned but not necessarily present yet:

```text
knowledge/registry.yaml
```

Expected:

```text
Knowledge and Memory are separated.
OpenWebUI Knowledge is source material.
Pantheon Memory requires candidate → Evidence Pack → validation.
Project-private Knowledge is not mixed across projects.
source tier, reliability, privacy and freshness are defined.
```

Failure mode:

```text
WARN if live Knowledge Registry is missing while still marked planned.
WARN if example registry is not validated against live OpenWebUI Knowledge names.
FAIL if documents say Knowledge Base equals canonical memory.
FAIL if cross-project private sources are allowed without policy.
```

---

## 22. Memory checks

Required:

```text
docs/governance/MEMORY.md
docs/governance/MEMORY_EVENT_SCHEMA.md
```

Expected canonical memory folders:

```text
memory/session
memory/candidates
memory/project
memory/system
```

Expected rules:

```text
no automatic promotion
memory promotion is C3 minimum
Evidence Pack required
system memory replaces agency memory
Hermes local memory is not canonical
OpenWebUI history is not canonical
workflow candidates are not canonical workflows
```

Failure mode:

```text
WARN if folders are missing but memory runtime is not implemented yet.
FAIL if docs describe automatic promotion as active policy.
FAIL if Hermes/OpenWebUI memory is treated as Pantheon canonical memory.
```

---

## 23. Security and secrets checks

Doctor must never print secret values.

It may report only:

```text
secret-like pattern detected
file path
line number if safe
redacted key name
```

Patterns to flag:

```text
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GITHUB_TOKEN=
HERMES_API_SERVER_KEY=
API_SERVER_KEY=
password=
secret=
token=
private_key
BEGIN RSA PRIVATE KEY
BEGIN OPENSSH PRIVATE KEY
```

Allowed files for placeholders:

```text
.env.example
*.example.yaml
```

Failure mode:

```text
WARN if placeholder appears in example file.
FAIL if plausible real secret appears in tracked non-example file.
BLOCKED_BY_POLICY if a proposed Doctor run would print secrets.
```

---

## 24. Docker / deployment checks

Doctor may inspect Docker files only.

It must not run containers.

Check for:

```text
docker-compose.yml
infra/compose/
.env.example
operations/install.md
operations/openwebui_manual_setup.md
```

Expected rules:

```text
OpenWebUI points to Hermes Gateway, not Pantheon API as /v1 backend.
Postgres OpenWebUI and Postgres Pantheon remain separated if both are used.
No Docker socket mounted into Hermes Lab.
No public Hermes Dashboard without auth/VPN.
No latest tag for critical storage services if avoidable.
```

Failure mode:

```text
WARN if compose docs are incomplete.
FAIL if Docker socket is mounted into Hermes or if secrets are hardcoded.
FAIL if public dashboard exposure is recommended without auth/VPN.
```

---

## 25. GitHub / PR hygiene checks

Expected:

```text
no direct push to main
one branch per intervention
one ai_logs entry per significant intervention
PR body states objective, changes, guardrails, tests and follow-up
no mixed runtime/domain/governance changes unless explicitly justified
```

Failure mode:

```text
WARN if PR body lacks tests or guardrails.
WARN if large governance rewrite occurs without focused rationale.
FAIL if direct main mutation is documented or detected.
FAIL if private data appears in PR content.
```

---

## 26. Suggested local commands

These are examples for a future manual run.

They are read-only.

```bash
find docs/governance -maxdepth 1 -type f -name "*.md" | sort
find ai_logs -maxdepth 1 -type f -name "*.md" | sort
find domains -maxdepth 4 -type f | sort
find operations -maxdepth 3 -type f | sort
find docs/assets -maxdepth 1 -type f | sort
```

Potential grep checks:

```bash
grep -R "domains/architecture\|skills/generic\|workflows/generic\|memory/agency" -n . --exclude-dir=.git
grep -R "OPENAI_API_KEY=\|GITHUB_TOKEN=\|private_key\|BEGIN RSA PRIVATE KEY" -n . --exclude-dir=.git
grep -R "Pantheon.*executes\|Pantheon runtime\|auto-promot" -n docs README.md operations --exclude-dir=.git
```

Rules:

```text
Do not paste secret values into reports.
Redact any suspicious value.
Do not run write commands in Doctor mode.
```

---

## 27. Doctor report template

```md
# Pantheon Doctor Report — YYYY-MM-DD

Branch / ref: `<ref>`
Mode: C0 read-only
Operator: `<name>`

## Summary

| Category | Status | Notes |
|---|---|---|
| Governance docs | PASS | |
| AI logs | PASS | |
| Doctrine coherence | PASS | |
| Domains | WARN | |
| Skills/workflows | WARN | |
| Single-role/workflow | PASS | |
| Task contracts | PASS | |
| Evidence Packs | WARN | |
| README assets | WARN | |
| OpenWebUI | PASS | |
| Hermes | WARN | |
| External tools | PASS | |
| n8n | TO_VERIFY | |
| Knowledge | WARN | |
| Memory | WARN | |
| Secrets | PASS | |
| Docker | TO_VERIFY | |
| PR hygiene | PASS | |

## Findings

| Check | Status | Evidence | Risk | Next action |
|---|---|---|---|---|

## Required approvals before fix

| Finding | Approval |
|---|---|

## Evidence Pack references

- files read:
- commands run:
- assumptions:
- limitations:
```

---

## 28. Future automation boundary

A future script may be added only if it remains:

```text
read-only by default
no network by default
no secret printing
no automatic fix
no commit
no push
no dependency install
no container control
no external service calls
```

Potential path:

```text
operations/doctor.py
```

Approval before adding script:

```text
C3
```

Forbidden for any future Doctor script:

```text
auto-fix
auto-commit
auto-merge
auto-install
secret scan with raw secret output
Docker socket access
OpenWebUI mutation
Hermes mutation
memory promotion
workflow canonization
```

---

## 29. Final rule

```text
Doctor observes and reports.
Doctor does not repair.
Doctor must never become the hidden runtime, scheduler, fixer or approval authority.
```
