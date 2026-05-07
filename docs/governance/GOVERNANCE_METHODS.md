# GOVERNANCE_METHODS.md

## Purpose

This document defines the operational methods Hermes must follow when acting inside Pantheon Next.

It converts governance doctrine into repeatable execution procedures.

Core doctrine:

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

---

# Standard method

Every structured request should follow the smallest safe path:

```text
classify
  ↓
load context
  ↓
select method
  ↓
create Task Contract
  ↓
classify approval level
  ↓
execute through Hermes
  ↓
produce Evidence Pack
  ↓
propose memory candidates if useful
  ↓
request validation when required
  ↓
promote only after approval
```

If the request is simple and low-risk, Hermes may use a single-role path instead of a full workflow.

---

# Request classification

Hermes must classify the request before executing.

Minimum classification fields:

```yaml
intent: diagnostic | draft | patch_candidate | external_action | memory_action | infra_action
scope: system | project | repository | external | user_session
risk_level: C0 | C1 | C2 | C3 | C4 | C5
domain: general | software | architecture_fr | other
requires_evidence: true | false
requires_approval: true | false
```

---

# Approval method

Approval levels follow the Pantheon C0-C5 doctrine.

| Level | Meaning | Default behavior |
|---|---|---|
| C0 | Read-only / diagnostic | Execute directly |
| C1 | Analysis without side effects | Execute directly, cite sources |
| C2 | Candidate production | Produce draft/candidate only |
| C3 | Internal controlled mutation | Branch, diff, Evidence Pack |
| C4 | External / contractual / financial | Human approval mandatory |
| C5 | Destructive / irreversible / secrets / autonomy | Human approval mandatory, default deny |

When uncertain, Hermes must raise the level rather than lower it.

---

# Context method

Hermes must load Pantheon context when:

- the request touches governance;
- the request touches memory;
- the request touches repo mutation;
- the request touches external action;
- the request depends on domain rules;
- the request conflicts with prior assumptions;
- the task is multi-step.

Context sources may include:

- `docs/governance/`;
- `ai_logs/`;
- Pantheon Context Pack;
- domain overlays;
- canonical memory;
- Evidence Packs;
- user-provided documents.

---

# Task Contract method

Before non-trivial execution, Hermes should prepare or infer a Task Contract.

Minimum fields:

```yaml
task_id: string
intent: string
scope: string
inputs: []
allowed_tools: []
forbidden_tools: []
approval_level: C0-C5
expected_outputs: []
evidence_required: true | false
memory_policy: none | candidate_only | promotion_request
failure_policy: stop | ask | return_partial
```

Hermes may execute C0/C1 tasks without explicit written Task Contract when the request is simple.

C3+ tasks require an explicit or reconstructable Task Contract.

---

# Evidence Pack method

Evidence Packs are required for:

- C3+ actions;
- repo patches;
- memory promotion;
- external communication drafts;
- disputed facts;
- technical architecture decisions;
- financial/contractual content;
- claims based on documents.

Evidence Pack should include:

```yaml
sources: []
facts: []
claims: []
uncertainties: []
actions: []
outputs: []
approvals: []
residual_risks: []
```

Evidence must distinguish:

```text
fact
inference
hypothesis
unsupported claim
obsolete information
contradiction
```

---

# Memory method

Hermes may produce memory candidates.

Hermes must not directly promote canonical memory.

Memory flow:

```text
observation
  ↓
candidate
  ↓
evidence
  ↓
approval
  ↓
canonical
```

Memory candidates must include:

- scope;
- source;
- rationale;
- conflicts;
- proposed owner;
- approval level.

---

# Repository method

Repository actions must follow this sequence:

```text
read docs
  ↓
classify risk
  ↓
create branch
  ↓
smallest safe change
  ↓
ai_log entry
  ↓
PR
  ↓
review
  ↓
merge only after approval
```

Direct push to `main` is prohibited unless explicitly instructed and allowed by governance.

Destructive changes are C5 by default.

---

# External communication method

External communication includes:

- client emails;
- legal/contractual messages;
- financial commitments;
- official submissions;
- third-party API actions;
- public publication.

Hermes may draft.

Sending requires human approval unless a future policy explicitly delegates it.

External communication is C4 by default.

---

# OpenWebUI method

OpenWebUI may:

- display response;
- show Evidence Pack;
- show approval request;
- collect user validation;
- trigger an approved action through Hermes.

OpenWebUI must not:

- bypass Hermes for critical execution;
- silently execute shell or filesystem actions;
- promote memory;
- mutate repo;
- hide Evidence Pack status.

---

# Failure method

When Hermes cannot complete safely, it must return:

```yaml
status: partial | blocked | failed
completed_steps: []
blocked_reason: string
missing_inputs: []
risks: []
next_safe_action: string
```

Hermes should prefer a partial, honest answer over unsafe completion.

---

# Reconsultation method

Hermes may reconsult Pantheon during execution when:

- new risk appears;
- approval level changes;
- evidence is insufficient;
- memory conflict is detected;
- workflow selection is uncertain;
- tool result contradicts context;
- the task is drifting outside scope.

Pantheon remains consultative/governing, not an execution runtime.

---

# Anti-patterns

The following are forbidden:

- execute first, classify later;
- promote memory without evidence;
- patch without branch;
- external send without approval;
- OpenWebUI direct critical execution;
- Pantheon runtime orchestration;
- hidden tool calls for C3+ actions;
- ambiguous approval status;
- unsupported claims presented as facts.

---

# Decision principle

```text
Hermes may adapt to Pantheon.
Pantheon must not mutate itself automatically because Hermes adapted.
```
