# Skill — agent_revision_request

Status: candidate.

Domain: general.

Purpose: allow a Pantheon role to request a bounded revision from another role when an output is incomplete, risky, incoherent or off-brief.

---

## 1. Role

`agent_revision_request` formalizes inter-role revision without creating a free autonomous agent loop.

It produces a structured request for a new candidate output.

It does not mutate files, approve changes or execute tools.

---

## 2. Inputs

```text
requesting_role
target_role
target_output
reason
requested_change
risk_or_evidence_context optional
```

---

## 3. Output

```yaml
agent_revision_request:
  requested_by: APOLLO
  target_role: IRIS
  target_output: draft_response
  reason: "The draft does not stay close enough to the initial request."
  requested_change:
    - "Reduce digressions."
    - "Make limitations more visible."
  approval_impact: none
  memory_impact: none
```

---

## 4. Rules

```text
request must be specific
request must be bounded
request must name the target output
request must not become an endless loop
request must not bypass THEMIS or APOLLO
```

---

## 5. Guardrails

This skill only requests a revised candidate output.

It must not silently rewrite a final answer, approve a revision, start an unbounded loop, or modify canonical content.

---

## 6. Final rule

```text
Ask for the smallest useful revision, not a new uncontrolled answer.
```
