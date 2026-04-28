# Adaptive Orchestration — Tests

> Documentation-level tests. These tests define expected behavior before implementation.

---

# 1. Preflight must run before workflow execution

## Given

A user request matches an existing workflow.

## Expected

The system must still produce a preflight decision before execution.

```yaml
required_output:
  decision: use_as_is | adapt_existing | insert_subworkflow | switch_workflow | ask_agents | expand_context | ask_user | propose_candidate_workflow
```

---

# 2. High-confidence low-risk adaptation can be direct

## Given

The selected workflow is correct but one optional technical agent is unnecessary.

## Expected

ZEUS may skip or remove that agent without user approval if the change is reversible and low-risk.

```yaml
expected:
  decision: remove_agent
  approval_required: false
  reason_required: true
  visible_report_required: true
```

---

# 3. Medium confidence requires agent consultation

## Given

The workflow may need a responsibility review but confidence is medium.

## Expected

ZEUS must ask relevant agents before adapting.

```yaml
expected:
  action: ask_agents
  agents:
    - THEMIS
    - ATHENA
```

---

# 4. Low confidence requires context expansion

## Given

Agents disagree about the right workflow.

## Expected

ZEUS expands context in the defined order.

```yaml
expected_order:
  - session_memory
  - project_memory
  - system_memory
  - knowledge
```

---

# 5. Remaining uncertainty requires user input

## Given

The workflow remains ambiguous after agent consultation and context expansion.

## Expected

ZEUS asks the user instead of silently choosing.

```yaml
expected:
  action: ask_user
  options_required: true
  recommendation_allowed: true
```

---

# 6. Risky or durable changes require approval

## Given

A proposed adaptation creates a permanent workflow update or memory promotion.

## Expected

User or human validation is required.

```yaml
expected:
  approval_required: true
  auto_apply: false
```

---

# 7. No raw chain-of-thought exposure

## Given

An agent emits a signal.

## Expected

Only structured signals, summaries, evidence and visible outputs are displayed.

```yaml
forbidden:
  - raw_chain_of_thought
  - hidden_reasoning
  - private_notes
```

---

# 8. Candidate update after useful pattern

## Given

The same adaptation proves useful repeatedly.

## Expected

The system may propose a candidate update, not apply it directly.

```yaml
expected:
  action: propose_candidate_update
  user_feedback_required: true
  auto_update_skill: false
  xp_status: pending
```
