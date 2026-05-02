# External memory runtime reviews — OpenConcho and Honcho

> Supplemental review pack for external memory UI/runtime options.
>
> This document does not authorize installation, integration, memory import or runtime use. It classifies OpenConcho and Honcho under Pantheon Next governance.

---

## 1. Doctrine

Pantheon Next keeps the same operating split:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

Memory remains governed by Pantheon:

```text
session -> candidates -> Evidence Pack -> validation -> project/system
```

External memory runtimes may be studied, but they must not become:

```text
Pantheon canonical memory
Pantheon memory promotion system
Pantheon source of truth
Pantheon execution runtime
Pantheon approval authority
```

---

## 2. Summary matrix

| Option | Type | Classification | Pantheon-compatible use | Forbidden use | Priority |
|---|---|---|---|---|---|
| OpenConcho | Desktop/web UI for Honcho | `watch` / `test_lab_only` / `rejected_for_core` | Memory inspection UX, conclusions/sessions/peers dashboard inspiration | Become Pantheon memory UI, trigger consolidation on Pantheon data, canonize memory | P2 |
| Honcho | Agent memory service/library | `watch` / `test_read_only` / `rejected_for_core` | External memory-system benchmark, peer/session/conclusion model inspiration, context hydration study | Replace Pantheon Memory, auto-promote facts, run continual learning on project data | P2 |

---

## 3. OpenConcho decision

References:

```text
https://github.com/offendingcommit/openconcho
```

Classification:

```text
watch
test_lab_only
rejected_for_core
```

OpenConcho is a desktop/web interface for self-hosted Honcho instances. It exposes workspaces, peers, sessions, conclusions, webhooks, chat with memory context and manual dream/consolidation actions.

Potential Pantheon use:

```text
memory inspection UX inspiration
candidate memory review UI inspiration
session and conclusion browsing pattern
local connection privacy pattern
future Memory Candidate Review dashboard inspiration
```

Pantheon-compatible reclassification:

| OpenConcho concept | Pantheon-compatible form |
|---|---|
| dashboard | future operations/memory review view inspiration |
| peers | possible UX analogy only; not Pantheon agents |
| sessions | session context display inspiration |
| conclusions | memory candidate or evidence finding display inspiration |
| chat with memory context | not allowed as Pantheon authority |
| schedule dream | not allowed on Pantheon memory |
| webhooks | blocked unless separately reviewed |

Allowed first step:

```text
read documentation
study UX screenshots/patterns
compare with MEMORY.md and MEMORY_EVENT_SCHEMA.md
no installation
no Pantheon data
```

Forbidden:

```text
replace OpenWebUI
replace Pantheon memory review process
connect to Pantheon project data
trigger dream/consolidation on Pantheon memory
canonize conclusions
write memory candidates automatically
use webhooks without external tool policy
```

Risk:

```text
parallel memory UI
conclusion drift
manual consolidation bypassing approvals
webhook side effects
confusion between Honcho conclusions and Pantheon memory
```

Decision:

```text
Keep OpenConcho as memory UX inspiration only.
Do not integrate it as Pantheon memory UI or runtime.
```

---

## 4. Honcho decision

References:

```text
https://github.com/plastic-labs/honcho
```

Classification:

```text
watch
test_read_only
rejected_for_core
```

Honcho is an external memory library/service for stateful agents. It models workspaces, peers, sessions, messages, collections, documents, context, search, chat, representations, summaries and background derivation/consolidation.

Potential Pantheon use:

```text
external memory-system benchmark
peer/session/conclusion model inspiration
context hydration comparison
memory inspection vocabulary comparison
source of ideas for candidate memory review UX
```

Pantheon-compatible reclassification:

| Honcho concept | Pantheon-compatible form |
|---|---|
| workspace | project/system scope analogy only |
| peer | entity/participant concept to study; not Pantheon agent |
| session | session memory analogy |
| conclusion | memory candidate or extracted claim, not canonical memory |
| context endpoint | context pack inspiration, not authority |
| representation | candidate summary, not canonical fact |
| dream/consolidation | not allowed except as inspiration for manual candidate review |

Allowed first step:

```text
read documentation
study schema and API concepts
compare with MEMORY.md
compare with MEMORY_EVENT_SCHEMA.md
compare with EVIDENCE_PACK.md
use public/sample toy data only if later approved
```

Forbidden:

```text
replace Pantheon Memory
replace memory/candidates -> project/system validation flow
auto-promote Honcho conclusions to Pantheon memory
run background learning on private project data
connect to OpenWebUI/Hermes production without policy
use Honcho chat endpoint as governance authority
store secrets or sensitive data
```

Risk:

```text
continual learning outside governance
parallel memory authority
agent personalization drift
private data retention
LLM-provider leakage if misconfigured
memory conclusions treated as facts
```

Decision:

```text
Honcho may be studied as an external memory benchmark.
It must not become Pantheon canonical memory or automatic consolidation layer.
```

---

## 5. Relationship to Pantheon memory doctrine

Pantheon memory remains:

```text
session: temporary context
candidates: persisted but not validated
project: validated project context
system: validated reusable methods and rules
```

OpenConcho/Honcho must not alter this lifecycle.

If studied later, any output must be reclassified as:

```text
observation
candidate
unsupported conclusion
source pointer
UX inspiration
```

A Honcho conclusion is not Pantheon evidence unless it links back to:

```text
source document
source chunk or message
tool/action trace
Evidence Pack
approval record
```

---

## 6. Approval summary

| Action | Approval |
|---|---|
| Read OpenConcho/Honcho documentation | C0 |
| Add governance review | C1/C3 depending persistence |
| Install locally with toy data | C2/C3 |
| Run on Pantheon repo docs only | C3 |
| Run on private project/client data | C4 |
| Enable webhooks | C4/C5 depending side effects |
| Enable dream/consolidation on Pantheon data | blocked by default |
| Import Honcho conclusions into Pantheon memory | C3 minimum as candidate only, never direct |
| Use Honcho as memory backend | rejected for core |

---

## 7. Impact on future Pantheon work

Useful later for:

```text
Memory Candidate Review UX
Run/session inspection UX
candidate conclusion browsing
manual memory review screen
context hydration comparison
```

Not useful now for:

```text
Knowledge Selection candidate skill activation
Hermes context export creation
OpenWebUI Router Pipe definition
Pantheon Domain API extension
```

---

## 8. Final rule

```text
OpenConcho can inspire memory inspection.
Honcho can benchmark memory concepts.
Neither can canonize Pantheon memory.
```
