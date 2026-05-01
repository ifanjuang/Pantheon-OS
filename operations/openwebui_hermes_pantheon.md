# OpenWebUI / Hermes Agent / Pantheon OS — Operating Protocol

> Planned operating protocol. This document defines the target interaction model between OpenWebUI, Hermes Agent and Pantheon OS.

---

# 1. Executive summary

The recommended architecture separates three responsibilities:

```text
OpenWebUI = user cockpit
Hermes Agent = privileged operational worker
Pantheon OS = governed domain authority and source of truth
```

Core rule:

```text
Hermes operates.
Pantheon arbitrates.
OpenWebUI pilots and displays.
```

Hermes Agent may become the preferred operational interlocutor for Pantheon OS. It may know the Pantheon operating protocol, consult Pantheon reference files, inspect repositories, run local checks, prepare patches and submit candidate assets.

Hermes does not replace Pantheon OS.

Pantheon remains the authority for canonical agents, workflows, skills, decisions, project memory, system memory, RAG policies, governance rules, validations, vetoes and criticality.

OpenWebUI remains the cockpit: chat, routing, run display, evidence display, validation actions, approvals and user-facing traceability.

---

# 2. Corrected authority model

Pantheon must not become a duplicated autonomous agent runtime.

Hermes already provides runtime execution capabilities.

Pantheon provides:

- governance;
- domain contracts;
- canonical skills;
- canonical workflows;
- memory validation rules;
- approval policies;
- veto and validation discipline;
- source-of-truth documentation;
- candidate promotion rules.

Correct formula:

```text
Hermes executes operational work.
Pantheon defines and canonizes.
OpenWebUI exposes and routes.
```

Forbidden drift:

```text
OpenWebUI owns skills.
Hermes owns skills.
Pantheon owns skills.
All three diverge.
```

Expected flow:

```text
Hermes experiments.
OpenWebUI exposes.
Pantheon canonizes.
```

---

# 3. Layer roles

| Layer | Primary role | Authority |
|---|---|---|
| OpenWebUI | Cockpit, chat, routing, user actions, trace display | Interface authority only |
| Hermes Agent | Operational worker, local skill lab, repo audit, long research, patch preparation | Local operational authority |
| Pantheon OS | Governed domain authority, canonical workflows, skills, memory, decisions, policies | Final authority |

Stable statement:

```text
Hermes knows the Pantheon protocol.
Pantheon stores the true state.
Hermes prepares and proposes.
Pantheon validates and persists.
OpenWebUI displays and asks for approval.
```

---

# 4. Canonical rule

Anything that becomes official must go through Pantheon OS.

This includes:

- active skills;
- active workflows;
- D0-D3 decisions;
- project memory;
- system memory;
- governance rules;
- structural documentation changes;
- structural code changes;
- official agents;
- domain packages;
- C3+ actions;
- every C4/C5 action.

Hermes may prepare. It cannot canonize.

OpenWebUI may trigger and display. It cannot arbitrate final governed truth.

Pantheon arbitrates.

---

# 5. Hermes as privileged operational worker

Hermes Agent is well-suited for:

- reading a repository;
- comparing documentation and code;
- running tests;
- auditing dependencies;
- preparing a patch;
- creating a branch;
- opening a candidate pull request;
- drafting a local experimental skill;
- transforming repeated procedures into candidate skills;
- conducting long research;
- analyzing external repositories;
- diagnosing Docker, API, RAG or CI issues.

Hermes must never:

- push directly to `main`;
- mutate project memory directly;
- create final official decisions;
- activate a canonical Pantheon skill;
- modify an active workflow directly;
- bypass ZEUS, THEMIS, APOLLO or HESTIA;
- use local Hermes memory as Pantheon truth;
- act on the repository without a dedicated branch;
- correct code before documentary clarification when the documentation is insufficient.

Short rule:

```text
Hermes is Pantheon’s privileged operator, not Pantheon’s authority.
```

---

# 6. What Hermes must know

Hermes should know the Pantheon operating protocol, not a frozen copy of all Pantheon truth.

Mandatory sequence for Pantheon repository work:

1. Read recent entries in `ai_logs/` (start with `ai_logs/README.md`).
2. Read `docs/governance/STATUS.md`.
3. Read the relevant reference Markdown files under `docs/governance/` before the code.
4. Respect the documentation hierarchy.
5. Treat Markdown reference files as the source of truth.
6. If code contradicts Markdown, Markdown wins.
7. If code is better than Markdown, propose or apply a Markdown update first.
8. Never push to `main`.
9. Work on a dedicated branch.
10. Produce candidates, not active canonical objects.
11. Ask for validation for structural or risky changes.
12. Add an `ai_logs/YYYY-MM-DD-slug.md` entry after a meaningful intervention.
13. Avoid new abstractions unless the gain is clear.
14. Avoid unnecessary complexity.

Hermes should not keep a frozen local copy of:

- every agent;
- every workflow;
- every decision;
- project memory;
- full system memory;
- complete roadmap;
- full code state;
- deployment configuration.

A frozen local copy becomes obsolete. Hermes should consult Pantheon for the true state.

---

# 7. Pantheon Context Pack

Pantheon should expose a compact context pack for Hermes.

Conceptual endpoint:

```http
GET /runtime/context-pack
```

Target response:

```json
{
  "project": "Pantheon OS",
  "truth_files": [
    "README.md",
    "ai_logs/README.md",
    "docs/governance/STATUS.md",
    "docs/governance/ARCHITECTURE.md",
    "docs/governance/MODULES.md",
    "docs/governance/AGENTS.md",
    "docs/governance/MEMORY.md",
    "docs/governance/ROADMAP.md"
  ],
  "current_status": "Hermes-backed domain operating layer, documentation-first, partially implemented",
  "active_rules": [
    "docs_before_code",
    "markdown_source_of_truth",
    "no_main_push",
    "branch_required",
    "candidate_before_active",
    "ai_log_required",
    "no_memory_promotion_without_validation"
  ],
  "domain_packages": [
    "domains/general",
    "domains/architecture_fr",
    "domains/software"
  ],
  "known_blockers": [
    "legacy runtime still requires audit",
    "Domain Layer tests not confirmed in this branch",
    "OpenWebUI / Hermes / Pantheon interaction layer not implemented yet"
  ],
  "recommended_entrypoint": "Hermes Pantheon Operator"
}
```

The context pack does not replace reference Markdown files. It only provides a compact operational orientation.

---

# 8. Official flows

| Flow | Usage | Final authority |
|---|---|---|
| OpenWebUI → Pantheon | Governed domain work, RAG, decisions, memory, workflows | Pantheon |
| OpenWebUI → Hermes → Pantheon | Repo audit, patches, skills, Pantheon maintenance | Pantheon |
| Pantheon → Hermes → Pantheon | Controlled technical delegation from a Pantheon workflow | Pantheon |

OpenWebUI → Hermes alone may exist only for:

- local experimentation;
- drafts;
- non-critical research;
- work outside Pantheon;
- local skill exploration;
- actions with no impact on Pantheon truth.

When the result may become official, Hermes must submit it back to Pantheon.

---

# 9. Global flow

```text
User
  ↓
OpenWebUI
  ↓
Pantheon Router or Hermes Pantheon Operator
  ↓
Hermes loads the Pantheon operating protocol
  ↓
Hermes consults the Pantheon Context Pack
  ↓
Hermes executes, analyzes or prepares
  ↓
Hermes returns Candidate + Evidence Pack
  ↓
Pantheon validates, rejects or requests correction
  ↓
OpenWebUI displays, traces and asks for human validation when required
```

Functional diagram:

```text
┌──────────────────────────────────────────────┐
│                  OpenWebUI                   │
│ cockpit, chat, routing, actions, approvals   │
└──────────────────────┬───────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌──────────────────┐          ┌──────────────────────┐
│   Pantheon OS     │          │     Hermes Agent      │
│ governed authority│          │ privileged operator   │
│ source of truth   │          │ worker / skill lab    │
└────────┬─────────┘          └──────────┬───────────┘
         │                               │
         └──────── consultation ─────────┘
```

---

# 10. OpenWebUI cockpit

OpenWebUI should become the user cockpit, not the business engine.

It should allow the user to:

- select Pantheon or Hermes entrypoints;
- use a default router;
- see the active workflow;
- see active agents;
- see when Hermes is consulted;
- display evidence;
- display errors;
- display vetoes;
- approve or reject actions;
- create decision candidates;
- create memory candidates;
- promote skill candidates after validation;
- export reports;
- rerun a validation agent.

Recommended interface entries:

```text
Pantheon Router
Pantheon Zeus
Pantheon Research
Pantheon Repo Audit
Hermes Pantheon Operator
Hermes Agent Direct
```

Default entrypoint:

```text
Domain work → Pantheon Router
Pantheon repository maintenance → Hermes Pantheon Operator
```

---

# 11. OpenWebUI actions

| Action | Effect |
|---|---|
| Consult Hermes | Pantheon delegates a controlled technical task to Hermes |
| Rerun ZEUS | Replans the run |
| Rerun THEMIS | Rechecks rules, responsibility and governance |
| Rerun APOLLO | Rechecks final output quality |
| Create decision candidate | Sends a proposed decision to the decision layer |
| Add project memory candidate | Creates a candidate for HESTIA review |
| Add system memory candidate | Creates a candidate for MNEMOSYNE review |
| Create skill candidate | Proposes a skill under the relevant domain package |
| Approve patch | Authorizes a controlled technical action |
| Reject | Closes or sends back for correction |
| View evidence | Displays the Evidence Pack |
| View graph | Displays workflow and consultation graph |
| Export report | Produces a downloadable artifact |

---

# 12. Hermes Pantheon Operator

`Hermes Pantheon Operator` is not a canonical Pantheon agent.

It is a Hermes usage mode specialized for Pantheon operations.

Target local structure:

```text
~/.hermes/skills/pantheon-os/
  SKILL.md
  scripts/
    pantheon_rules.py
    pantheon_status.py
    pantheon_context_pack.py
    pantheon_run.py
    pantheon_artifacts.py
    pantheon_skill_candidate.py
    pantheon_memory_candidate.py
    pantheon_decision_candidate.py
  examples/
    audit_repo.md
    create_skill_candidate.md
    update_docs_first.md
    propose_patch.md
```

This Hermes skill should contain the Pantheon operating doctrine.

Conceptual excerpt:

```markdown
# Pantheon OS Skill

Use this skill whenever the user asks to work on Pantheon OS, audit the repo, modify documentation, create or review a skill, inspect workflows, consult project memory, or propose code changes.

## Core Doctrine

Pantheon OS is the source of truth.
Hermes is an operational worker and skill-forging assistant.
Hermes may inspect, prepare, test, research, propose and document.
Hermes must not bypass Pantheon governance.

## Mandatory Sequence for Repo Work

1. Read recent entries in ai_logs/ (start with ai_logs/README.md).
2. Read docs/governance/STATUS.md.
3. Read README.md and the relevant files under docs/governance/ (ARCHITECTURE.md, MODULES.md, AGENTS.md, MEMORY.md, ROADMAP.md) as needed.
4. Do not start from code before reading the Markdown references.
5. If code contradicts Markdown, Markdown wins.
6. If code is better than Markdown, propose a Markdown update first.
7. Never push to main.
8. Work on a dedicated branch.
9. Add an ai_logs/YYYY-MM-DD-slug.md entry after intervention.
10. Do not create abstractions without clear gain.

## Forbidden Actions

- Do not activate a Pantheon skill directly.
- Do not mutate project memory directly.
- Do not create final D0-D3 decisions directly.
- Do not bypass ZEUS, THEMIS, APOLLO or HESTIA.
- Do not promote local Hermes memory into Pantheon memory without review.
```

---

# 13. Hermes Skill Lab

Hermes may learn and draft skills locally in a separate experimental area.

```text
~/.hermes/pantheon-skill-lab/
  repo_md_code_audit/
  quote_review/
  formal_notice_letter/
  pantheon_boot_debug/
  adaptive_workflow_design/
  hermes_pantheon_operator/
```

These skills are experimental. They are not Pantheon skills.

When a skill becomes useful, Hermes may propose it as a Pantheon candidate under the relevant domain package:

```text
domains/{domain}/skills/{skill_id}/
  SKILL.md
  manifest.yaml
  examples.md
  tests.md
  UPDATES.md
```

The manifest must start as:

```yaml
lifecycle:
  state: candidate
  level: 0
  xp:
    validated: 0
    pending: 0
```

Lifecycle:

```text
Hermes draft
→ Hermes tested
→ Pantheon candidate
→ THEMIS review when risk/governance is involved
→ APOLLO review
→ human approval when required
→ Pantheon active
→ OpenWebUI exposed
```

---

# 14. Hermes outputs are candidates

| Hermes production | Initial status | Validation |
|---|---|---|
| Audit report | Artifact | APOLLO / human if critical |
| Repository patch | Patch candidate | Review + branch |
| Skill | Local draft, then candidate | THEMIS + APOLLO |
| Memory | Memory candidate | HESTIA / MNEMOSYNE |
| Decision | Decision candidate | ZEUS / THEMIS / human |
| Workflow | Workflow candidate | ZEUS / APOLLO / human |
| Documentation change | Documentation patch candidate | Documentation review |
| Code change | Code patch candidate | Only after documentation is clear |

Rule:

```text
Hermes proposes.
Pantheon canonizes.
```

---

# 15. Evidence Pack

Every Hermes output intended for Pantheon must include an Evidence Pack.

```json
{
  "evidence_pack": {
    "files_read": [
      "ai_logs/README.md",
      "docs/governance/STATUS.md",
      "docs/governance/ARCHITECTURE.md"
    ],
    "commands_run": [],
    "tests_run": [],
    "sources_used": [],
    "diffs_created": [],
    "errors": [],
    "limitations": [
      "No write action executed",
      "No tests run"
    ]
  }
}
```

The Evidence Pack allows Pantheon to validate the result without trusting only a narrative summary.

---

# 16. Run Contract

Every mixed task should have a clear run contract.

```json
{
  "run_id": "run_123",
  "entrypoint": "openwebui",
  "operator": "hermes",
  "authority": "pantheon",
  "mode": "suggest",
  "scope": "repo_audit",
  "allowed_actions": [
    "read_files",
    "run_tests",
    "propose_patch"
  ],
  "forbidden_actions": [
    "push_main",
    "activate_skill",
    "write_project_memory"
  ],
  "requires_validation": true,
  "expected_outputs": [
    "diagnostic",
    "patch_proposal",
    "skill_candidate"
  ]
}
```

---

# 17. Consultation Request and Result

When Pantheon delegates a task to Hermes, it should issue a `ConsultationRequest`.

```json
{
  "consultation_id": "consult_001",
  "parent_run_id": "run_123",
  "from": "pantheon",
  "to": "hermes",
  "reason": "repo_audit_requires_terminal",
  "mode": "read_only",
  "scope": "ifanjuang/Pantheon-OS",
  "allowed_actions": [
    "read_files",
    "run_tests",
    "propose_patch"
  ],
  "forbidden_actions": [
    "push_main",
    "modify_active_skills",
    "write_project_memory",
    "send_external_message"
  ],
  "expected_output": "findings_with_evidence",
  "requires_pantheon_validation": true
}
```

Hermes answers with a `ConsultationResult`.

```json
{
  "consultation_id": "consult_001",
  "status": "completed",
  "summary": "Legacy runtime components still require audit before deletion.",
  "findings": [],
  "evidence": [],
  "artifacts": [],
  "confidence": 0.84,
  "needs_pantheon_decision": true,
  "proposed_next_action": "Update reference Markdown files before code changes."
}
```

---

# 18. Anti-loop policy

Pantheon and Hermes must not create recursive consultation loops.

Rules:

```yaml
max_consultation_depth: 2
requires_new_information: true
same_consultant_repeat: false
```

Allowed pattern:

```text
Hermes consults Pantheon rules.
Hermes works.
Hermes submits result to Pantheon.
Pantheon decides.
```

Forbidden pattern:

```text
Hermes → Pantheon → Hermes → Pantheon → Hermes
```

A consultation must bring new information. Otherwise it is refused.

---

# 19. Hermes result scorecard

Each Hermes result sent to Pantheon should be scored.

```json
{
  "source_confidence": 0.90,
  "execution_confidence": 0.80,
  "scope_confidence": 0.95,
  "governance_confidence": 0.90,
  "reuse_value": 0.70
}
```

| Score | Question |
|---|---|
| source_confidence | Are the sources solid? |
| execution_confidence | Did Hermes execute correctly? |
| scope_confidence | Was the requested scope respected? |
| governance_confidence | Were Pantheon rules followed? |
| reuse_value | Should this be capitalized as memory, skill or workflow candidate? |

High `reuse_value` may trigger a candidate skill, candidate workflow or memory candidate proposal.

It must not trigger automatic promotion.

---

# 20. Event bus

Pantheon, Hermes and OpenWebUI should share standardized events.

Recommended events:

```text
run.created
run.started
agent.started
agent.completed
consultation.requested
consultation.completed
skill.draft_created
skill.candidate_created
memory.candidate_created
decision.candidate_created
veto.warning
veto.blocking
approval.required
artifact.created
run.completed
run.failed
```

OpenWebUI may display them as a timeline, graph or agent status report.

Example:

```text
Run #123 — Pantheon repo audit
├─ ZEUS                    completed
├─ ATHENA                  completed
├─ Hermes consultation      completed
├─ THEMIS                  warning
├─ APOLLO                  pending
└─ Human approval           required
```

---

# 21. Run Graph

Every significant task should be able to produce a graph.

```json
{
  "run_id": "run_123",
  "entrypoint": "openwebui",
  "router": "pantheon-router",
  "nodes": [
    {"id": "zeus", "type": "agent", "status": "completed"},
    {"id": "athena", "type": "agent", "status": "completed"},
    {"id": "hermes_consult_1", "type": "external_consultation", "status": "completed"},
    {"id": "themis", "type": "veto", "status": "warning"},
    {"id": "apollo", "type": "validation", "status": "pending"}
  ],
  "edges": [
    ["zeus", "athena"],
    ["athena", "hermes_consult_1"],
    ["hermes_consult_1", "themis"],
    ["themis", "apollo"]
  ]
}
```

This is the basis for visualizing workflow progress, agent status, consultations, blockers and approvals.

No raw chain-of-thought is displayed.

---

# 22. Memory separation

Memory must remain separated.

| Memory | Role |
|---|---|
| OpenWebUI memory | User preferences, UX comfort, lightweight personalization |
| Hermes memory | Operational experience, local skills, procedures, technical errors |
| Pantheon memory | Project memory, system memory, decisions, evidence, constraints |

Allowed bridges:

| Source | Destination | Status |
|---|---|---|
| Hermes | Pantheon | Memory candidate |
| OpenWebUI | Pantheon | User context candidate |
| Pantheon | Hermes | Limited task context |
| Pantheon | OpenWebUI | Display context |
| Hermes | OpenWebUI | Worker status |

Hermes must never write directly into Pantheon project memory.

---

# 23. Authority matrix

| Element | OpenWebUI | Hermes | Pantheon |
|---|---|---|---|
| Interface | Authority | No | No |
| Simple routing | Yes | No | Arbitration authority |
| Technical execution | No | Operational authority | Delegates |
| Project rules | Displays | Consults | Authority |
| Project memory | Displays | Candidate only | Authority |
| System memory | Displays | Candidate only | Authority |
| Experimental skills | No | Local authority | No |
| Candidate skills | Displays | Proposes | Validates |
| Active skills | Exposes | No | Authority |
| Official workflows | Triggers | Proposes | Authority |
| Decisions | Displays | Proposes | Authority |
| Vetoes | Displays | No | Authority |
| Criticality | Displays | May estimate | Authority |
| Human validation | Interface | No | Requires and traces |

---

# 24. Pantheon components to add later

Planned core layer:

```text
core/consultation/
  contracts.py
  router.py
  hermes_client.py
  policy.py
  events.py
```

Responsibilities:

| File | Role |
|---|---|
| `contracts.py` | RunContract, ConsultationRequest, ConsultationResult, EvidencePack |
| `router.py` | Decides when Hermes should be consulted |
| `hermes_client.py` | Calls Hermes once an integration mode exists |
| `policy.py` | Checks allowed actions, forbidden actions, modes and approvals |
| `events.py` | Emits events for OpenWebUI display |

Potential module package:

```text
modules/hermes_ops/
  workflows/
    hermes_self_audit.yaml
    hermes_skill_candidate_review.yaml
    hermes_upgrade_review.yaml
    hermes_failure_postmortem.yaml
  policies/
    hermes_policy.yaml
  scorecards/
    hermes_result_scorecard.yaml
  templates/
    HERMES_AUDIT_REPORT.md
    HERMES_SKILL_REVIEW.md
    HERMES_UPGRADE_PLAN.md
```

Status: planned, not implemented.

---

# 25. Minimal planned API

Pantheon side for OpenWebUI:

```http
POST /runs
GET  /runs/{run_id}
GET  /runs/{run_id}/events
GET  /runs/{run_id}/artifacts
GET  /runs/{run_id}/graph
POST /runs/{run_id}/approve
POST /runs/{run_id}/cancel
```

Pantheon side for Hermes:

```http
GET  /runtime/context-pack
GET  /runtime/capabilities
GET  /runtime/rules
GET  /status
POST /skills/candidates
POST /memory/candidates
POST /decisions/candidates
POST /consultations
```

Pantheon to Hermes:

```http
POST /hermes/tasks
GET  /hermes/tasks/{task_id}
GET  /hermes/tasks/{task_id}/artifacts
POST /hermes/tasks/{task_id}/cancel
```

Status: target API only.

---

# 26. Example: Pantheon repository audit

User request:

```text
Check my full Pantheon OS repository.
```

Flow:

1. OpenWebUI receives the request.
2. Router identifies a Pantheon repository task.
3. It routes to Hermes Pantheon Operator.
4. Hermes loads the `pantheon-os` local skill.
5. Hermes calls `GET /runtime/context-pack` when available.
6. Hermes reads recent entries in `ai_logs/`, then `docs/governance/STATUS.md`.
7. Hermes reads relevant reference Markdown files.
8. Hermes analyzes the code.
9. Hermes produces a diagnostic and Evidence Pack.
10. Hermes submits the result to Pantheon.
11. Pantheon checks documentation/code consistency.
12. THEMIS flags governance issues.
13. APOLLO validates output structure.
14. OpenWebUI displays the report, evidence and possible actions.

Expected output:

- short diagnostic;
- documentation/code inconsistencies;
- affected files;
- priority;
- documentation proposal;
- code proposal after documentation validation;
- Evidence Pack;
- recommended action.

---

# 27. Example: skill creation

User request:

```text
Create a skill for quote analysis.
```

Flow:

1. OpenWebUI routes to Hermes Pantheon Operator.
2. Hermes creates a local draft under `~/.hermes/pantheon-skill-lab/quote_review`.
3. Hermes checks existing Pantheon skills.
4. Hermes checks Hermes built-in or optional skills.
5. Hermes tests the draft on fictional examples.
6. Hermes proposes a candidate under the relevant Pantheon domain package.
7. Candidate files include `SKILL.md`, `manifest.yaml`, `examples.md`, `tests.md`, `UPDATES.md`.
8. Pantheon launches review.
9. THEMIS checks limits, risks and governance.
10. APOLLO checks structure, testability and clarity.
11. Human approval is requested when required.
12. The skill may become active only after validation.
13. OpenWebUI may then expose it.

---

# 28. Example: architecture evolution

User request:

```text
Improve adaptive orchestration.
```

Correct flow:

1. Hermes identifies a structural request.
2. Hermes consults Pantheon.
3. Hermes reads reference Markdown files.
4. Hermes checks the real code state.
5. Hermes proposes a documentation decision.
6. Pantheon validates or corrects.
7. If validated, Hermes prepares a branch.
8. Hermes proposes a patch.
9. Pantheon reviews.
10. Human validation occurs when required.

Forbidden flow:

```text
Hermes directly codes a new abstraction without documentation update.
```

---

# 29. Deployment plan

## Immediate

1. Document the OpenWebUI / Hermes / Pantheon architecture.
2. Add the rule: Hermes is operator, Pantheon is authority.
3. Define Hermes Skill Lab → Pantheon candidate → active lifecycle.
4. Define RunContract, ConsultationRequest, ConsultationResult and EvidencePack.
5. Add the interaction layer to `STATUS.md` as planned.

## Short term

1. Create the local Hermes `pantheon-os` skill.
2. Create `~/.hermes/pantheon-skill-lab`.
3. Expose a first static `/runtime/context-pack` endpoint.
4. Create a basic OpenWebUI router/action.
5. Create a first Evidence Pack template.

## Medium term

1. Add Pantheon → Hermes consultations.
2. Require Evidence Packs for candidate outputs.
3. Add Run Graph generation.
4. Add event timeline display.
5. Add THEMIS/APOLLO reviews for candidate skills.

## Long term

1. Add Hermes scorecards.
2. Add controlled automation.
3. Add full skill promotion workflows.
4. Add controlled pull request workflow.
5. Add full multi-system observability.

---

# 30. Risks and guardrails

| Risk | Guardrail |
|---|---|
| Hermes becomes implicit authority | Hermes outputs are candidates |
| Skill duplication | Pantheon alone canonizes |
| Obsolete Hermes memory | Hermes consults Context Pack |
| Pantheon/Hermes ping-pong | Anti-loop and max depth |
| OpenWebUI becomes business engine | OpenWebUI remains cockpit |
| Direct patch on main | Dedicated branch required |
| Dangerous skill activated too fast | THEMIS/APOLLO review |
| Critical decision without validation | C4/C5 + human validation |
| Abstraction bloat | Documentation first, clear gain required |
| Lost evidence | Evidence Pack required |

---

# 31. Final rule

```text
Hermes knows the protocol.
Pantheon provides the true state.
Hermes prepares.
Pantheon validates.
OpenWebUI displays and asks for approval.
```

Governance rule:

```text
Hermes never creates canonical truth.
Hermes creates candidates.
Pantheon canonizes.
```

This keeps the system powerful, extensible and controlled without duplicating runtime responsibilities.
