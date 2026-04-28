# Adaptive Orchestration

> Candidate Pantheon skill. Defines how ZEUS selects, adapts, simplifies, switches or extends workflows before and during execution.

---

# 1. Purpose

`adaptive_orchestration` prevents Pantheon from executing workflows mechanically.

Before a workflow starts, it checks whether the selected workflow fits the user request and the available context.

During execution, it checks whether the workflow still fits the evolving agent outputs.

After execution, it may propose candidate improvements when a reusable pattern appears.

---

# 2. Core rule

```text
Before execution: select or adapt.
During execution: reevaluate and adjust.
After execution: propose candidate improvement when useful.
```

---

# 3. Responsibilities

This skill may decide to:

- use an existing workflow as-is;
- adapt an existing workflow;
- add an agent;
- remove an agent;
- add a step;
- skip a step;
- insert a subworkflow;
- switch to another workflow;
- expand context;
- ask specific agents for arbitration;
- ask the user only if uncertainty remains;
- propose a candidate workflow;
- propose a candidate skill or workflow update.

---

# 4. Non-responsibilities

This skill must not:

- create an active workflow automatically;
- permanently modify a workflow without validation;
- promote memory automatically;
- upgrade a skill level automatically;
- expose raw chain-of-thought;
- perform risky external actions without approval;
- silently change the user’s intended output.

---

# 5. Preflight phase

Before using a workflow, ZEUS must run a preflight check.

The preflight checks:

```text
intent_match
context_match
risk_level
missing_information
available_workflows
required_agents
unnecessary_agents
memory_need
user_validation_need
```

Possible decisions:

```text
use_as_is
adapt_existing
insert_subworkflow
switch_workflow
ask_agents
expand_context
ask_user
propose_candidate_workflow
```

---

# 6. Runtime adaptation phase

After each significant agent output, ZEUS checks whether the current workflow is still appropriate.

Runtime checks:

```text
workflow_still_relevant
new_signal_detected
agent_needed
agent_no_longer_needed
step_needed
step_no_longer_needed
subworkflow_needed
memory_needed
user_input_needed
risk_changed
confidence_changed
```

Allowed runtime actions:

```text
continue
add_agent
remove_agent
add_step
skip_step
insert_subworkflow
switch_workflow
pause_for_user
propose_candidate_update
```

---

# 7. Confidence-driven adaptation

ZEUS may adapt directly only when:

```text
confidence = high
risk = low
change = reversible
privacy = safe
no external action
no contractual commitment
```

If confidence is medium, ZEUS asks the relevant agents.

If confidence is low or agents disagree, ZEUS expands context.

Context expansion order:

```text
session memory
project memory
system memory
knowledge
external sources when policy allows
```

If uncertainty remains, ZEUS asks the user.

---

# 8. Agent roles

| Agent | Role in adaptive orchestration |
|---|---|
| ZEUS | Orchestrates and decides trajectory changes |
| ATHENA | Checks method and strategy |
| THEMIS | Controls risk, approval, responsibility and veto |
| APOLLO | Validates final coherence |
| PROMETHEUS | Detects contradictions and blind spots |
| HECATE | Flags uncertainty and missing information |
| HERMES | Executes allowed functions and runtime operations |
| Relevant domain agents | Provide specialized signals when needed |

---

# 9. Signals

Agents must not emit raw reasoning.

They emit structured signals:

```yaml
agent: THEMIS
signal: liability_risk
severity: high
summary: "The requested output may be interpreted as contractual validation."
recommended_action: add_step
recommended_target: liability_warning
requires_user_validation: true
```

Signal types:

```text
missing_data
contradiction
scope_conflict
liability_risk
technical_gap
cost_gap
privacy_risk
workflow_mismatch
unnecessary_step
confidence_drop
candidate_pattern
```

---

# 10. Adaptation report

Every workflow adaptation must be visible in OpenWebUI through a concise report.

Required fields:

```text
initial_workflow
decision
reason
signal
agents_added
agents_removed
steps_added
steps_skipped
subworkflow_inserted
workflow_switched_to
context_expanded
approval_required
next_action
```

No raw chain-of-thought is displayed.

---

# 11. User validation

User validation is required when the adaptation is:

- irreversible;
- risky;
- externally visible;
- legally or contractually sensitive;
- a memory promotion;
- a permanent workflow change;
- a skill level-up;
- a new active workflow creation;
- unresolved after agent consultation and context expansion.

Preferred prompt:

```text
The workflow needs a trajectory change. Do you want me to proceed with the proposed adaptation?
```

---

# 12. Candidate updates

After a workflow completes, this skill may propose:

- a candidate workflow update;
- a candidate skill update;
- a new candidate workflow;
- pending XP for a skill;
- a memory candidate.

It must not apply these changes directly.

---

# 13. Output discipline

Adaptive orchestration should reduce unnecessary complexity.

It may add structure when required, but it must also remove or skip unnecessary steps.

Rule:

```text
Add when needed.
Remove when unnecessary.
Switch when misaligned.
Insert when a prerequisite is missing.
Create only when nothing fits.
Validate when durable or risky.
```

---

# 14. Status

Current status: `candidate`.

This skill is not active until reviewed against `hermes/skill_policy.md`, `MODULES.md` and the first real domain workflows.
