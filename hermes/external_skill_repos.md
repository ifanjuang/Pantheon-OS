# External Hermes Skill Repositories — Pantheon OS

> Classification of Hermes-related repositories used as inspiration for Pantheon skill governance.

---

# 1. Rule

External Hermes repositories are not runtime dependencies unless explicitly approved.

They can inform Pantheon only if they improve:

- skill governance;
- skill creation flow;
- skill review;
- safety policy;
- observability;
- UI/operator experience;
- memory hygiene;
- user-controlled learning.

No external skill pack is installed directly in Pantheon production.

No external repository may bypass Pantheon governance.

---

# 2. Global decision model

| Decision | Meaning |
|---|---|
| `integrate_now` | Adopt as documentation or governance pattern now |
| `integrate_later` | Keep as future implementation pattern |
| `interesting_not_priority` | Useful idea, not needed for current core |
| `redundant` | Already covered by Pantheon or Hermes |
| `risky` | Requires strong sandbox, approval or audit before use |
| `reject` | Do not import or use |
| `to_verify` | Insufficient audit; keep in watchlist only |

---

# 3. Source classification

| Source | Classification | Retained idea | Pantheon decision | Priority |
|---|---|---|---|---|
| `0xNyk/awesome-hermes-agent` | `integrate_now` | Ecosystem radar and maturity watchlist | Use as watchlist method, not dependency | P1 |
| `Cranot/super-hermes` | `integrate_later` | Constraint reports, blind spots, analysis transparency | Extract pattern into review workflows | P2 |
| `Romanescu11/hermes-skill-factory` | `integrate_later` | Candidate skill proposal from repeated workflows | Proposal only; no active auto-generation | P1 docs / P2 implementation |
| `AMAP-ML/SkillClaw` | `risky` | Request interception, session pattern mining, skill evolution | Inspiration only; no proxy/interception in Pantheon core | P3 |
| `longyunfeigu/learn-hermes-agent` | `integrate_now` | Pedagogical system map of agent loop, tools, memory, skills, safety | Use as reference for Pantheon docs and developer onboarding | P1 |
| `pyrate-llama/hermes-ui` | `interesting_not_priority` | Operator UI: logs, memory inspection, skills browser, cron, MCP, file browser | Useful UI inspiration; do not replace OpenWebUI now | P3 |
| `ChuckSRQ/awesome-hermes-skills` | `integrate_later` | Artifact preview, deep research lenses, behavioral benchmarks, GitHub workflow skills | Extract benchmarks/review patterns only | P2 |
| `Yonkoo11/hermes-dojo` | `risky` | Skill performance monitoring and weakness reports | Keep measurement/reporting; reject overnight auto-fix | P2/P3 |
| `swarmclawai/swarmclaw` | `interesting_not_priority` | Control plane, visual agents, task board, approvals, eval lab, skill drafting | Strong inspiration for future operator console; not current runtime | P3 |
| `zzyong24/skills-judgment` | `integrate_later` | Skill health scoring, probation, exile, graveyard, reversible quarantine | Adopt as future skill lifecycle pattern with human approval | P2 |
| `nexus9888/hermes-memory-skills` | `integrate_later` | Memory dreaming, candidate extraction, lean memory check | Adapt to Pantheon memory, but no automatic promotion | P1/P2 |
| `Lethe044/hermes-incident-commander` | `risky` | Incident workflow: detect, triage, diagnose, remediate, verify, learn | Use workflow anatomy only; reject autonomous infra remediation for Pantheon | P3 |
| `thedavidweng/skills` | `integrate_later` | Wiki hygiene, document generation, code entropy reduction, source integrity | Extract wiki/source hygiene and document-as-source patterns | P2 |

---

# 4. Retained patterns

## 4.1 Ecosystem radar

Source:

```text
0xNyk/awesome-hermes-agent
```

Retained idea:

- track Hermes ecosystem;
- classify maturity;
- avoid random community skill installation;
- identify useful patterns before implementation.

Pantheon impact:

| File | Section |
|---|---|
| `EXTERNAL_WATCHLIST.md` | Hermes ecosystem watch |
| `hermes/skill_policy.md` | Community skills and external repository classification |
| `ROADMAP.md` | Optional future ecosystem review cycle |

Code impact: none now.

Risk: catalogue bloat.

---

## 4.2 Constraint reports

Sources:

```text
Cranot/super-hermes
ChuckSRQ/awesome-hermes-skills
```

Retained idea:

A deep review should not only state findings. It should also state what was not checked.

Required output pattern:

```text
analysis_focus
maximized_dimension
sacrificed_dimension
blind_spots
confidence_limits
recommended_follow_up
```

Pantheon adaptation:

```text
domains/general/skills/analysis_constraint_report/
domains/general/workflows/deep_review.yaml
```

Code impact: later only.

Risk: verbose outputs and false sense of depth.

---

## 4.3 Candidate skill proposal

Sources:

```text
Romanescu11/hermes-skill-factory
AMAP-ML/SkillClaw
Yonkoo11/hermes-dojo
swarmclawai/swarmclaw
```

Retained idea:

Repeated workflows can produce candidate skill proposals.

Rejected behavior:

- automatic active skill creation;
- automatic plugin creation;
- automatic skill patching;
- request interception without explicit consent;
- background rewrite of active skills.

Pantheon-approved flow:

```text
observed pattern
→ candidate proposal
→ name check
→ duplicate check
→ Hermes skill check
→ privacy check
→ review
→ human validation
→ create candidate files
→ promote only after validation
```

Pantheon impact:

| File | Section |
|---|---|
| `MEMORY.md` | Candidate memory |
| `MODULES.md` | Skill lifecycle |
| `hermes/skill_policy.md` | Skill factory policy |
| `ROADMAP.md` | Capability creation workflow |

Future code/files:

```text
domains/general/skills/skill_design/
domains/general/skills/workflow_design/
domains/general/skills/name_check/
domains/general/skills/hermes_skill_check/
domains/general/workflows/capability_creation.yaml
```

Risk: skill spam, duplicates, privacy leaks.

---

## 4.4 Skill health and quarantine

Sources:

```text
zzyong24/skills-judgment
Yonkoo11/hermes-dojo
```

Retained idea:

Skills need lifecycle discipline: usage, freshness, completeness, relationships, failures and reversibility.

Pantheon adaptation:

```text
active
candidate
probation
quarantine
archived
rejected
```

Allowed actions:

- mark as candidate;
- mark as probation;
- mark as quarantine;
- propose archive;
- propose deletion.

Rejected actions:

- automatic deletion;
- automatic exile without review;
- automatic promotion;
- automatic patching of active skills.

Pantheon should prefer reversible states.

Future files:

```text
domains/general/skills/skill_health_check/
domains/general/workflows/skill_review.yaml
```

Risk: over-managing small skill libraries before there are enough skills.

Priority: P2 after first domain skills exist.

---

## 4.5 Memory hygiene

Sources:

```text
nexus9888/hermes-memory-skills
thedavidweng/skills
```

Retained idea:

Memory should be lean, verified and linked to durable sources instead of becoming a raw transcript archive.

Pantheon adaptation:

- candidate extraction is allowed;
- memory trimming is allowed;
- source integrity checks are allowed;
- broken reference detection is allowed;
- automatic memory promotion is rejected.

Approved cycle:

```text
session material
→ candidates
→ privacy check
→ review
→ project or system memory
```

Pantheon impact:

| File | Section |
|---|---|
| `MEMORY.md` | Candidate memory, promotion, privacy |
| `hermes/skill_policy.md` | Automatic memory promotion risk |
| `ROADMAP.md` | Memory hygiene workflow |

Future files:

```text
domains/general/skills/memory_candidate_review/
domains/general/skills/memory_lean_check/
domains/general/workflows/memory_review.yaml
```

Risk: leaking real project/private data into system memory.

Priority: P1 documentation, P2 implementation.

---

## 4.6 Operator UI and observability

Sources:

```text
pyrate-llama/hermes-ui
swarmclawai/swarmclaw
```

Retained idea:

An operator should see:

- skills;
- memory;
- logs;
- cron jobs;
- MCP tools;
- running jobs;
- failed runs;
- pending approvals;
- evals;
- context pressure.

Pantheon decision:

Do not build UI now.

Keep this as future inspiration for a Pantheon operator console.

Potential future:

```text
operations/operator_console.md
```

Risk: UI work before the domain model is stable.

Priority: P3.

---

## 4.7 Workflow anatomy and training references

Sources:

```text
longyunfeigu/learn-hermes-agent
Lethe044/hermes-incident-commander
ChuckSRQ/awesome-hermes-skills
```

Retained idea:

Good workflows expose their phases explicitly.

Useful phase patterns:

```text
detect → triage → diagnose → act → verify → report → learn
measure → identify weakness → propose fix → review → validate → report
research → multi-lens analysis → synthesis → open questions
```

Pantheon adaptation:

Use these as anatomy references for workflows, not as runtime imports.

Risk:

- importing highly autonomous remediation patterns too early;
- giving agents external action rights before approval gates exist.

Priority: P2 for workflow templates.

---

# 5. Explicit rejections

Pantheon rejects these behaviors unless a future policy explicitly authorizes them:

- installing external skill packs directly into production;
- giving external skills unrestricted file access;
- giving external skills unrestricted terminal access;
- proxying or intercepting requests without explicit user approval;
- automatic active skill generation;
- automatic active skill patching;
- automatic memory promotion;
- autonomous infrastructure remediation;
- automatic deletion of skills;
- direct wallet, payment or signing operations;
- public posting from agents without approval.

---

# 6. Required review before adoption

Before any retained idea becomes a Pantheon capability, the review must define:

| Field | Required |
|---|---|
| Problem solved | yes |
| Target Markdown file | yes |
| Target section | yes |
| Architecture impact | yes |
| Code impact | yes |
| Security risk | yes |
| Privacy risk | yes |
| Rollback path | yes |
| Human validation | yes |

---

# 7. Priority synthesis

## P1 — integrate in documentation now

- Hermes ecosystem radar.
- Candidate skill proposal policy.
- Memory hygiene doctrine.
- Reversible skill lifecycle states.

## P2 — implement after core domain skills exist

- `skill_health_check`.
- `memory_candidate_review`.
- `analysis_constraint_report`.
- `capability_creation.yaml`.
- behavioral benchmark templates.

## P3 — later / not current core

- operator console;
- SwarmClaw-style control plane;
- autonomous incident workflows;
- UI for cron/MCP/skills/memory;
- proxy-based skill evolution.

---

# 8. Final rule

```text
External repositories can teach Pantheon how to govern skills.
They cannot bypass Pantheon governance.
```

Pantheon may learn from the Hermes ecosystem, but every retained pattern must become a documented Pantheon rule before it becomes code.
