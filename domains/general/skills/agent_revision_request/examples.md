# Examples — agent_revision_request

All examples are fictional and generic.

---

## APOLLO asks IRIS to revise wording

```yaml
agent_revision_request:
  requested_by: APOLLO
  target_role: IRIS
  target_output: draft_response
  reason: "The response is clear but does not keep the limitation visible."
  requested_change:
    - "Add a visible limitation paragraph."
    - "Avoid definitive validation wording."
  approval_impact: none
  memory_impact: none
```

---

## THEMIS asks IRIS to make wording safer

```yaml
agent_revision_request:
  requested_by: THEMIS
  target_role: IRIS
  target_output: client_message
  reason: "The text sounds like a formal technical approval."
  requested_change:
    - "Replace approval wording with a cautious observation."
  approval_impact: C4
  memory_impact: none
```
