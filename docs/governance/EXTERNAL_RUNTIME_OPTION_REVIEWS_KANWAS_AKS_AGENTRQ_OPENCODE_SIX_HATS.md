# External runtime option reviews — Kanwas, AKS, AgentRQ, opencode-loop, six-hats-skill

> Supplemental review pack for external runtime, Knowledge, HITL and reasoning-method options.
>
> This document does not authorize installation or integration. It classifies options under Pantheon Next governance.

---

## 1. Doctrine

Pantheon Next keeps the same operating split:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

External options may inspire Pantheon or assist Hermes, but they must not become:

```text
Pantheon runtime
Pantheon memory authority
Pantheon scheduler
Pantheon approval authority
Pantheon source of truth
```

The current next internal target remains:

```text
domains/general/skills/knowledge_selection/
```

---

## 2. Summary matrix

| Option | Type | Classification | Pantheon-compatible use | Forbidden use | Priority |
|---|---|---|---|---|---|
| Kanwas | Collaborative AI workspace / visual board | `watch` / `inspiration_only` | Evidence Board / Decision Board UX, Git-backed Markdown workspace patterns | Replace `docs/governance/`, become source of truth, sync private project data without policy | P2 |
| AKS Reference Server | Agent Knowledge Standard / knowledge graph server | `watch` / `test_read_only` | Provenance schema, confidence metadata, source traversal, Knowledge Registry inspiration | Replace Pantheon Memory, auto-promote graph facts, ingest private data before policy | P1/P2 |
| AgentRQ | Human-in-the-loop task collaboration | `test_lab_only` / `watch` | Approval thread UX, task status lifecycle, agent-human handoff patterns | Become Pantheon scheduler, replace OpenWebUI approval surface, persist decisions as canonical memory | P2 |
| opencode-loop | Coding-agent loop around OpenCode | `to_verify` / `blocked_until_reviewed` | Possible Hermes-side software audit or patch-candidate experiment after review | Autonomous patch loop, direct push, write access to main, C3+ change without approval | P2 |
| six-hats-skill | Structured reasoning method | `inspiration_only` / `candidate_method` | Reasoning lenses for `knowledge_selection`, Evidence Pack review, architecture_fr risk review | Replace Pantheon agent roles, become autonomous agent, decide without evidence | P1 |

---

## 3. Kanwas decision

References:

```text
https://github.com/kanwas-ai/kanwas
https://kanwas.ai/
```

Classification:

```text
watch
inspiration_only
rejected_for_core
```

Kanwas is interesting as a collaborative context board and visual workspace pattern. Its useful contribution for Pantheon is not runtime execution. It is the idea that decisions, evidence, context and Markdown-backed artifacts can be visible in one shared workspace.

Potential Pantheon use:

```text
future Evidence Board UX
future Decision Board UX
collaborative context map inspiration
visual README/governance diagrams inspiration
Git-backed Markdown workspace pattern study
```

Pantheon-compatible reclassification:

| Kanwas concept | Pantheon-compatible form |
|---|---|
| shared board | future OpenWebUI/operations view inspiration |
| agent + human workspace | approval and Evidence Pack display inspiration |
| Git-backed Markdown | useful pattern, but repo remains canonical |
| visual context | README diagrams and Run Graph UX inspiration |

Forbidden:

```text
replace docs/governance/
become Pantheon source of truth
become OpenWebUI replacement
sync private project data without policy
store canonical memory outside Pantheon repo
allow external agent actions without Task Contract
```

Risk:

```text
parallel source of truth
workspace drift
private project data exposure
visual board becoming informal authority
agent actions bypassing approvals
```

Decision:

```text
Keep Kanwas as UX/workspace inspiration only.
Do not integrate as runtime or source-of-truth layer.
```

---

## 4. AKS Reference Server decision

References:

```text
https://github.com/Agent-Knowledge-Standard/AKS-Reference-Server
```

Classification:

```text
watch
test_read_only
rejected_for_core
```

AKS is conceptually strong for Pantheon because it focuses on structured agent knowledge, provenance, confidence, corroboration and traversable knowledge graphs.

Potential Pantheon use:

```text
Knowledge Registry schema inspiration
Memory Event Schema enrichment
source provenance patterns
confidence and corroboration metadata
knowledge graph traversal evidence
scope-aware source routing
portable knowledge export ideas
```

Pantheon-compatible reclassification:

| AKS concept | Pantheon-compatible form |
|---|---|
| knowledge entity | memory/event candidate entity |
| confidence score | Evidence Pack / memory candidate confidence |
| source traversal | Evidence trace / source path |
| last corroborated | freshness and validation metadata |
| scope | project/system/domain scope |
| knowledge graph server | optional read-only benchmark, not authority |

Allowed first step:

```text
read documentation
study schema only
compare with MEMORY_EVENT_SCHEMA.md
compare with KNOWLEDGE_TAXONOMY.md
compare with knowledge/registry.example.yaml
create a non-sensitive sample mapping if needed
```

Forbidden:

```text
replace Pantheon Memory
replace Knowledge Registry
auto-promote graph facts
run private project data through AKS before policy
create a second canonical memory server
treat graph traversal as proof without Evidence Pack
```

Risk:

```text
parallel memory authority
schema drift
false certainty from confidence scores
graph facts becoming canonical too early
private data ingestion risk
```

Decision:

```text
Use AKS as strong inspiration for provenance and confidence metadata.
Do not integrate it as a Pantheon memory backend now.
```

---

## 5. AgentRQ decision

References:

```text
https://github.com/agentrq/agentrq
https://agentrq.com/
```

Classification:

```text
test_lab_only
watch
rejected_for_core
```

AgentRQ is relevant because it focuses on human-in-the-loop collaboration between agents and users: tasks, status, replies, attachments and approvals.

Potential Pantheon use:

```text
OpenWebUI Actions inspiration
approval thread UX
agent-human handoff pattern
Task Contract status lifecycle inspiration
Run Graph interaction model
remote feedback pattern study
```

Pantheon-compatible reclassification:

| AgentRQ concept | Pantheon-compatible form |
|---|---|
| task board | Task Contract status display |
| agent request to user | approval interrupt |
| human reply | validation record |
| attachment | Evidence Pack artifact |
| task status | Run Graph / ConsultationResult state |

Allowed first step:

```text
study UX and API concepts
compare with OPENWEBUI_INTEGRATION.md
compare with APPROVALS.md
compare with TASK_CONTRACTS.md
```

Forbidden:

```text
become Pantheon scheduler
replace OpenWebUI approval surface
assign autonomous tasks without Task Contract
persist decisions as canonical memory
connect private projects without policy
execute C3-C5 actions through AgentRQ
```

Risk:

```text
parallel task manager
approval bypass
external collaboration surface exposure
state split between AgentRQ and Pantheon
scheduler drift
```

Decision:

```text
Keep AgentRQ as HITL and approval UX inspiration.
Do not integrate it as a task manager or scheduler now.
```

---

## 6. opencode-loop decision

References:

```text
https://github.com/ByBrawe/opencode-loop
https://github.com/sst/opencode
```

Classification:

```text
to_verify
blocked_until_reviewed
rejected_for_core
```

Status:

```text
À vérifier: exact repository behavior, license, loop behavior and write/shell permissions must be inspected before any test.
```

The repository name suggests an automation loop around OpenCode. OpenCode-style coding agents can be useful for software-domain diagnostics, but a looped coding agent is dangerous if it can apply patches repeatedly or mutate files without approval.

Potential Pantheon use after review:

```text
Hermes-side software audit experiment
read-only plan mode inspiration
patch candidate generation in sandbox
regression loop on non-sensitive sample repo
```

Allowed first step:

```text
read documentation
verify license
verify write behavior
verify shell behavior
verify loop stop conditions
verify whether read-only mode exists
```

Forbidden now:

```text
install in Pantheon repo
run on main
write to Pantheon files
direct push
autonomous patch loop
continuous loop on Pantheon repo
C3+ change without approval
access secrets
access Docker socket
```

Risk:

```text
autonomous patch loop
main branch mutation
silent file changes
approval bypass
regression from repeated agent edits
secret or shell exposure
```

Decision:

```text
Block until reviewed.
Only consider later as Hermes-side sandbox tool for software-domain patch candidates.
```

---

## 7. six-hats-skill decision

References:

```text
https://github.com/juanallo/six-hats-skill
```

Classification:

```text
inspiration_only
candidate_method
rejected_for_runtime
```

Six Hats is useful as a structured reasoning method, not as an executable dependency. It can enrich Pantheon skills by forcing distinct perspectives before synthesis.

Pantheon-compatible mapping:

| Six Hats lens | Pantheon role mapping | Use |
|---|---|---|
| White hat | ARGOS | facts, sources, extraction |
| Red hat | IRIS / HECATE | user friction, perception, ambiguity |
| Black hat | THEMIS / HEPHAISTOS | risk, veto, feasibility, compliance |
| Yellow hat | ATHENA | value, opportunity, usable path |
| Green hat | PROMETHEUS | alternatives, variants, blind spots |
| Blue hat | ZEUS / APOLLO | process, arbitration, final quality gate |

Potential Pantheon use:

```text
knowledge_selection reasoning lenses
Evidence Pack completeness check
architecture_fr risk review
client_message_safety review
postmortem structure
workflow arbitration checklist
```

Allowed first integration:

```text
method section inside domains/general/skills/knowledge_selection/
no dependency
no external runtime
no automatic activation outside Task Contract
```

Forbidden:

```text
install as active external skill by default
replace Pantheon agent roles
create autonomous Six Hats agent workers
decide without source evidence
override THEMIS/APOLLO vetoes
```

Risk:

```text
method overuse
longer outputs without better evidence
role duplication
style framework replacing governance
```

Decision:

```text
Use Six Hats as a candidate method inside Pantheon skills.
It is especially relevant for knowledge_selection and review workflows.
```

---

## 8. Integration impact on knowledge_selection

These five options suggest two additions to the future `knowledge_selection` candidate skill.

### 8.1 AKS-inspired provenance fields

The skill should consider, at minimum:

```text
source_id
source_tier
reliability_level
privacy_level
project_scope
last_checked
last_corroborated
confidence
contributing_documents
traversal_path
limitations
```

### 8.2 Six-Hats-inspired selection lenses

The skill may use a lightweight lens pass:

```text
ARGOS / White: what sources exist?
THEMIS / Black: what sources are forbidden or risky?
ATHENA / Yellow: which source set is most useful?
PROMETHEUS / Green: what alternative source path exists?
HECATE / Red: where is ambiguity or user-intent risk?
APOLLO / Blue: what final source set is defensible?
```

Rule:

```text
The method can structure selection.
It cannot replace source-tier, privacy, freshness and Evidence Pack requirements.
```

---

## 9. Approval summary

| Action | Approval |
|---|---|
| Add these reviews to governance docs | C1/C3 depending persistence |
| Read documentation only | C0 |
| Test Kanwas on non-sensitive sample data | C2/C3 |
| Test AKS on sample data | C2 |
| Test AgentRQ in isolated lab | C2/C3 |
| Test opencode-loop on sample repo | C3 minimum |
| Run opencode-loop on Pantheon repo | C3/C5 depending write access |
| Integrate six-hats as method text | C1/C3 |
| Install any of these as runtime dependency | C3/C5 depending capability |
| Connect private data | C4 |
| Enable write/shell/secrets | C5 |

---

## 10. Final rule

```text
These tools may inform Pantheon.
They must not become Pantheon.
```
