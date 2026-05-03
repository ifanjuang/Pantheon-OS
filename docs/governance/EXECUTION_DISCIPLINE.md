# EXECUTION DISCIPLINE — Pantheon Next

> Minimal execution discipline for Pantheon contributors, Hermes executions and AI-assisted repository work.
>
> This document is inspired by external coding-agent discipline patterns, including `forrestchang/andrej-karpathy-skills`, but it is rewritten as Pantheon governance doctrine.

---

## 1. Principle

Pantheon does not reward complexity.

Every execution path must choose the smallest safe path that satisfies the request.

```text
single role before workflow
solo before dependency graph
template before new abstraction
candidate before canonical
patch before merge
evidence before assertion
```

The goal is not to make every request ceremonial.

The goal is to avoid uncontrolled assumptions, unnecessary abstractions, hidden mutations and unsupported conclusions.

---

## 2. Scope

This doctrine applies to:

```text
ChatGPT interventions
Claude interventions
Hermes Agent executions
candidate skill reviews
workflow/session adaptations
repository documentation changes
future code patches
external option reviews
```

It does not create runtime behavior by itself.

It is a governance and contribution discipline.

---

## 3. Core rules

### 3.1 Think before executing

Before modifying files or asking Hermes to execute:

```text
identify the user objective
identify the minimum sufficient path
identify uncertainty
identify required sources
identify approval level
identify whether a workflow is actually needed
```

Do not proceed from a hidden assumption when a visible uncertainty matters.

Use explicit status markers:

```text
À vérifier
Partiel
Non implémenté
Implémenté mais non documenté
Documenté mais non implémenté
Obsolète
Contradictoire
```

### 3.2 Simplicity first

Prefer:

```text
single_role_path over workflow
existing workflow template over generated workflow
existing skill over new skill
small patch over broad refactor
one focused PR over mixed changes
read-only diagnosis before mutation
```

Do not create a new abstraction unless it gives a clear governance, auditability or execution benefit.

### 3.3 Surgical changes

When editing the repository:

```text
touch only files needed for the objective
avoid opportunistic cleanup
avoid unrelated formatting churn
avoid rewriting large docs when an additive patch is enough
avoid mixing code, governance, domain and operations changes in one PR
```

If a file is large or central, prefer a focused follow-up PR rather than broad churn.

### 3.4 Goal-driven execution

Before execution, define success criteria.

Examples:

```text
The PR adds one governance document and indexes it.
The skill remains candidate.
The workflow remains template-only.
No runtime behavior changes.
No private data enters the repo.
The output includes Evidence Pack requirements.
```

A task is incomplete if it cannot say what success would look like.

---

## 4. Single-role path before workflow

Not every question needs a workflow.

Use a `single_role_path` when a single Pantheon Role can answer safely.

Examples:

```text
IRIS rewrites a short draft without sending it.
ARGOS extracts one fact from a provided source.
ATHENA structures a simple plan.
THEMIS classifies an approval level.
APOLLO checks a short answer for unsupported claims.
```

Escalate to a workflow when:

```text
multiple roles are required
multiple sources must be reconciled
external communication is requested
approval level rises
memory could be affected
file mutation is requested
technical, contractual, financial or regulatory exposure appears
```

Reference:

```text
WORKFLOW_SCHEMA.md
WORKFLOW_ADAPTATION.md
domains/general/skills/adaptive_orchestration/SKILL.md
```

---

## 5. Anti-overengineering guardrails

A proposal is overengineered if it:

```text
creates a workflow where one role is enough
creates a new skill where a note or template is enough
creates a new runtime adapter before the current runtime works
creates a dashboard before simple API/state is available
creates persistent storage before the schema is proven
creates automated execution before approval/evidence paths exist
```

Preferred sequence:

```text
document
example
candidate
review
minimal implementation
smoke test
evaluation
promotion
```

---

## 6. Evidence discipline

No consequential output should hide its proof standard.

For a consequential answer or patch, record:

```text
files read
sources used
assumptions
limitations
unsupported claims
approval required
next safe action
```

If evidence is missing, say so.

Do not convert uncertainty into confident prose.

---

## 7. Repository intervention discipline

Before any significant repository change:

```text
read ai_logs/README.md
read docs/governance/STATUS.md
read relevant governance docs
work on a dedicated branch
avoid main direct push
add ai_logs entry
state tests or state not run
```

PR body must include:

```text
objective
files changed
guardrails
runtime impact
tests
follow-up
```

For documentation-only PRs, explicitly state:

```text
No code changed.
No runtime behavior changed.
No endpoint added.
No dependency added.
No private project/client data added.
```

---

## 8. Hermes execution discipline

Hermes may execute, but only inside the frame.

Hermes should:

```text
receive a Task Contract when risk requires it
use the smallest allowed toolset
emit structured outputs when expected
emit Evidence Pack fragments
emit workflow_revision_signal when current path no longer fits
stop when approval is required
```

Hermes must not:

```text
canonize memory
canonize workflows
activate skills
send external communications without approval
silently switch to unallowlisted tools
mutate files outside the task frame
```

---

## 9. Claude / coding-agent discipline

Claude or another coding agent must:

```text
work on an explicit branch
stay inside the assigned scope
avoid touching governance files reserved for another intervention
avoid unrelated refactors
avoid inventing implementation details not requested
prefer additive docs when doctrine is unclear
log intervention in ai_logs
```

If the task becomes broader than expected, it should stop with a diagnostic or propose a follow-up.

---

## 10. Review checklist

Before approving a PR:

```text
Does it solve the stated objective?
Does it touch only necessary files?
Does it avoid runtime drift?
Does it preserve OpenWebUI / Hermes / Pantheon boundaries?
Does it avoid real private data?
Does it mark candidate status where appropriate?
Does it specify Evidence Pack and approvals where consequential?
Does it avoid unnecessary workflow creation?
Does it leave clear next action?
```

---

## 11. Final rule

```text
Use the smallest safe path.
Escalate only when the task requires it.
Never hide uncertainty.
Never let execution convenience override governance.
```
