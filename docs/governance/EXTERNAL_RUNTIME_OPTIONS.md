# EXTERNAL RUNTIME OPTIONS — Pantheon Next

> Classification of optional runtimes, AI workflow frameworks, context engines and graph/workspace tools that may interact with Pantheon Next.

---

## 1. Principle

Pantheon Next must not absorb every attractive agent framework into its core.

External runtimes and workflow tools are allowed only if they preserve the operating split:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

An external runtime may be useful, but it must not become the source of truth for:

```text
domains
agents
skills
workflows
approvals
memory
Evidence Packs
external tools policy
```

---

## 2. Classification statuses

| Status | Meaning |
|---|---|
| `allowed_as_library_in_hermes` | May be used by Hermes-side executable skills as an implementation library |
| `test_lab_only` | May be used in isolated experiments or visual prototyping, not production governance |
| `test_read_only` | May be tested read-only on non-sensitive data or sandbox repositories |
| `blocked_until_reviewed` | Must not be installed or connected before security/governance review |
| `to_verify` | Insufficiently reviewed; no integration decision yet |
| `watch` | Interesting but not actionable now |
| `rejected_for_core` | Must not become a Pantheon core component |

---

## 3. Evaluation matrix

| Tool | Type | Status | Pantheon fit | Allowed use | Forbidden use | Priority |
|---|---|---|---|---|---|---|
| Hermes Agent | Execution runtime | canonical external runtime | Primary execution runtime | Execute Task Contracts, return Evidence Packs, apply policies | Canonize memory or mutate governance without approval | P0 |
| LangChain / LangGraph | Agent/workflow library | `allowed_as_library_in_hermes` | Useful implementation library for Hermes skills | Retrieval, structured output, tools, controlled workflows inside Hermes | Become Pantheon runtime, provider router or hidden autonomy layer | P2 |
| Langflow | Visual AI workflow lab | `test_lab_only` | Useful for visual prototyping | Prototype flows, visualize chains, export lessons to `WORKFLOW_SCHEMA.md` | Define canonical workflows, execute sensitive tasks, bypass approvals | P2/P3 |
| OpenAI Symphony | Issue-tracker orchestration spec / runner | `watch` / `rejected_for_core` | Strong inspiration for Task Contract lifecycle, isolated workspaces and proof-of-work | Study workspace/run/handoff patterns; adapt concepts into schemas | Become Pantheon scheduler, runner or autonomous issue executor | P2/P3 |
| OpenClaw | Autonomous personal AI runtime | `blocked_until_reviewed` | Powerful but risky and runtime-overlapping | Future external runtime experiment in sandbox only | Replace Hermes, access secrets/repo/files, run C3-C5 actions, write memory | P3 |
| Graphify | Repo/document graph tool | `test_read_only` | Strong fit for repo/code/docs graph audit | Read-only graphing of repo/docs, produce graph reports for Evidence Packs | Become canonical memory, auto-update graph on private data without policy | P1/P2 |
| Layer Infinite / Layer | AI app/workflow platform | `to_verify` | Unclear fit | Watch or verify documentation before decision | Treat as Pantheon runtime without audit | P3 |
| CTX | Context runtime engine for coding agents | `to_verify` | Relevant but overlaps context packs/Hermes memory | Study context packing, repo indexing and local retrieval ideas | Become Pantheon runtime or memory authority | P2/P3 |
| Binderly | Document/export/workspace tool | `to_verify` | Potentially useful for packaging/export | Verify for Markdown/PDF/export workflows | Become source of truth or memory layer | P3 |
| NeverWrite | Local-first Markdown/AI workspace | `watch` | Interesting workspace model, but overlaps Obsidian/OpenWebUI | Study review/change-control ideas | Become Pantheon source of truth or parallel domain workspace | P3 |

---

## 4. LangChain / LangGraph decision

Classification:

```text
allowed_as_library_in_hermes
rejected_for_core
```

Use LangChain/LangGraph only as an implementation detail inside Hermes-side executable skills or labs.

Allowed:

```text
Hermes skill uses LangChain for structured output
Hermes skill uses retrieval chains
Hermes skill uses a bounded graph workflow under Task Contract
```

Forbidden:

```text
Pantheon creates a LangGraph central orchestrator
Pantheon creates an Execution Engine
Pantheon creates a Tool Runtime
Pantheon creates a provider router
Pantheon stores runtime state as canonical memory
```

Required controls:

```text
Task Contract
allowed tools
forbidden tools
Evidence Pack
approval checks
fallback behavior
```

---

## 5. Langflow decision

Classification:

```text
test_lab_only
rejected_for_core
```

Langflow may be used as a visual prototyping lab.

Allowed:

```text
prototype a document review chain
prototype a retrieval flow
prototype a validation sequence
convert findings into WORKFLOW_SCHEMA.md
```

Forbidden:

```text
canonical workflow authority
production approval engine
direct private data processing without policy
direct mutation of Pantheon repo or memory
OpenWebUI replacement
Hermes replacement
```

Rule:

```text
A Langflow flow is a prototype artifact, not Pantheon governance.
```

---

## 6. OpenAI Symphony decision

Classification:

```text
watch
rejected_for_core
```

References:

```text
https://github.com/openai/symphony
https://github.com/openai/symphony/blob/main/SPEC.md
https://openai.com/index/open-source-codex-orchestration-symphony/
```

Symphony is useful to Pantheon as an orchestration reference because it describes a long-running service that reads work from an issue tracker, creates isolated per-issue workspaces, launches coding-agent sessions, manages bounded concurrency, retries, reconciliation and observability, and loads workflow behavior from a repository-owned `WORKFLOW.md`.

Compatible ideas to study:

```text
one task / ticket = one isolated workspace
repo-owned workflow contract
bounded concurrency
run reconciliation
retry and backoff policy
human handoff state
proof-of-work output
structured run logs
workspace lifecycle hooks
tracker state awareness
```

Pantheon-compatible reclassification:

| Symphony concept | Pantheon-compatible form |
|---|---|
| `WORKFLOW.md` | `WORKFLOW_SCHEMA.md` / Task Contract template |
| issue tracker candidate | Task Contract candidate |
| isolated issue workspace | Hermes sandbox workspace |
| agent run attempt | Hermes execution attempt |
| run logs | Evidence Pack + Run Graph events |
| Human Review state | approval interrupt / C3-C4-C5 validation |
| retry queue | remediation / rerun policy |
| workspace cleanup | operations / doctor / cleanup policy |

Allowed now:

```text
study SPEC.md
extract schema ideas
compare with TASK_CONTRACTS.md
compare with WORKFLOW_SCHEMA.md
compare with EVIDENCE_PACK.md
compare with HERMES_INTEGRATION.md
```

Allowed later, after review:

```text
read-only local prototype on sample/non-sensitive issue data
sandboxed workspace model experiment
manual comparison with Hermes execution contract
```

Forbidden:

```text
replace Hermes
become Pantheon scheduler
become Pantheon Execution Engine
poll real project trackers without policy
run agents against Pantheon repo automatically
mutate tickets, PRs or files without approval
execute C3-C5 actions without explicit validation
store run state as canonical Pantheon memory
```

Risk:

```text
scheduler drift
runtime duplication
approval bypass
issue tracker becomes hidden control plane
background automation complexity
workspace cleanup hazards
```

Decision:

```text
Use Symphony as inspiration for lifecycle, workspace and proof-of-work patterns.
Do not integrate it as a Pantheon runtime.
Do not install before a dedicated external runtime review.
```

---

## 7. OpenClaw decision

Classification:

```text
blocked_until_reviewed
rejected_for_core
```

OpenClaw overlaps strongly with autonomous runtime behavior.

Potential value:

```text
external channels
automation experiments
skills ecosystem
local assistant patterns
```

Risks:

```text
autonomous tool execution
messaging channel actions
file/system access
secret exposure
memory drift
runtime duplication with Hermes
approval bypass
```

Allowed only after review:

```text
read-only sandbox
no secrets
no repo write
no client data
no Docker socket
no C3-C5 action
Evidence Pack required
```

Forbidden now:

```text
replace Hermes
connect to production Pantheon
write Pantheon memory
install skills/plugins automatically
send external messages
execute shell/filesystem actions
```

---

## 8. Graphify decision

Classification:

```text
test_read_only
```

Graphify is promising for Pantheon software audits because it can turn a folder of code/docs into graph artifacts.

Potential Pantheon use:

```text
repo_md_audit support
code_audit_post_pivot support
document graph report
architecture relation map
Evidence Pack attachment
legacy dependency exploration
```

Allowed first test:

```text
non-sensitive repository snapshot
read-only execution
output to ignored/sandbox folder
manual review of generated graph report
no automatic memory promotion
```

Forbidden:

```text
run on private client/project data without policy
commit generated graph artifacts without review
use inferred graph relations as canonical facts
replace Evidence Pack source tracing
continuous background indexing
```

Required classification in Evidence Pack:

```text
EXTRACTED
INFERRED
AMBIGUOUS
UNSUPPORTED
```

---

## 9. Layer Infinite / Layer decision

Classification:

```text
to_verify
```

The documentation must be reviewed before any Pantheon decision.

Initial guardrail:

```text
Do not install.
Do not connect to private data.
Do not use as workflow authority.
Do not use as asset-generation dependency until classified.
```

---

## 10. CTX decision

Classification:

```text
to_verify
```

CTX is relevant because it focuses on local context runtime, compact retrieval, project rules, code structure, logs, diffs and task context.

Potential Pantheon use:

```text
context-pack optimization inspiration
repo context slicing
local retrieval ideas
operations doctor inspiration
```

Risks:

```text
runtime overlap
parallel memory layer
MCP exposure
context authority drift
```

Allowed next step:

```text
read docs
classify context packing ideas
compare with HERMES_INTEGRATION.md and MEMORY_EVENT_SCHEMA.md
```

Forbidden now:

```text
install into Pantheon repo
make CTX canonical memory
replace Pantheon context packs
expose MCP tools without policy
```

---

## 11. Binderly decision

Classification:

```text
to_verify
```

Potential value depends on actual capabilities.

Candidate use if verified:

```text
Markdown/PDF packaging
project binder export
Evidence Pack export
client-safe deliverable bundling
```

Forbidden before review:

```text
source-of-truth workspace
automatic document publishing
private data export
unreviewed external sync
```

---

## 12. NeverWrite decision

Classification:

```text
watch
rejected_for_core
```

NeverWrite is interesting as a local-first Markdown/AI workspace and review environment.

Potential inspiration:

```text
inline review
change-control UX
graph navigation
local vault workflow
multi-agent review UX
```

Risks:

```text
parallel source of truth
Obsidian/Cursor-like workspace drift
AI workspace replacing governance repo
local HTTP/API exposure
memory confusion
```

Allowed:

```text
study UX ideas
study review/change-control patterns
manual non-sensitive experiment outside Pantheon repo
```

Forbidden:

```text
make NeverWrite the Pantheon vault
store canonical memory there
replace docs/governance
sync private project data without policy
```

---

## 13. Required review checklist for any option

Before moving a tool from `to_verify`, `watch` or `blocked_until_reviewed` to `test_read_only` or `allowed_as_library_in_hermes`, record:

```text
repository URL
documentation URL
license
maintainer activity
local/cloud behavior
network behavior
data retention
secret handling
filesystem access
shell/tool access
MCP exposure
plugin mechanism
side effects
rollback plan
sandbox plan
approval level
Evidence Pack requirements
```

---

## 14. Approval policy

| Action | Approval |
|---|---|
| Read documentation | C0 |
| Add policy entry | C1/C3 depending persistence |
| Run tool read-only on public/sample repo | C2 |
| Run tool on Pantheon repo read-only | C2/C3 |
| Run tool on private project data | C4 |
| Enable write access | C5 |
| Enable shell/filesystem mutation | C5 |
| Enable messaging/email actions | C4/C5 |
| Install plugin ecosystem | C5 |
| Connect secrets | C5 |

---

## 15. Final rule

```text
External runtimes may assist Pantheon.
They must not become Pantheon.
```
