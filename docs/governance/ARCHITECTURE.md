# System Anatomy — Pantheon OS

> Technical reference document. Describes the real system anatomy after the Hermes-backed pivot.

---

# 1. Structural decision

Pantheon OS is a governed Domain Operating Layer.

```text
Pantheon defines and canonizes.
Hermes executes.
OpenWebUI exposes, retrieves and asks for approval.
```

Pantheon must not reimplement subsystems already handled by Hermes Agent: agent loop, prompt assembly, provider resolution, tool registry, terminal/browser/web/MCP backends, session storage, scheduler, gateways, optional skills or the Skills Hub.

Reference governance documents:

```text
APPROVALS.md
TASK_CONTRACTS.md
EVIDENCE_PACK.md
HERMES_INTEGRATION.md
KNOWLEDGE_TAXONOMY.md
MEMORY.md
MODULES.md
AGENTS.md
```

---

# 2. Layered anatomy

```text
OpenWebUI
  user cockpit
  document Knowledge surface
  approval surface

Pantheon OS
  source-of-truth Markdown
  abstract agents
  domain packages
  task contracts
  approval policy
  evidence policy
  memory policy
  Knowledge taxonomy
  Hermes integration rules
  candidate skills and workflows

Hermes Agent
  operational runtime
  executable skills
  tools
  session execution
  provider/runtime features
  local operational memory
```

Hermes is the runtime.

Pantheon is the definition, governance and domain-specialization layer.

OpenWebUI is the cockpit and Knowledge surface.

---

# 3. Domain packages

Official structure:

```text
domains/
  general/
    domain.md
    rules.md
    knowledge_policy.md
    output_formats.md
    skills/
    workflows/
    templates/
  architecture_fr/
    domain.md
    rules.md
    knowledge_policy.md
    output_formats.md
    skills/
    workflows/
    templates/
  software/
    domain.md
    rules.md
    knowledge_policy.md
    output_formats.md
    skills/
    workflows/
    templates/
```

`general` contains invariant system capabilities: triage, verification, approval risk, evidence checks, memory promotion, skill/workflow design, repository inspiration, source check and prompt system design.

`architecture_fr` contains French-speaking architecture-domain capabilities: CCTP, quotes, DPGF, notices, site reports, PLU, ERP/SDIS, responsibilities and construction contracts.

`software` contains repository, documentation, code governance, API layer, legacy audit and context export capabilities.

Rule:

```text
The French architecture domain must not be recreated under domains/architecture/.
```

---

# 4. Task contracts

Reference:

```text
TASK_CONTRACTS.md
```

A task contract defines what Hermes or Pantheon may execute for a bounded task.

It defines:

- task id;
- domain;
- purpose;
- mode;
- inputs;
- outputs;
- allowed tools;
- forbidden tools;
- approval level;
- agents;
- skills;
- memory impact;
- evidence requirement.

Rule:

```text
A task contract frames execution.
It does not authorize execution by itself.
```

---

# 5. Approval policy

Reference:

```text
APPROVALS.md
```

Criticality levels:

```text
C0 = read / diagnostic
C1 = draft / suggestion
C2 = reversible low-risk action
C3 = persistent internal change
C4 = external / contractual / financial / responsibility action
C5 = critical / irreversible / secrets / destructive
```

Rule:

```text
No persistent, external, critical or irreversible action without a visible approval path.
```

---

# 6. Evidence Pack

Reference:

```text
EVIDENCE_PACK.md
```

Consequential outputs require an Evidence Pack.

Minimum evidence frame:

```text
files_read
sources_used
commands_run
tools_used
knowledge_bases_consulted
documents_used
assumptions
unsupported_claims
limitations
outputs
approval_required
next_safe_action
```

Rule:

```text
A model statement is not evidence.
```

---

# 7. Hermes skill strategy

Before creating a Pantheon skill:

```text
1. search existing Pantheon skills;
2. search Hermes built-in or optional skills;
3. review community skills only as inspiration;
4. decide: use_existing, wrap_hermes_skill, create_candidate, reject_duplicate;
5. create only after validation.
```

Rule:

```text
Pantheon skill = domain contract + governance.
Hermes skill = executable capability.
```

If Hermes already provides a technical capability, Pantheon must not recode it. Pantheon may create a domain wrapper that defines context, inputs, outputs, approvals, privacy, memory impact and templates.

---

# 8. Skills and lifecycle

Minimal structure of a Pantheon skill:

```text
SKILL.md
manifest.yaml
examples.md
tests.md
UPDATES.md
```

`SKILL.md` is the active version.
`UPDATES.md` contains proposals.
`manifest.yaml` contains status, level, XP, policy and optional Hermes mapping.

No level changes without review, optimization and validation.

XP is allowed only for:

- real improvement;
- blockage identified;
- blockage fixed;
- method simplified;
- guardrail added.

---

# 9. Workflows

Workflows are YAML files in:

```text
domains/{domain}/workflows/*.yaml
```

They describe structured and testable procedures.

A workflow must not be a long prompt disguised as architecture.

---

# 10. Memory

Reference:

```text
MEMORY.md
```

Structure:

```text
memory/
  session/
  candidates/
  project/
  system/
```

Rules:

```text
session    = temporary
candidates = persisted but not validated
project    = validated project context
system     = validated rules, methods and patterns
```

Cycle:

```text
SESSION → CANDIDATES → Evidence Pack → validation → PROJECT or SYSTEM
```

Memory promotion is at least C3.

No automatic promotion.

---

# 11. Knowledge taxonomy

Reference:

```text
KNOWLEDGE_TAXONOMY.md
```

OpenWebUI Knowledge is not Pantheon memory.

Rule:

```text
Documents are knowledge.
Validated reusable facts become memory candidates.
Pantheon alone canonizes memory.
```

Initial Knowledge collections use `architecture_fr`, not `architecture`.

---

# 12. Privacy by default

No real data from private conversations, real projects, clients, companies, construction sites, addresses, persons or identifiable situations may be written into the repository.

Examples, tests and templates must be fictional, neutral and non-traceable.

Every memory promotion must check anonymization.

---

# 13. Change triage

Before any modification, Pantheon must classify the request:

```text
situation
project_memory
system_memory
skill_update
workflow_update
new_capability
policy_update
code_patch
external_action
```

The classification determines:

- task contract;
- approval level;
- agents;
- skills;
- Evidence Pack requirement;
- next safe action.

---

# 14. Runtime security

Risky capabilities remain on the Hermes side but must be policy-gated by Pantheon:

- browser automation;
- terminal;
- web actions;
- MCP;
- file mutations;
- scheduler;
- gateways;
- memory providers;
- optional/community skills.

Minimal rules:

- sandbox or Docker for risky tools;
- no Docker socket at startup;
- no secrets access without policy;
- no external action without approval;
- visible execution required;
- logs and traceability.

---

# 15. Hermes context strategy

Reference:

```text
HERMES_INTEGRATION.md
```

Pantheon provides controlled context exports:

```text
hermes/context/
  pantheon_context.md
  agents_context.md
  memory_context.md
  rules_context.md
  architecture_fr_context.md
  software_context.md
  tools_policy.md
```

These files do not replace the reference Markdown files. They export a compact operational version for Hermes.

---

# 16. OpenWebUI / Hermes / Pantheon operating protocol

Pantheon uses an explicit operating protocol for the three-system setup:

```text
OpenWebUI = user cockpit
Hermes Agent = privileged operational worker
Pantheon OS = governed domain authority and source of truth
```

Corrected rule:

```text
Hermes operates.
Pantheon arbitrates.
OpenWebUI pilots and displays.
```

Hermes may inspect, prepare, test, research, draft local skills, propose patches, create candidate assets and return evidence.

Hermes must not canonize.

Pantheon remains the authority for:

- active skills;
- active workflows;
- project memory;
- system memory;
- decisions;
- governance rules;
- validations;
- vetoes;
- criticality;
- candidate promotion.

OpenWebUI remains the cockpit and approval surface.

Detailed protocol:

```text
operations/openwebui_hermes_pantheon.md
```

Status: documented target architecture, not fully implemented.

---

# 17. Installation and operations

Target environment: NAS with Portainer, existing OpenWebUI, existing PostgreSQL and Ollama on a LAN PC.

Rules:

- never overwrite an existing stack;
- detect before installing;
- isolate Hermes Lab;
- do not expose PostgreSQL unnecessarily;
- do not use unstable Docker tags in production;
- test locally before merge.

---

# 18. Existing code

The repository still contains elements from the previous autonomous architecture: FastAPI apps, registries, workflow loader, approvals, installer UI, migrations and legacy tests.

Status: legacy to audit.

No automatic deletion before diagnosis.

Target audit document:

```text
CODE_AUDIT_POST_PIVOT.md
```

---

# 19. Final rule

Pantheon must remain simpler than the runtime it governs.

If a capability already exists in Hermes, Pantheon must govern it, not duplicate it.
