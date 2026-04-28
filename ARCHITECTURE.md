# System Anatomy — Pantheon OS

> Technical reference document. Describes the real system anatomy after the Hermes-backed pivot.

---

# 1. Structural decision

Pantheon OS is a Domain Operating Layer.

```text
Pantheon defines.
Hermes executes.
OpenWebUI exposes and retrieves.
```

Pantheon must not reimplement subsystems already handled by Hermes Agent: agent loop, prompt assembly, provider resolution, tool registry, terminal/browser/web/MCP backends, session storage, scheduler, gateways, optional skills or the Skills Hub.

---

# 2. Layered anatomy

```text
OpenWebUI
  user interface
  document knowledge

Pantheon OS
  abstract agents
  domain packages
  domain skills
  workflows
  memory policies
  approval policies
  Hermes skill policy

Hermes Agent
  agent loop
  prompt assembly
  runtime provider resolution
  tool registry
  session storage
  cron scheduler
  gateways
  optional skills
```

Hermes is the runtime. Pantheon is the definition, governance and domain-specialization layer.

---

# 3. Domain packages

Official structure:

```text
domains/
  general/
    domain.md
    skills/
    workflows/
    templates/
  architecture_fr/
    domain.md
    skills/
    workflows/
    templates/
  software/
    domain.md
    skills/
    workflows/
    templates/
```

`general` contains invariant system capabilities: triage, verification, on-the-fly creation, memory promotion, skill/workflow design, repository inspiration, source check and prompt system design.

`architecture_fr` contains French-speaking architecture-domain capabilities: CCTP, quotes, DPGF, notices, site reports, PLU, ERP/SDIS, responsibilities and construction contracts.

Rule: the French architecture domain must not be recreated under `domains/architecture/`.

---

# 4. Hermes skill strategy

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

# 5. Skills and lifecycle

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

# 6. Workflows

Workflows are YAML files in:

```text
domains/{domain}/workflows/*.yaml
```

They describe structured and testable procedures.

A workflow must not be a long prompt disguised as architecture.

---

# 7. Memory

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
SESSION → CANDIDATES → validation → PROJECT or SYSTEM
```

No automatic promotion.

---

# 8. Privacy by default

No real data from private conversations, real projects, clients, companies, construction sites, addresses, persons or identifiable situations may be written into the repository.

Examples, tests and templates must be fictional, neutral and non-traceable.

Every memory promotion must check anonymization.

---

# 9. Change triage

Before any modification, Pantheon must classify the request:

```text
situation
project_memory
system_memory
skill_update
workflow_update
new_capability
policy_update
```

The classification determines the target and the validation level.

---

# 10. Runtime security

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

# 11. Hermes context strategy

Hermes assembles prompts from personality, memory, skills, context files, tool guidance and model instructions.

Pantheon therefore provides controlled context exports:

```text
hermes/context/
  pantheon_context.md
  agents_context.md
  memory_context.md
  rules_context.md
  architecture_fr_context.md
  software_context.md
```

These files do not replace the reference Markdown files. They export a stable operational version for Hermes.

---

# 12. OpenWebUI / Hermes / Pantheon operating protocol

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

# 13. Installation and operations

Target environment: NAS with Portainer, existing OpenWebUI, existing PostgreSQL and Ollama on a LAN PC.

Rules:

- never overwrite an existing stack;
- detect before installing;
- isolate Hermes Lab;
- do not expose PostgreSQL unnecessarily;
- do not use unstable Docker tags in production;
- test locally before merge.

---

# 14. Existing code

The repository still contains elements from the previous autonomous architecture: FastAPI apps, registries, workflow loader, approvals, installer UI, migrations and legacy tests.

Status: legacy to audit.

No automatic deletion before diagnosis.

---

# 15. Final rule

Pantheon must remain simpler than the runtime it governs.

If a capability already exists in Hermes, Pantheon must govern it, not duplicate it.
