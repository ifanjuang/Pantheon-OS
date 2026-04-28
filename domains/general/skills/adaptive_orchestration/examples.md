# Adaptive Orchestration — Examples

> Fictional examples only. No real project, client, company, address or private conversation data.

---

# 1. Use workflow as-is

## Input

```text
Create a concise meeting summary from these notes.
```

## Preflight decision

```yaml
decision: use_as_is
workflow: meeting_summary
reason: "Intent is clear, risk is low, no additional context required."
approval_required: false
```

---

# 2. Adapt existing workflow before execution

## Input

```text
Compare this quote against the technical specification.
```

## Preflight decision

```yaml
decision: adapt_existing
workflow: quote_vs_spec_review
reason: "The request involves technical scope and possible cost discrepancies."
adaptations:
  add_agents:
    - THEMIS
    - PROMETHEUS
  conditional_agents:
    - DEMETER
approval_required: false
```

## Visible report

```markdown
## Pantheon Trace — Workflow Preflight

Initial workflow: `quote_vs_spec_review`
Decision: `adapt_existing`
Reason: technical and responsibility checks may be needed.
Added agents: THEMIS, PROMETHEUS.
Conditional agent: DEMETER if quantities or prices are exploitable.
```

---

# 3. Insert subworkflow during execution

## Runtime signal

```yaml
agent: ARGOS
signal: missing_data
severity: medium
summary: "The reference specification appears incomplete."
recommended_action: insert_subworkflow
recommended_target: specification_completeness_check
requires_user_validation: false
```

## ZEUS decision

```yaml
decision: insert_subworkflow
from_workflow: quote_vs_spec_review
inserted_subworkflow: specification_completeness_check
reason: "The main review needs a reliable reference document before comparison."
approved_by:
  - ZEUS
  - THEMIS
approval_required: false
```

---

# 4. Switch workflow

## Input

```text
Check whether this response creates a responsibility issue.
```

## Preflight decision

```yaml
decision: switch_workflow
from_workflow: general_text_review
to_workflow: liability_risk_review
reason: "The real intent is responsibility and risk, not text improvement."
user_informed: true
approval_required: false
```

---

# 5. Remove unnecessary agent

## Runtime signal

```yaml
agent: ZEUS
signal: unnecessary_step
severity: low
summary: "No cost, quantity or resource issue is present."
recommended_action: remove_agent
recommended_target: DEMETER
requires_user_validation: false
```

## Decision

```yaml
decision: remove_agent
agent_removed: DEMETER
reason: "Economic review is unnecessary for this request."
impact: "Shorter workflow, no loss of required validation."
```

---

# 6. Ask user after unresolved uncertainty

## Situation

Agents disagree after context expansion.

## Report

```markdown
## Pantheon Trace — User Validation Required

The current workflow can proceed in two valid directions:

1. `technical_gap_review` — focus on technical inconsistencies.
2. `liability_risk_review` — focus on responsibility and contractual exposure.

ZEUS cannot choose without changing the intended output.

Please choose: `1`, `2`, or `both`.
```

---

# 7. Candidate update after completion

## Signal

```yaml
signal: candidate_pattern
severity: low
summary: "The same preflight adaptation was useful across several similar reviews."
recommended_action: propose_skill_update
recommended_target: adaptive_orchestration
```

## Non-intrusive feedback

```text
This looks reusable. Should I mark it as a candidate improvement for adaptive_orchestration?
```
