# EVIDENCE PACK — Pantheon OS

> Reference schema for proving what a result is based on.

---

# 1. Purpose

An Evidence Pack is the audit trail attached to any significant Pantheon or Hermes output.

It records what was read, used, assumed, produced, left unsupported, retried, remediated or left pending.

Rule:

```text
A consequential output without evidence is a draft, not a validated result.
```

---

# 2. Evidence Pack levels

Pantheon uses two levels:

```text
minimum_evidence_pack
extended_evidence_pack
```

The minimum level is required for most consequential outputs.

The extended level is required when the task involves external tools, PDF processing, Knowledge ingestion, plugin installation, memory promotion, self-evolution, before/after comparison, fallback or remediation.

---

# 3. Minimum Evidence Pack

| Field | Required | Purpose |
|---|---:|---|
| `id` | yes | Stable evidence identifier |
| `task_id` | yes | Related task contract or task name |
| `date` | yes | Date of execution or analysis |
| `operator` | yes | Human, Hermes, Pantheon workflow or other operator |
| `files_read` | yes | Repository or local files inspected |
| `sources_used` | yes | External, regulatory, web or documentation sources used |
| `commands_run` | yes | Commands executed |
| `tools_used` | yes | Tools or integrations used |
| `knowledge_bases_consulted` | yes | OpenWebUI or other Knowledge Bases consulted |
| `documents_used` | yes | Project or system documents used |
| `assumptions` | yes | Explicit assumptions made |
| `unsupported_claims` | yes | Claims that still lack direct proof |
| `limitations` | yes | Missing data, scope limits, tool failures |
| `outputs` | yes | Files, patches, drafts, reports or candidates produced |
| `approval_required` | yes | Approval level or user validation needed |
| `next_safe_action` | yes | Recommended next action that does not exceed approval |

Generic shape:

```yaml
evidence_pack:
  id: null
  task_id: null
  date: null
  operator: null
  files_read: []
  sources_used: []
  commands_run: []
  tools_used: []
  knowledge_bases_consulted: []
  documents_used: []
  assumptions: []
  unsupported_claims: []
  limitations: []
  outputs: []
  approval_required: null
  next_safe_action: null
```

---

# 4. Extended Evidence Pack

The extended Evidence Pack adds fields for higher-risk or more structured operations.

| Field | Required when relevant | Purpose |
|---|---:|---|
| `source_repository` | yes | Repository or external project used as reference |
| `source_excerpt` | yes | Short excerpt or pointer supporting the conclusion |
| `entity_candidates` | yes | Candidate entities extracted from documents |
| `event_candidates` | yes | Candidate events extracted from documents |
| `relationship_candidates` | yes | Candidate relationships between entities/events |
| `before_after_metrics` | yes | Metrics for evolution, patch, compression or optimization |
| `risk_level` | yes | C0-C5 risk level |
| `rollback_plan` | yes | Reversal path |
| `fallbacks` | yes | Failed actions, retries and alternatives |
| `remediation` | yes | Issue analysis and patch candidate proposal |

Extended shape:

```yaml
extended_evidence_pack:
  source_repository: null
  source_excerpt: null
  entity_candidates: []
  event_candidates: []
  relationship_candidates: []
  before_after_metrics: []
  risk_level: null
  rollback_plan: null
  fallbacks: []
  remediation: null
```

---

# 5. Fallback evidence

Every fallback, retry or alternative path must be recorded.

```yaml
fallbacks:
  - original_action: ""
    original_tool: ""
    failure_reason: ""
    fallback_action: ""
    fallback_tool: ""
    risk_delta: same | lower | higher
    approval_required: true
    approved: false
```

Rules:

- same or lower risk fallback may proceed only if allowed by task contract;
- higher-risk fallback requires new approval;
- unallowlisted fallback is blocked;
- fallback cannot bypass approval, allowlist, privacy, memory or tool policy.

---

# 6. Remediation evidence

Every remediation candidate must be recorded.

```yaml
remediation:
  issue_detected: true
  issue_summary: ""
  suspected_cause: ""
  affected_component: ""
  proposed_fix: ""
  patch_candidate: ""
  risk_level: C0
  approval_required: false
  applied: false
```

Rules:

- remediation may propose;
- remediation must not auto-apply;
- patch candidates require approval when they mutate files, skills, workflows, memory, policies, external tools or runtime configuration;
- remediation cannot be used to bypass a blocked action.

---

# 6b. Role signal traceability

When the task involved structured role-to-role messages, the Evidence Pack must reference those signals.

The signals themselves are defined in `ROLE_SIGNALS.md` and `ROLE_SIGNAL_PROFILES.md`.

The Evidence Pack does not duplicate raw signal payloads. It records the artifacts that prove governance was respected.

| Field | Required when relevant | Purpose |
|---|---:|---|
| `role_signals` | yes | List of `role_signal` ids with sender, recipient, type and risk level |
| `addressed_role_signals` | yes | List of IRIS-mediated `addressed_role_signal` ids with mediator, sender substance ref and addressed profile |
| `role_consultations` | yes | List of `role_consultation` ids with reason, expected outputs, max rounds and final status |
| `format_reminder_request` | yes | List of `format_reminder_request` ids and the addressed role |
| `format_reminder_response` | yes | List of structure-only responses received |
| `format_blocked` | yes | List of `format_blocked` events and the role they were rerouted to |
| `handoff_signals` | yes | List of handoffs between active roles |
| `veto_signal` | yes | THEMIS veto signals raised, including approval impact |
| `stop_gate_signal` | yes | APOLLO stop gate decisions and unresolved items |
| `workflow_revision_signal` | yes | Revision signals emitted, the recommendation and the resulting arbitration |

Role signal evidence shape:

```yaml
role_signal_traceability:
  role_signals: []
  addressed_role_signals: []
  role_consultations: []
  format_reminder_request: []
  format_reminder_response: []
  format_blocked: []
  handoff_signals: []
  veto_signal: []
  stop_gate_signal: []
  workflow_revision_signal: []
```

Rules:

```text
Role signal payloads must remain bounded.
Raw chain-of-thought is forbidden in the Evidence Pack.
Risk levels recorded in evidence must match the risk levels emitted in the original signal.
Limitations declared in a signal must remain visible in the Evidence Pack.
A consequential addressed_role_signal must reference the underlying role_signal substance, not replace it.
A format_reminder_request must remain structure-only; any decision-bearing response is invalid evidence and must be flagged.
```

---

# 7. When Evidence Pack is mandatory

Evidence Pack is mandatory for:

- repository audit;
- OCR / PDF processing;
- OpenWebUI Knowledge ingestion;
- quote / CCTP analysis;
- DPGF or quantity analysis;
- Markdown modification;
- code patch proposal;
- skill proposal;
- workflow proposal;
- memory candidate;
- plugin installation;
- external tool installation;
- self-evolution;
- client-facing communication;
- contractual or responsibility analysis;
- legacy audit;
- fallback;
- remediation candidate;
- any output that may become canonical Pantheon truth.

---

# 8. Source discipline

Evidence must distinguish:

```text
file read
source used
document used
Knowledge Base consulted
assumption
unsupported claim
fallback
remediation
```

A model statement is not evidence.

A previous conversation is not canonical evidence unless it was already promoted to validated memory or is visible in the active session and disclosed as context.

---

# 9. Approval discipline

The Evidence Pack must state:

- whether approval is required;
- which criticality level applies;
- which action is safe next;
- which actions remain forbidden.

Example:

```yaml
approval_required:
  level: C3
  reason: "Markdown files were modified on a branch."
next_safe_action: "Run tests and review the diff before merge."
```

---

# 10. RAG discipline

When a result uses Knowledge Bases, the Evidence Pack must list:

- Knowledge Bases consulted;
- documents actually used;
- missing documents;
- source reliability level when available;
- whether cross-project data was used.

Rule:

```text
No cross-project document mixing without explicit trace or approval.
```

---

# 11. PDF discipline

When PDF processing is involved, the Evidence Pack must list:

- source PDF path or identifier;
- working copy path or identifier;
- metadata checked;
- text layer status;
- OCR action if any;
- compression or transformation if any;
- redaction/sanitization if any;
- whether source PDF was preserved;
- approval before Knowledge ingestion.

Rule:

```text
Never overwrite the source PDF.
```

---

# 12. Limitations discipline

Limitations are not optional.

If no test was run, say:

```text
No tests were run.
```

If a source could not be checked, say:

```text
Source not verified.
```

If a conclusion is inferred, say:

```text
Inference, not directly proven by source.
```

If a fallback was not attempted, say why.

If remediation was not applied, say why.

---

# 13. Final rule

```text
Evidence Pack first. Canonization later.
```
