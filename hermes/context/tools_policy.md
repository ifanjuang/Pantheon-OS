# Tools policy — context for Hermes

> Compact orientation. Source of truth: `docs/governance/EXTERNAL_TOOLS_POLICY.md`,
> `docs/governance/EXTERNAL_RUNTIME_OPTIONS.md`,
> `docs/governance/EXTERNAL_AI_OPTION_REVIEWS.md`,
> `docs/governance/EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md`,
> `docs/governance/EXTERNAL_RUNTIME_OPTION_REVIEWS_KANWAS_AKS_AGENTRQ_OPENCODE_SIX_HATS.md`,
> `docs/governance/APPROVALS.md`,
> `docs/governance/TASK_CONTRACTS.md`,
> `docs/governance/MODEL_ROUTING_POLICY.md`.

Status: **Documented / not runtime**.

---

## 1. Default posture

```text
Unknown tools are blocked until reviewed.
External tools are capabilities, not authorities.
External runtimes may assist Pantheon but must not become Pantheon.
External memory runtimes may be studied but must not become Pantheon Memory.
```

Default classification for any unknown tool:

```yaml
status: blocked
approval_level: C5
sandbox_required: true
secrets_access: forbidden
shell_access: forbidden
memory_access: none
network_exposure: none
```

A blocked tool may be reconsidered only through explicit review and an update to the relevant governance policy or review file under `docs/governance/`.

---

## 2. Allowed status values

```text
allowed   → may be used inside policy and task contract
test      → sandbox only, no production use
blocked   → blocked by default, only revisitable through review
rejected  → rejected for Pantheon use
watch     → tracked as inspiration / future candidate, no execution
```

Supplemental external option reviews may also use more specific labels such as:

```text
test_read_only
watch
inspiration_only
candidate_method
rejected_for_core
rejected_for_runtime
blocked_until_reviewed
to_verify
```

When in doubt, the stricter interpretation wins.

---

## 3. C-level mapping (summary)

| Action | Default level |
|---|---:|
| read file | C0 |
| search files | C0 |
| web search / extract | C0 / C1 |
| draft response / report | C1 |
| reversible local action | C2 |
| write file / patch candidate | C3 |
| safe diagnostic shell | C3 |
| local service install | C3 |
| OpenWebUI plugin install one-by-one | C3 |
| Hermes plugin install | C3 / C5 depending on capability |
| MCP server install | C3 / C4 |
| memory plugin install | C4 |
| external communication / web side effect | C4 |
| destructive shell / overwrite / force | C5 |
| secret access | C5 |
| Docker socket | C5 |
| batch plugin install | C5 / blocked |
| remote MCP server | C5 / blocked until audited |

Reference: `docs/governance/APPROVALS.md` and `docs/governance/EXTERNAL_TOOLS_POLICY.md`.

---

## 4. Forbidden by default

The following are forbidden by default and require an explicit policy gate before any use:

- shell access for destructive or privileged operations;
- secret or credential access;
- Docker socket access;
- privileged volume mounts;
- public exposure of admin dashboards;
- batch installation of plugins from a remote source;
- self-evolution that mutates active skills, workflows or policies;
- runtime authority frameworks that would replace Pantheon governance;
- external memory runtimes that would replace Pantheon Memory;
- remote MCP servers that are not audited;
- direct repository mutation outside an approved task contract;
- memory promotion without Evidence Pack and approval;
- dream/consolidation passes on Pantheon data through external memory tools.

---

## 5. Canonical and classified tool families

Hermes must follow the governance documents, not memory of past behavior.

### 5.1 Tool policy entries

Covered primarily by `docs/governance/EXTERNAL_TOOLS_POLICY.md`:

```text
Stirling-PDF
OpenWebUI extensions
Hermes plugins
AgentScope
Hermes self-evolution
BrainAPI2
GBrain
Cycles / runcycles
Omnigraph
SearXNG
```

### 5.2 Runtime and framework options

Covered primarily by `docs/governance/EXTERNAL_RUNTIME_OPTIONS.md`:

```text
LangChain / LangGraph
Langflow
OpenClaw
OpenAI Symphony
Graphify
RAGFlow
Thoth
kontext-brain-ts
Layer Infinite / Layer
CTX
Binderly
NeverWrite
```

### 5.3 AI option reviews

Covered primarily by `docs/governance/EXTERNAL_AI_OPTION_REVIEWS.md`:

```text
AnimoCerebro
Caliber / ai-setup
```

### 5.4 Supplemental option reviews

Covered by `docs/governance/EXTERNAL_RUNTIME_OPTION_REVIEWS_KANWAS_AKS_AGENTRQ_OPENCODE_SIX_HATS.md`:

```text
Kanwas
AKS Reference Server
AgentRQ
opencode-loop
six-hats-skill
```

Covered by `docs/governance/EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md`:

```text
OpenConcho
Honcho
```

When a tool listed above is involved, re-read the relevant governance file before use.

---

## 6. Current integration status summary

The following summaries are orientation only. The governing files listed above remain authoritative.

| Tool / family | Current orientation for Hermes |
|---|---|
| Stirling-PDF | External document/PDF capability under policy |
| SearXNG | Local search capability under policy |
| OpenWebUI extensions | Not installed by default; one-by-one policy review |
| Hermes plugins | Not installed by default; sandbox and capability review |
| RAGFlow | Optional `test_read_only` external Knowledge/RAG engine, rejected for core |
| Thoth | `inspiration_only`, rejected for core runtime |
| kontext-brain-ts | `watch` / `test_read_only`, possible inspiration for `knowledge_selection` |
| Kanwas | `watch` / `inspiration_only`, workspace/board UX inspiration |
| AKS Reference Server | `watch` / `test_read_only`, provenance and Knowledge schema inspiration |
| AgentRQ | `test_lab_only` / `watch`, HITL approval UX inspiration |
| opencode-loop | `to_verify` / `blocked_until_reviewed`, no use before audit |
| six-hats-skill | `inspiration_only` / `candidate_method`, no runtime dependency |
| OpenConcho | `watch` / `test_lab_only`, memory inspection UX inspiration |
| Honcho | `watch` / `test_read_only`, external memory benchmark only |
| LangChain / LangGraph | Possible Hermes-side library later; rejected for Pantheon core |
| Langflow | Lab-only visual prototyping, not workflow authority |
| OpenClaw | Blocked until reviewed; not Hermes replacement |
| Symphony | Watch / inspiration for lifecycle and workspace patterns only |
| Graphify | Read-only graph audit candidate on non-sensitive snapshots |
| Caliber / ai-setup | Read-only inspiration for Doctor/config parity |

---

## 7. Not integrated means not callable

If a tool is classified as `watch`, `inspiration_only`, `candidate_method`, `to_verify`, `blocked_until_reviewed`, `rejected_for_core` or `rejected_for_runtime`, Hermes must not treat that as permission to call, install or connect it.

Default decision for non-integrated tools:

```yaml
status: not_integrated
default_decision: documentation_review_only
auto_call_allowed: false
auto_install_allowed: false
memory_authority: false
source_of_truth: false
```

Allowed action without further approval:

```text
read governance classification
summarize classification
use documented ideas as method inspiration when explicitly incorporated into Pantheon docs
```

Forbidden action without further approval:

```text
call the tool
install the tool
connect private data
connect secrets
connect shell
connect Docker socket
sync memory
canonize outputs
run background consolidation
```

---

## 8. Fallback rule

A fallback cannot replace a blocked path with an unreviewed path. Allowed fallback only if:

- intent is unchanged;
- tool stays allowlisted;
- risk is equal or lower;
- data exposure does not increase silently;
- Evidence Pack records the substitution.

Forbidden fallback regardless of context:

```text
unallowlisted tool
destructive action
external send
secret access
Docker socket
memory write
plugin installation
batch install
remote MCP server not audited
external memory consolidation
autonomous patch loop
```

---

## 9. Pre-flight checklist before using any external tool

1. Locate the relevant entry in the governance policy or review file.
2. Confirm `status` allows the intended use.
3. Confirm `approval_level` matches the task contract.
4. Confirm `allowed_usage` covers the action.
5. Confirm `forbidden_usage` does not block the action.
6. Confirm sandbox / network / secrets / shell constraints.
7. Confirm memory access and memory promotion constraints.
8. Confirm rollback is defined.
9. Record the use in the Evidence Pack.

If any step fails, **do not run the tool**.

---

## 10. Final rule

```text
Capabilities, not authorities.
Allowlist, not improvisation.
Policy, contract, evidence, rollback.
```
