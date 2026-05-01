# SKILL LIFECYCLE — Pantheon Next

> Governance reference for Pantheon skills and Hermes skill wrappers.

---

## 1. Principle

```text
Hermes skill = executable capability.
Pantheon skill = domain contract + governance layer.
```

Pantheon must not duplicate Hermes. It defines purpose, domain, inputs, outputs, limits, risk, approval level, evidence requirements, memory impact and optional Hermes mapping.

---

## 2. Skill states

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
| `candidate` | Proposed, not validated |
| `active` | Validated and usable |
| `probation` | Usable but under observation |
| `quarantine` | Temporarily blocked pending review |
| `archived` | Preserved for history, not recommended |
| `rejected` | Explicitly not retained |

Rules:

- every new skill starts as `candidate`;
- every major rewrite returns to `probation`;
- quarantine, archive and rejection require review;
- reversible states are preferred over deletion;
- no active skill is rewritten silently.

---

## 3. Creation flow

Before creating a skill, check:

```text
existing Pantheon skills
existing Pantheon workflows
Hermes built-in skills
Hermes optional skills
external/community skills as inspiration only
near-duplicate names
privacy, runtime and side-effect risks
```

Allowed decisions:

```text
use_existing
use_hermes_builtin
wrap_hermes_skill
create_candidate
extend_existing
reject_duplicate
block_for_safety
```

---

## 4. Minimal skill package

```text
domains/{domain}/skills/{skill_id}/
  SKILL.md
  manifest.yaml
  examples.md
  tests.md
  UPDATES.md
```

`SKILL.md` is the current reviewed definition.

`UPDATES.md` stores candidate improvements.

`manifest.yaml` stores lifecycle, level, XP, risk and Hermes mapping.

---

## 5. Manifest lifecycle block

```yaml
lifecycle:
  state: candidate
  level: 0
  xp:
    validated: 0
    pending: 0
  last_review: null
  review_required: true
  probation_reason: null
```

---

## 6. Hermes mapping

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

## 7. XP model

XP measures validated maturity, not usage volume.

XP rewards reliability, clarity, reuse, safety, fewer mistakes, better checks and better outputs.

XP must not reward raw usage count, long answers, cosmetic edits, unverified success or automatic self-assessment.

XP starts as `pending` and becomes validated only after review.

---

## 8. Levels

| Level | Name | Validated XP | Meaning |
|---:|---|---:|---|
| 0 | Candidate | 0 | Proposed, not reliable yet |
| 1 | Usable | 10 | Can be used with caution |
| 2 | Stable | 25 | Reused and documented |
| 3 | Reliable | 50 | Handles normal edge cases and has checks |
| 4 | Expert | 90 | Strong outputs, failure modes documented |
| 5 | Core | 150 | System-critical, protected from casual rewrites |

XP alone is not enough for level-up.

Level-up requires updated examples, updated tests or checklists, privacy check, rollback path and human approval.

---

## 9. Candidate skill factory rule

A skill factory may only propose.

Approved flow:

```text
observed pattern
→ candidate proposal
→ name check
→ duplicate check
→ Hermes skill check
→ privacy check
→ review
→ human validation
→ candidate files
```

Forbidden:

```text
automatic active skill creation
automatic active skill patching
automatic level-up
automatic memory promotion
```

---

## 10. Quarantine and level-down

Triggers:

- repeated wrong outputs;
- unsafe behavior;
- privacy risk;
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

Deletion is exceptional.

---

## 11. Final rule

```text
A skill becomes stronger through validated usefulness, not automatic activity.
```
