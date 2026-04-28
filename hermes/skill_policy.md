# Hermes Skill Policy — Pantheon OS

> Reference policy for using, evolving and leveling Hermes-related skills inside Pantheon OS.

---

# 1. Principle

Hermes provides executable skills.

Pantheon provides governance, domain contracts and validation.

```text
Hermes skill = executable capability.
Pantheon skill = domain contract + governance layer.
```

Pantheon must not duplicate an existing Hermes capability when a controlled wrapper is enough.

---

# 2. Creation rule

Before creating a new Pantheon skill, the system must check:

```text
1. existing Pantheon skills;
2. existing Pantheon workflows;
3. Hermes built-in skills;
4. Hermes optional skills;
5. community skills as inspiration only;
6. near-duplicate names;
7. runtime and privacy risks.
```

A new skill can only be created as `candidate` first.

---

# 3. Decision classes

| Decision | Meaning |
|---|---|
| `use_existing` | Existing Pantheon skill or workflow is sufficient |
| `use_hermes_builtin` | Hermes built-in skill is sufficient under Pantheon policy |
| `wrap_hermes_skill` | Hermes executes; Pantheon defines contract, inputs, outputs and approvals |
| `create_candidate` | New Pantheon candidate skill is justified |
| `extend_existing` | Existing Pantheon skill should receive an update proposal |
| `reject_duplicate` | Request is already covered |
| `block_for_safety` | Request is too risky without sandbox, approval or policy |

---

# 4. Skill states

Pantheon skills use explicit lifecycle states.

```text
candidate
active
probation
quarantine
archived
rejected
```

| State | Meaning |
|---|---|
| `candidate` | Proposed but not validated |
| `active` | Validated and usable |
| `probation` | Usable but under observation after weakness or change |
| `quarantine` | Temporarily removed from normal use pending review |
| `archived` | Preserved but not recommended |
| `rejected` | Not retained; should not be used |

Rules:

- every new skill starts as `candidate`;
- every major rewrite returns the skill to `probation`;
- `quarantine`, `archive` and `delete` require human approval;
- reversible states are preferred over deletion.

---

# 5. Optional skills

Hermes optional skills are not enabled by default.

Pantheon rule:

```text
No Hermes optional skill may be installed, enabled or used in a real workflow without review.
```

Review must check:

- real utility;
- dependencies;
- API keys;
- filesystem access;
- network access;
- external actions;
- privacy exposure;
- sandbox requirement;
- rollback path.

---

# 6. Community skills

Community skills are inspiration sources, not trusted capabilities.

They must be classified as:

```text
integrate_now
integrate_later
interesting_not_priority
redundant
risky
reject
```

No community skill is installed directly into a Pantheon production environment.

---

# 7. External repository classification

Any repository used as inspiration must be evaluated only for what improves Pantheon.

For each retained idea, document:

- problem solved;
- Markdown file to modify;
- target section;
- architecture impact;
- code impact;
- risks;
- priority.

No external architecture is copied mechanically.

---

# 8. Skill factory policy

Automatic skill creation is not allowed.

A skill-factory mechanism may only produce a proposal.

Required flow:

```text
observed pattern
→ candidate proposal
→ name check
→ duplicate check
→ Hermes skill check
→ privacy check
→ review
→ human validation
→ file creation
```

Generated skills must not be written directly into active skill folders.

---

# 9. Meta-reasoning policy

Meta-reasoning skills such as analytical prisms, self-reflection and blind-spot reports are allowed as inspiration.

They must remain controlled:

- no hidden automatic self-improvement;
- no silent rewrite of active skills;
- explicit constraint report when analysis is partial;
- clear statement of what was not checked;
- no project memory promotion without review.

---

# 10. Manifest mapping

A Pantheon skill that uses Hermes must define a mapping:

```yaml
hermes_mapping:
  type: wrap_hermes_skill
  hermes_skill: official/category/name
  activation_required: true
  sandbox_required: true
  approval_required: true
```

If no Hermes skill is found:

```yaml
hermes_mapping:
  type: none_found
  checked: true
```

---

# 11. Risky skills

The following are risky by default:

- terminal;
- browser automation;
- web actions;
- MCP;
- file mutation;
- scheduler;
- gateways;
- credentials;
- external APIs;
- autonomous coding agents;
- automatic skill generation;
- automatic memory promotion.

Rule:

```text
sandbox + visible execution + approval required
```

---

# 12. Privacy

No real data from private conversations, real projects, clients, companies, addresses, construction sites or identifiable people may be injected into a Hermes skill without explicit validation.

Examples and tests must be fictional.

---

# 13. Updates

A positive result does not modify an active skill directly.

Required flow:

```text
useful result
→ UPDATES.md
→ review
→ optimization
→ validation
→ SKILL.md
```

XP may be granted only for real improvement, detected blockage, fixed blockage, simplification or new guardrail.

XP never triggers automatic level-up.

---

# 14. XP model

Pantheon uses XP to measure skill maturity, not usage volume.

XP is qualitative evidence.

It must reward:

- reliability;
- clarity;
- reuse;
- safety;
- fewer mistakes;
- better outputs;
- better verification.

It must not reward:

- number of executions alone;
- long answers;
- repeated cosmetic edits;
- unverified success;
- user flattery;
- automatic self-assessment.

---

## 14.1 XP events

| Event | XP | Requirement |
|---|---:|---|
| User confirms answer was useful | 1 | Non-intrusive feedback or explicit confirmation |
| Minor clarity improvement | 2 | Reviewable change in `UPDATES.md` |
| Repeated confusion fixed | 3 | Same issue observed at least twice |
| Verification checklist added | 5 | Reduces risk of wrong output |
| Blockage detected and fixed | 8 | Clear before/after improvement |
| Reusable workflow extracted | 13 | Pattern confirmed across several uses |
| Safety/privacy guardrail added | 13 | Prevents meaningful risk |
| Major validated upgrade | 21 | Review + tests/examples + human validation |

XP is first recorded as `pending_xp`.

Validated XP is granted only after review.

---

## 14.2 Anti-farming rules

A skill must not gain XP from volume alone.

Rules:

- one XP event per improvement type per version;
- no XP for duplicate feedback;
- no XP for unreviewed self-claims;
- no XP for raw usage count;
- no XP when privacy or safety checks are missing;
- XP can be denied during review;
- XP can be reversed if an upgrade creates regression.

---

# 15. Level model

Pantheon uses a slow stepped progression curve.

The goal is to make early progress visible while making high levels difficult to reach.

| Level | Name | Validated XP | Meaning |
|---:|---|---:|---|
| 0 | Candidate | 0 | Proposed, not reliable yet |
| 1 | Usable | 10 | Can be used with caution |
| 2 | Stable | 25 | Reused successfully and documented |
| 3 | Reliable | 50 | Handles normal edge cases and has checks |
| 4 | Expert | 90 | Strong outputs, failure modes documented |
| 5 | Core | 150 | System-critical, mature, protected from casual rewrites |

Level thresholds are intentionally non-linear.

Late levels require more evidence, not more activity.

---

## 15.1 Level-up requirements

XP alone is not enough.

A level-up requires:

- enough validated XP;
- no unresolved critical issue;
- examples updated;
- tests or checklists updated;
- privacy check passed;
- rollback path available;
- human approval.

Additional requirements:

| Target level | Extra requirement |
|---:|---|
| 1 | At least one validated use case |
| 2 | At least three successful uses or one strong repeatable workflow |
| 3 | Edge cases documented |
| 4 | Failure modes and guardrails documented |
| 5 | Protected core status approved explicitly |

---

## 15.2 Level-down and quarantine

A skill can lose status.

Triggers:

- repeated wrong outputs;
- unsafe behavior;
- privacy leak risk;
- obsolete assumptions;
- duplicate of a better skill;
- unclear scope;
- broken examples or tests.

Allowed decisions:

```text
keep_active
move_to_probation
move_to_quarantine
archive
reject
```

Deletion remains exceptional.

---

# 16. Feedback policy

Pantheon should ask for user feedback only when it is useful.

Do not ask after every message.

Ask only after:

- a substantial answer;
- a reusable method;
- a corrected blockage;
- a workflow or skill proposal;
- an output that could improve a skill.

Preferred non-intrusive wording:

```text
This looks reusable. Should I mark it as a candidate improvement for the relevant skill?
```

French equivalent:

```text
Ce résultat semble réutilisable. Je le note comme amélioration candidate de la skill concernée ?
```

Feedback options should stay simple:

```text
yes
no
revise
```

or:

```text
oui
non
à revoir
```

Rules:

- feedback creates a candidate update, not an automatic upgrade;
- positive feedback can create `pending_xp` only;
- negative feedback should trigger review, not penalty by default;
- no pressure, no repeated request, no gamified noise.

---

# 17. Manifest fields

Skill manifests may include XP and level metadata.

```yaml
lifecycle:
  state: active
  level: 2
  xp:
    validated: 31
    pending: 5
  last_review: 2026-04-28
  review_required: false
  probation_reason: null
```

Every XP change must be traceable.

---

# 18. Final rule

Pantheon governs Hermes.

It does not replace it, duplicate it or delegate governance to it.

A skill becomes stronger through validated usefulness, not through automatic activity.
