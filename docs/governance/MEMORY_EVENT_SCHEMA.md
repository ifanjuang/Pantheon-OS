# MEMORY EVENT SCHEMA — Pantheon Next

> Candidate schema for memory events and memory candidates.
> This document prevents automatic memory promotion while preserving useful fields found in the legacy runtime.

---

## 1. Principle

Memory events are not memory.

They are structured candidates that may later become project or system memory after evidence and validation.

```text
session material
→ memory event
→ memory candidate
→ Evidence Pack
→ C3+ review
→ project or system memory
```

No automatic promotion.

---

## 2. Memory scopes

```text
session
candidates
project
system
```

Forbidden terminology:

```text
agency memory
memory/agency
```

Use `system memory` for reusable patterns, methods and rules.

---

## 3. Event model

Base pattern:

```text
Actor → Action/Event → Target → Context → Evidence → Candidate decision
```

Recommended fields:

```yaml
memory_event:
  id: memevt_001
  event_type: design_decision
  source_layer: openwebui | hermes | pantheon | imported_document
  source_ref: null
  actor: null
  target: null
  project_id: null
  text: ""
  category: general
  scope_candidate: project | system | session
  confidence: 0.0
  sensitivity: public | internal | project | sensitive | secret
  evidence_pack_id: null
  source_documents: []
  source_runs: []
  related_files: []
  tags: []
  created_at: null
  validation_status: candidate
  reviewer: null
  decision: keep_candidate | promote_to_project | promote_to_system | reject | needs_more_evidence
  valid_from: null
  valid_until: null
  superseded_by: null
```

---

## 4. Event types

Initial event types:

```text
client_request
company_quote
site_observation
contractual_warning
design_decision
approval_decision
document_received
document_sent
regulatory_constraint
payment_event
delay_event
nonconformity
scope_change
quote_revision
site_instruction
safety_notice
permit_event
commission_feedback
technical_reserve
contract_amendment
invoice_dispute
reception_reserve
insurance_risk
skill_improvement_candidate
workflow_improvement_candidate
source_policy_candidate
```

---

## 5. Categories

Recommended categories:

```text
general
technical
planning
budget
contractual
regulatory
safety
quality
privacy
operations
software
```

---

## 6. Candidate decisions

Allowed decisions:

```text
keep_candidate
promote_to_project
promote_to_system
reject
archive
needs_more_evidence
supersede_existing
```

A decision is invalid without an Evidence Pack when it has durable impact.

---

## 7. Supersession

Memory must support correction and obsolescence.

```yaml
valid_from: 2026-05-01
valid_until: null
superseded_by: null
```

When a memory item becomes obsolete:

```yaml
valid_until: 2026-06-15
superseded_by: mem_2026_0615_001
```

Old memory is not deleted by default. It is invalidated or superseded.

---

## 8. Promotion requirements

Promotion requires:

- identifiable source;
- clear scope;
- Evidence Pack;
- contradiction check;
- privacy review;
- usefulness review;
- stale-source check;
- C3+ approval.

System memory requires stronger review than project memory.

---

## 9. Forbidden behavior

```text
automatic memory promotion
automatic agency promotion
LLM consolidation without Evidence Pack
cross-project memory merge without approval
project fact promoted to system without separate review
Hermes local memory treated as Pantheon truth
OpenWebUI Knowledge treated as memory
```

---

## 10. Evidence Pack link

Every memory event promoted beyond candidate must reference an Evidence Pack.

Minimum fields:

```text
files_read
sources_used
documents_used
knowledge_bases_consulted
assumptions
unsupported_claims
limitations
approval_required
```

---

## 11. Final rule

```text
Memory is validated, scoped and reversible.
Raw extraction is only a candidate.
```
