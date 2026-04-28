# External Hermes Skill Repositories — Pantheon OS

> Classification of Hermes-related repositories used as inspiration for Pantheon skill governance.

---

# 1. Rule

External Hermes repositories are not runtime dependencies unless explicitly approved.

They can inform Pantheon only if they improve:

- skill governance;
- skill creation flow;
- review discipline;
- safety policy;
- observability;
- user-controlled learning.

No external skill pack is installed directly in Pantheon production.

---

# 2. Source classification

| Source | Classification | Why | Pantheon decision |
|---|---|---|---|
| `0xNyk/awesome-hermes-agent` | `integrate_now` as watchlist method | Curated ecosystem map with maturity tags and categories | Use as radar for Hermes ecosystem, not as dependency |
| `Cranot/super-hermes` | `integrate_later` as analysis pattern | Provides prism-based analysis, blind-spot reporting and constraint reports | Extract the `constraint report` idea into Pantheon review workflows |
| `Romanescu11/hermes-skill-factory` | `integrate_later` as controlled pattern | Detects repeated workflows and proposes generated skills/plugins | Use only as inspiration for candidate skill proposals, never automatic activation |

---

# 3. `awesome-hermes-agent`

## Problem solved

Pantheon needs a way to track the Hermes ecosystem without installing random community skills.

## Retained idea

Use the repository as a radar:

- maturity categories;
- skill registries;
- plugins;
- deployment tools;
- GUI tools;
- memory tools;
- multi-agent experiments.

## Markdown impact

| File | Section |
|---|---|
| `EXTERNAL_WATCHLIST.md` | Hermes ecosystem watch |
| `hermes/skill_policy.md` | Community skills and external repository classification |
| `ROADMAP.md` | Optional future Hermes ecosystem review cycle |

## Architecture impact

Low.

No runtime change.

## Code impact

None.

## Risks

- catalogue bloat;
- temptation to install too many skills;
- unstable community repos;
- duplication with Hermes Skills Hub.

## Priority

P1 for watchlist method.

---

# 4. `super-hermes`

## Problem solved

Pantheon needs better analysis transparency: not only findings, but also what the analysis did not cover.

## Retained idea

Add a constraint report to deep reviews.

A constraint report should state:

```text
analysis focus
maximized dimension
sacrificed dimension
blind spots
recommended follow-up workflow
confidence limits
```

## Pantheon adaptation

Do not import prism skills directly.

Instead, create a general review capability later:

```text
domains/general/skills/analysis_constraint_report/
```

Potential workflow integration:

```text
domains/general/workflows/deep_review.yaml
```

## Markdown impact

| File | Section |
|---|---|
| `MODULES.md` | Skill review and workflow review outputs |
| `AGENTS.md` | APOLLO / PROMETHEUS / HECATE responsibilities |
| `hermes/skill_policy.md` | Meta-reasoning policy |

## Architecture impact

Medium.

Adds quality discipline to review workflows.

## Code impact

None now.

Later: tests for required `constraint_report` output field in review workflows.

## Risks

- verbose outputs;
- false sense of depth;
- model-dependent quality;
- possible over-analysis for simple tasks.

## Priority

P2.

Useful after the first real skills exist.

---

# 5. `hermes-skill-factory`

## Problem solved

Pantheon needs a way to convert repeated workflows into reusable skills without losing governance.

## Retained idea

Detect repeated workflows and propose skills.

## Rejected behavior

Automatic write into active skill folders is rejected.

Automatic plugin creation is rejected for Pantheon production.

## Pantheon adaptation

Allowed flow:

```text
repeated workflow detected
→ candidate proposal
→ name check
→ duplicate check
→ Hermes built-in / optional skill check
→ privacy check
→ review
→ human validation
→ create candidate files
```

Generated skill files must start as candidates.

## Markdown impact

| File | Section |
|---|---|
| `hermes/skill_policy.md` | Skill factory policy |
| `MEMORY.md` | Candidate memory and skill updates |
| `MODULES.md` | Skill lifecycle |
| `ROADMAP.md` | Candidate skill creation workflow |

## Architecture impact

Medium.

This strengthens the `domains/general` layer.

## Code impact

Later only:

```text
domains/general/skills/skill_design/
domains/general/skills/workflow_design/
domains/general/skills/name_check/
domains/general/skills/hermes_skill_check/
domains/general/workflows/capability_creation.yaml
```

## Risks

- skill spam;
- poor names;
- duplicated skills;
- privacy leaks from real sessions;
- uncontrolled plugin generation;
- silent self-modification.

## Priority

P1 for documented candidate flow.

P2 for implementation.

---

# 6. Final decision

| Idea | Decision |
|---|---|
| Ecosystem radar | Keep now |
| Maturity classification | Keep now |
| Constraint reports | Integrate later |
| Prism skills | Inspiration only |
| Automatic skill generation | Reject as direct behavior |
| Candidate skill proposals | Keep later |
| Automatic plugin generation | Reject for production |

---

# 7. Pantheon rule

```text
External repositories can teach Pantheon how to govern skills.
They cannot bypass Pantheon governance.
```
