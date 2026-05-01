# Pantheon Next — Claude Code guidance

> Repository guidance for Claude Code agents.
> This file is intentionally aligned with the Hermes-backed Pantheon Next pivot.

---

## 1. Operating doctrine

Pantheon Next is not an autonomous agent runtime.

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

Pantheon Next provides governance, domain definitions, task contracts, approval rules, Evidence Packs, memory policy, Knowledge taxonomy, candidate skill/workflow lifecycle and context exports.

Hermes provides execution capabilities.

OpenWebUI provides the cockpit, Knowledge surface, result display and human validation surface.

---

## 2. Mandatory sequence before repository work

1. Read `ai_logs/README.md`.
2. Read recent `ai_logs/*.md` entries when relevant.
3. Read `docs/governance/STATUS.md`.
4. Read the relevant governance documents before modifying code.
5. Treat Markdown governance files as source of truth.
6. If code contradicts Markdown, Markdown wins.
7. If code is technically better than Markdown, update Markdown first.
8. Never push directly to `main`.
9. Work on a dedicated branch.
10. Add an `ai_logs/YYYY-MM-DD-slug.md` entry after any meaningful intervention.

---

## 3. Source-of-truth documents

Canonical governance path:

```text
docs/governance/
```

Core documents:

```text
STATUS.md
ROADMAP.md
ARCHITECTURE.md
MODULES.md
AGENTS.md
MEMORY.md
APPROVALS.md
TASK_CONTRACTS.md
EVIDENCE_PACK.md
HERMES_INTEGRATION.md
OPENWEBUI_INTEGRATION.md
EXTERNAL_TOOLS_POLICY.md
KNOWLEDGE_TAXONOMY.md
CODE_AUDIT_POST_PIVOT.md
PRE_REFACTOR_ARCHITECTURE_FINDINGS.md
WORKFLOW_SCHEMA.md
SKILL_LIFECYCLE.md
MEMORY_EVENT_SCHEMA.md
```

Root entry points:

```text
README.md
CLAUDE.md
CHANGELOG.md
VERSION
```

---

## 4. Current architecture boundary

Allowed Pantheon responsibilities:

- expose domain definitions;
- expose context packs;
- define task contracts;
- classify approvals;
- define Evidence Pack requirements;
- define memory promotion rules;
- define Knowledge source policy;
- define domain packages;
- define candidate skills and workflows;
- classify legacy code before reuse.

Forbidden Pantheon drift:

```text
Execution Engine
Agent Runtime
Tool Runtime
LLM Provider Router
Scheduler
LangGraph central orchestrator
memory auto-promotion
self-evolution auto-merge
plugin batch install
Docker socket access
secret access by default
public admin dashboard without auth/VPN
```

---

## 5. Repository areas

```text
ai_logs/                         AI intervention logs
docs/governance/                 governance source of truth
domains/general/                 invariant/general domain capabilities
domains/architecture_fr/         French architecture/MOE domain
domains/software/                software/repo governance domain
hermes/                          Hermes policy, templates, external repo notes
operations/                      operating protocols and future ops docs
platform/api/pantheon_domain/    lightweight Domain Layer API
platform/api/pantheon_runtime/   context export only; not a runtime authority
platform/api/apps/               legacy/MVP apps to audit before reuse
platform/api/core/               legacy contracts/services; extract useful schemas carefully
legacy/                          archived code; never import into active path
```

---

## 6. Code audit rule

Before modifying legacy code, classify it in or against:

```text
docs/governance/CODE_AUDIT_POST_PIVOT.md
```

Allowed audit decisions:

```text
keep
reorient
archive
delete_later
to_verify
legacy
```

Do not delete useful legacy code before diagnosis.

Do not reactivate the old autonomous runtime path by accident.

---

## 7. Existing code assets worth preserving

See:

```text
docs/governance/PRE_REFACTOR_ARCHITECTURE_FINDINGS.md
```

Important assets to preserve or reclassify:

- Domain Layer API;
- context-pack endpoint;
- manifest contracts;
- task/workflow contracts;
- approval queue;
- hybrid RAG / RRF retrieval;
- OCR fallback pattern;
- circuit breaker;
- trusted source registry;
- Evidence trace fields from agent runs;
- memory supersession model;
- Hermes skill lifecycle and XP policy.

These are patterns, schemas and guardrails to extract. They do not justify reviving the old runtime.

---

## 8. Domains and naming

Use:

```text
domains/general
domains/architecture_fr
domains/software
memory/system
```

Do not recreate:

```text
domains/architecture
skills/generic
workflows/generic
memory/agency
agency memory
```

---

## 9. Task / approval / evidence discipline

Use C0-C5:

```text
C0 = read / diagnostic
C1 = draft / suggestion
C2 = reversible low-risk action
C3 = persistent internal change
C4 = external / contractual / financial / responsibility action
C5 = critical / irreversible / secrets / destructive
```

Consequential work requires an Evidence Pack.

A model statement is not evidence.

---

## 10. Memory discipline

Memory flow:

```text
session
→ candidates
→ Evidence Pack
→ C3+ review
→ project or system
```

Rules:

- no automatic promotion;
- no Hermes local memory as Pantheon truth;
- no OpenWebUI Knowledge as Pantheon memory;
- no real private project/client data in repo examples;
- use fictional examples and tests.

---

## 11. Installation and compose warning

`docker-compose.yml` is a legacy/MVP stack until the post-pivot deployment model is rewritten.

Do not assume it represents the final target wiring.

Target direction:

```text
OpenWebUI → Hermes Gateway → Pantheon Context Pack / Domain API
```

Pantheon API is not the final OpenAI-compatible model backend.

---

## 12. Final rule

```text
Documentation first.
Contracts before execution.
Evidence before conclusion.
Candidates before canonization.
```
