# HERMES INTEGRATION — Pantheon OS

> Reference document for how Hermes Agent consumes Pantheon OS without becoming Pantheon’s authority.

---

# 1. Purpose

`HERMES_INTEGRATION.md` defines the boundary between Pantheon OS and Hermes Agent.

Core rule:

```text
Hermes executes capabilities.
Pantheon defines, governs and canonizes.
OpenWebUI exposes the interface and knowledge surface.
```

Hermes must know the Pantheon operating protocol. It must not keep a stale copy of Pantheon truth.

---

# 2. Authority model

| Layer | Role | Authority |
|---|---|---|
| OpenWebUI | User cockpit, chat, routing, Knowledge UI, approvals | Interface only |
| Hermes Agent | Operational worker, local skills, repository work, tool execution | Local execution only |
| Pantheon OS | Reference docs, canonical skills, workflows, memory, approvals | Final authority |

Short rule:

```text
Hermes proposes.
Pantheon canonizes.
```

---

# 3. What Pantheon provides to Hermes

Pantheon provides:

- reference Markdown files;
- runtime Context Pack;
- context exports;
- task contracts;
- approval policy;
- tool policy;
- evidence requirements;
- memory policy;
- skill lifecycle rules;
- domain boundaries.

Hermes consumes these to execute safely.

---

# 4. What Hermes may do

Hermes may:

- read repository files;
- compare documentation and code;
- run safe tests when scoped;
- prepare candidate patches;
- draft local skills;
- propose Pantheon skill candidates;
- propose memory candidates;
- produce Evidence Packs;
- inspect external repositories as inspiration;
- diagnose local API, Docker, RAG or CI issues when authorized.

---

# 5. What Hermes must not do

Hermes must not:

- push directly to `main`;
- mutate validated project memory;
- mutate validated system memory;
- promote a skill to active;
- change active workflows directly;
- create final decisions;
- bypass `APPROVALS.md`;
- bypass THEMIS, APOLLO or human validation when required;
- read undocumented internal state unless policy explicitly allows it;
- access secrets or Docker socket by default;
- send external communication without explicit approval.

---

# 6. Context exports

Pantheon may expose compact context files for Hermes.

Target structure:

```text
hermes/context/
  pantheon_context.md
  agents_context.md
  rules_context.md
  memory_context.md
  architecture_fr_context.md
  software_context.md
  tools_policy.md
```

Rules:

- short;
- operational;
- no real project data;
- no private client data;
- no identifiable conversation data;
- does not replace the reference Markdown files;
- used only to guide Hermes execution.

---

# 7. Runtime Context Pack

Pantheon exposes a compact API context pack:

```http
GET /runtime/context-pack
```

The Context Pack is an orientation layer. It does not replace:

- `AI_LOG.md`;
- `STATUS.md`;
- `README.md`;
- `ARCHITECTURE.md`;
- `MODULES.md`;
- `AGENTS.md`;
- `MEMORY.md`;
- `ROADMAP.md`;
- `APPROVALS.md`;
- `TASK_CONTRACTS.md`;
- `EVIDENCE_PACK.md`.

---

# 8. Local Hermes skill

Repository template:

```text
hermes/templates/pantheon-os/
```

Target local installation:

```text
~/.hermes/skills/pantheon-os/
```

This skill is local to Hermes. It is not a Pantheon canonical skill.

---

# 9. Task execution flow

```text
User request
→ OpenWebUI
→ Pantheon Router / task contract
→ approval classification
→ optional Hermes delegation
→ Hermes executes within contract
→ Evidence Pack returned
→ THEMIS / APOLLO review if required
→ OpenWebUI displays result and approval options
→ Pantheon canonizes only after validation
```

---

# 10. Hermes outputs

Hermes outputs are candidates by default:

| Output | Status |
|---|---|
| Audit report | artifact |
| Patch | candidate patch |
| Skill | local draft or Pantheon candidate |
| Workflow | workflow candidate |
| Memory | memory candidate |
| Decision | decision candidate |
| Documentation change | documentation patch candidate |
| Code change | code patch candidate |

---

# 11. Approval alignment

Hermes must respect `APPROVALS.md`.

Examples:

| Hermes action | Level |
|---|---:|
| read repository file | C0 |
| draft report | C1 |
| write candidate file | C3 |
| run safe diagnostic command | C3 |
| send external message | C4 |
| access secrets | C5 |
| use Docker socket | C5 |

---

# 12. Final rule

```text
Hermes is the operator.
Pantheon is the authority.
OpenWebUI is the cockpit.
```
