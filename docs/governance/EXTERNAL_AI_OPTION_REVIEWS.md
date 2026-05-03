# EXTERNAL AI OPTION REVIEWS — Pantheon Next

> Focused classification addendum for external AI runtimes, structured-output tools, evaluation tools and AI-configuration tools reviewed after `EXTERNAL_RUNTIME_OPTIONS.md`.

---

## 1. Purpose

This document records targeted reviews for external AI systems that do not yet deserve installation or integration, but may influence Pantheon Next governance.

It complements:

```text
docs/governance/EXTERNAL_RUNTIME_OPTIONS.md
docs/governance/EXTERNAL_TOOLS_POLICY.md
docs/governance/EXECUTION_DISCIPLINE.md
```

Core rule:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

---

## 2. Summary table

| Tool | Repository | Type | Status | Core decision | Pantheon value | Main risk | Priority |
|---|---|---|---|---|---|---|---|
| AnimoCerebro | `xunharry4-source/AnimoCerebro` | external cognitive runtime / brain | `blocked_until_reviewed` | `rejected_for_core` | precheck loop, audit trace, truthfulness boundary | autonomous cognitive runtime drift | P3 |
| Caliber AI Setup | `caliber-ai-org/ai-setup` | AI config sync / audit tool | `test_read_only` / `inspiration_for_doctor` | `rejected_for_core` | doctor/config parity, deterministic AI config scoring, multi-tool alignment | automatic mutation of governance files and learning hooks | P1/P2 |
| Andrej Karpathy Skills | `forrestchang/andrej-karpathy-skills` | coding-agent discipline reference | `inspiration_only` | `adapt_as_doctrine` | smallest safe path, surgical changes, goal-driven execution | imported blindly as hard process or skill pack | P1 |
| Promptfoo | `promptfoo/promptfoo` | prompt / model / RAG evaluation | `candidate_eval_tool` | `allow_sandbox_eval_later` | skill eval, prompt regression, red-team tests | eval tool becomes authority or CI blocker too early | P1/P2 |
| Instructor | `567-labs/instructor` | structured typed outputs | `candidate_adapter_library` | `Hermes_side_candidate` | Pydantic validation, retries, typed Evidence/Task outputs | schema layer becomes runtime authority | P1/P2 |
| Outlines | `dottxt-ai/outlines` | constrained generation | `candidate_structured_generation` | `Hermes_side_candidate` | JSON Schema / regex / grammar constraints, local model output control | tight coupling to model stack | P2 |
| Guidance | `guidance-ai/guidance` | programmable constrained generation | `lab_only` | `not_core_now` | fine-grained generation control, regex/CFG constraints | extra DSL/runtime complexity | P2/P3 |
| DSPy | `stanfordnlp/dspy` | LM program optimization | `lab_only` | `not_core_now` | optimize prompt/RAG programs later | optimization layer bypasses governance or hides prompts | P2/P3 |
| Brainlid LangChain | `brainlid/langchain` | Elixir LangChain implementation | `watch_only` | `not_relevant_now` | useful only if Elixir/Phoenix stack appears | unrelated stack drift | P3 |
| Recursive-Language-Models | `prashant852/Recursive-Language-Models` | recursive context processing / LangGraph runtime example | `watch_test_only` | `sandbox_only` | long-context exploration pattern | recursive autonomous runtime drift | P3 |
| Warp | `warpdotdev/warp` | developer terminal / agentic dev environment | `developer_tool_optional` | `blocked_for_core` | local developer productivity | cloud/agent orchestration parallel to Hermes | P2/P3 |

---

## 3. AnimoCerebro classification

Classification:

```text
blocked_until_reviewed
rejected_for_core
```

Repository:

```text
https://github.com/xunharry4-source/AnimoCerebro
```

### 3.1 Pantheon fit

AnimoCerebro is relevant as an external cognitive-runtime reference, not as a Pantheon component.

Potential ideas worth studying:

```text
Nine Questions loop
allowed / forbidden action precheck
truthfulness boundary
trace_id audit trail
plugin separation language
cognitive decision log vocabulary
```

Pantheon-compatible reclassification:

| AnimoCerebro idea | Pantheon-compatible form |
|---|---|
| Nine Questions loop | Task Contract precheck checklist |
| “What am I allowed to do?” | `APPROVALS.md` + `allowed_tools` |
| “What should I not do even if I can?” | veto / `forbidden_tools` / THEMIS guardrail |
| trace_id audit trail | Evidence Pack run id / task id / tool trace |
| truthfulness boundary | unsupported claims / evidence-required rule |
| plugin separation | External Tools Policy review and sandbox model |

### 3.2 Allowed use

Allowed now:

```text
read documentation
extract governance vocabulary
compare precheck ideas with TASK_CONTRACTS.md
compare audit trail ideas with EVIDENCE_PACK.md
compare truthfulness ideas with APOLLO/THEMIS validation rules
```

### 3.3 Forbidden use

Forbidden:

```text
replace Hermes
add Pantheon cognitive runtime
enable daemon/background autonomy
enable continuous learning
enable automatic long-term memory
enable self-upgrading
connect to OpenClaw without review
connect to private project data
write Pantheon memory
mutate governance Markdown
install plugins automatically
```

### 3.4 Risk

Risk level:

```text
high
```

Reason:

```text
AnimoCerebro is positioned around autonomous cognition, memory, plugins, daemon behavior and self-improvement. Those properties directly conflict with the Pantheon Next pivot if adopted as runtime.
```

Decision:

```text
Keep as inspiration only.
Do not install.
Do not connect.
Do not treat as Pantheon or Hermes replacement.
```

---

## 4. Caliber AI Setup classification

Classification:

```text
test_read_only
inspiration_for_doctor
rejected_for_core
```

Repository:

```text
https://github.com/caliber-ai-org/ai-setup
```

### 4.1 Observed capabilities

Caliber is an AI-configuration setup and maintenance tool. It targets AI-facing repository instruction files and agent configs, including:

```text
CLAUDE.md
CALIBER_LEARNINGS.md
AGENTS.md
copilot-instructions.md
.cursor/rules/*.mdc
.claude/skills/*/SKILL.md
.cursor/skills/*/SKILL.md
.agents/skills/*/SKILL.md
.opencode/skills/*/SKILL.md
.mcp.json
.cursor/mcp.json
.claude/settings.json
```

Notable properties from the upstream documentation:

```text
Node.js >= 20
npx bootstrap flow
deterministic scoring without LLM/API calls
diff review before writes
backup and undo behavior
score comparison against a git ref
pre-commit refresh hooks
session-end refresh hooks
session learning hooks
MCP server discovery
multi-agent config parity across Claude Code, Cursor, Codex, OpenCode and Copilot
optional telemetry with opt-out
```

### 4.2 Pantheon fit

Caliber is relevant because Pantheon Next has many AI-facing configuration files that must remain synchronized with the real repository state.

Potential Pantheon value:

```text
AI config parity across Claude, Cursor, Codex, OpenCode, Copilot and Hermes context exports
checks for stale paths and obsolete references
checks for missing files referenced by governance docs
checks for drift between CLAUDE.md, AGENTS.md, README.md and docs/governance
inspiration for operations/doctor.md
inspiration for repo_md_audit and code_vs_docs_check
inspiration for config scoring without LLM calls
structured patch-candidate review flow
```

Pantheon-compatible reclassification:

| Caliber idea | Pantheon-compatible form |
|---|---|
| deterministic score | operations doctor / repo governance check |
| config freshness | `STATUS.md` / `README.md` / `CLAUDE.md` coherence check |
| multi-tool config generation | suggestion-only config candidate |
| path grounding | code/docs path existence check |
| score comparison against `main` | branch quality report |
| diff review before writes | patch candidate + approval |
| backup / undo | rollback plan requirement |
| skill generation | skill candidate only, never active directly |
| session learning | memory candidates only, never canonical memory |
| MCP discovery | external tool candidate list, never auto-install |
| pre-commit refresh | rejected for Pantheon unless explicitly approved later |

### 4.3 Allowed use

Allowed now:

```text
read documentation
study deterministic scoring
study config freshness criteria
study generated AI config formats
study path-grounding checks
study rollback and undo patterns
extract ideas for operations/doctor.md
extract ideas for repo_md_audit and code_vs_docs_check
```

Allowed later after review:

```text
run score on a sandbox branch
run read-only audit against non-sensitive repo state
generate suggestions only
produce patch candidates only
compare a branch against main for AI-context drift
```

Any future test must be:

```text
read-only or sandbox branch first
no private project data
no automatic commit
no automatic hook installation
no direct mutation of governance source of truth
Evidence Pack required
```

### 4.4 Forbidden use

Forbidden:

```text
auto-refresh hooks on main
pre-commit mutation of governance files
session-end mutation of governance files
automatic overwrite of CLAUDE.md or AGENTS.md
automatic overwrite of hermes/context exports
automatic overwrite of OpenWebUI/Cursor/Copilot configs
automatic MCP discovery / installation
automatic skill activation
community skill installation
learning hooks writing canonical memory
CALIBER_LEARNINGS.md as Pantheon source of truth
auto-commit or auto-merge
telemetry-enabled run on sensitive/private project data
API key or provider config committed to repo
```

### 4.5 Risk

Risk level:

```text
medium
```

Reason:

```text
The audit/scoring model is useful and close to Pantheon Doctor goals, but automatic refresh hooks, session learning hooks, generated configs and MCP discovery could mutate Pantheon governance files, create a parallel memory channel or expose too much environment context without C3/C4/C5 review.
```

### 4.6 Pantheon decision

Decision:

```text
Use as doctor/config-parity inspiration first.
Future testing must be read-only or sandbox-branch only.
Do not install hooks.
Do not let Caliber write canonical Pantheon files automatically.
```

Best next reuse inside Pantheon:

```text
operations/doctor.md
future read-only doctor report
repo_md_audit skill candidate
code_vs_docs_check skill candidate
AI-context drift check
Hermes context export freshness check
```

---

## 5. Andrej Karpathy Skills classification

Classification:

```text
inspiration_only
adapt_as_doctrine
```

Repository:

```text
https://github.com/forrestchang/andrej-karpathy-skills
```

### 5.1 Pantheon fit

Relevant as execution discipline, not as a skill pack to import.

Pantheon-compatible ideas:

```text
think before coding
simplicity first
surgical changes
goal-driven execution
avoid assumptions
avoid unrelated refactors
```

These ideas are adapted in:

```text
docs/governance/EXECUTION_DISCIPLINE.md
```

### 5.2 Allowed use

Allowed:

```text
read and cite as inspiration
adapt principles into Pantheon doctrine
use as contributor discipline reference
use to reinforce single_role_path before workflow
```

### 5.3 Forbidden use

Forbidden:

```text
import as canonical skill pack
install without review
treat upstream wording as Pantheon source of truth
override Pantheon approvals or Evidence Pack rules
```

Decision:

```text
Use as inspiration for execution discipline only.
```

---

## 6. Promptfoo classification

Classification:

```text
candidate_eval_tool
allow_sandbox_eval_later
```

Repository:

```text
https://github.com/promptfoo/promptfoo
```

### 6.1 Pantheon fit

Promptfoo is relevant for evaluation, regression tests and red-team checks around prompts, skills, RAG behavior and model outputs.

Pantheon-compatible uses:

```text
skill candidate evaluation
prompt regression checks
Hermes output checks
Knowledge Selection test cases
approval classification tests
Evidence Pack quality tests
red-team tests for unsafe outputs
model fallback comparison
```

### 6.2 Allowed use

Allowed now:

```text
read documentation
classify capability
create future eval plan
```

Allowed later:

```text
sandbox eval suite on fictive data
CI optional report
non-blocking eval report
skill regression test corpus
```

### 6.3 Forbidden use

Forbidden:

```text
make promptfoo an authority over approvals
make eval scores canonize skills automatically
run against private project/client data without approval
block all CI before baselines are stable
store secrets in eval config
send sensitive prompts to external providers without C4/C5 review
```

Decision:

```text
Best near-term evaluation option.
Add only after fictive test corpus and provider policy are defined.
```

---

## 7. Instructor classification

Classification:

```text
candidate_adapter_library
Hermes_side_candidate
```

Repository:

```text
https://github.com/567-labs/instructor
```

### 7.1 Pantheon fit

Instructor is relevant for typed structured outputs using Pydantic-like schemas and validation/retry behavior.

Pantheon-compatible uses:

```text
EvidencePack schema validation
TaskContractResult schema validation
role_need_statement output validation
workflow_revision_signal output validation
approval_check output validation
Hermes result scorecard validation
```

### 7.2 Allowed use

Allowed now:

```text
read documentation
classify as Hermes-side candidate
study schema/retry pattern
```

Allowed later:

```text
use inside Hermes adapter for typed outputs
use in test harnesses for structured result validation
use only with schemas defined by Pantheon governance
```

### 7.3 Forbidden use

Forbidden:

```text
turn Instructor into a workflow authority
let schemas replace approvals
let retries hide uncertainty or missing evidence
install in Pantheon core before runtime boundary is stable
```

Decision:

```text
Strong Hermes-side candidate for structured outputs.
Not a Pantheon authority.
```

---

## 8. Outlines classification

Classification:

```text
candidate_structured_generation
Hermes_side_candidate
```

Repository:

```text
https://github.com/dottxt-ai/outlines
```

### 8.1 Pantheon fit

Outlines is relevant for constrained generation using JSON Schema, regex or grammar constraints, especially with local/Ollama-compatible model paths.

Pantheon-compatible uses:

```text
strict JSON outputs
schema-constrained Evidence Pack fragments
grammar-constrained role signals
local model output control
structured generation under Hermes
```

### 8.2 Allowed use

Allowed now:

```text
read documentation
classify as structured generation candidate
compare with Instructor for Hermes needs
```

Allowed later:

```text
sandbox structured output tests
Hermes-side local model structured generation
fictive corpus only until policy is stable
```

### 8.3 Forbidden use

Forbidden:

```text
make Outlines a workflow engine
make generation constraints replace validation
couple Pantheon governance to one model runtime too early
use on private data before approval
```

Decision:

```text
Useful candidate for Hermes structured generation, especially local models.
```

---

## 9. Guidance classification

Classification:

```text
lab_only
not_core_now
```

Repository:

```text
https://github.com/guidance-ai/guidance
```

### 9.1 Pantheon fit

Guidance is relevant as a programmable constrained-generation DSL/reference.

Potential value:

```text
fine-grained generation control
regex / grammar / CFG constraints
interleaved control and generation
structured tool-use experiments
```

### 9.2 Risk

Risk:

```text
adds an extra DSL/runtime layer
can obscure control flow
can become a parallel prompt execution framework
```

Decision:

```text
Lab only.
Revisit after Instructor/Outlines comparison.
```

---

## 10. DSPy classification

Classification:

```text
lab_only
not_core_now
```

Repository:

```text
https://github.com/stanfordnlp/dspy
```

### 10.1 Pantheon fit

DSPy is relevant later for LM program optimization, RAG tuning and prompt/program evaluation.

Potential value:

```text
optimize skill prompts
optimize RAG retrieval programs
evaluate prompt/module variants
produce better prompt baselines
```

### 10.2 Risk

Risk:

```text
optimizer hides prompt changes
evaluation process becomes opaque
optimized program bypasses governance review
adds complexity before stable baselines exist
```

Decision:

```text
Lab only for P2/P3.
No core integration until evaluation baselines and governance review are stable.
```

---

## 11. Brainlid LangChain classification

Classification:

```text
watch_only
not_relevant_now
```

Repository:

```text
https://github.com/brainlid/langchain
```

### 11.1 Pantheon fit

This is an Elixir LangChain-style implementation. Pantheon Next currently does not target an Elixir/Phoenix runtime.

Decision:

```text
Watch only.
No integration unless the platform stack changes toward Elixir.
```

---

## 12. Recursive-Language-Models classification

Classification:

```text
watch_test_only
sandbox_only
```

Repository:

```text
https://github.com/prashant852/Recursive-Language-Models
```

### 12.1 Pantheon fit

Relevant as a long-context exploration pattern, not as runtime.

Potential value:

```text
long repo audit exploration
large corpus decomposition
recursive source exploration
multi-document contradiction search
```

### 12.2 Forbidden use

Forbidden:

```text
Pantheon core runtime
Hermes replacement
OpenWebUI direct runtime
workflow authority
memory promotion
project/client data processing
secrets access
Docker socket access
public API exposure
```

Approval:

```text
sandbox test on fictive/non-sensitive data: C3
network, secrets or filesystem broad access: C5
```

Decision:

```text
Keep as lab/watch-only recursive context strategy.
Do not integrate now.
```

---

## 13. Warp classification

Classification:

```text
developer_tool_optional
blocked_for_core
```

Repository:

```text
https://github.com/warpdotdev/warp
```

### 13.1 Pantheon fit

Warp may be useful as a developer terminal. Warp/Oz agent orchestration must not become Pantheon runtime.

Allowed:

```text
local developer terminal
manual repo inspection
manual tests
manual git commands
local productivity workflows
```

Watch-only / blocked for core:

```text
Oz cloud agents
Warp agent workflows
GitHub Action agent integrations
autonomous PR creation
cloud agent execution on private project data
```

Decision:

```text
Developer tool optional.
Not a Pantheon component.
```

---

## 14. Approval policy

| Action | Approval |
|---|---:|
| Read repository/docs | C0 |
| Add classification entry | C1/C3 depending persistence |
| Run Caliber score read-only on sandbox branch | C2 |
| Run Promptfoo on fictive local tests | C2 |
| Run Promptfoo against private/project data | C4 |
| Run Instructor/Outlines sandbox validation on fictive data | C2 |
| Add Instructor/Outlines to Hermes adapter dependencies | C3 |
| Run Recursive-Language-Models sandbox on non-sensitive corpus | C3 |
| Use Warp as local manual terminal | C0 |
| Use Warp/Oz cloud agents on repo | C3/C4 |
| Use any external tool with secrets, broad filesystem or Docker socket | C5 |
| Enable hooks that mutate files | C4/C5 |
| Enable learning hooks | C4/C5 |
| Enable MCP auto-discovery / install | C5 |
| Install plugin/runtime or connect private data | C4/C5 |
| Enable autonomous learning or self-upgrade | C5 / blocked |

---

## 15. Recommended follow-up

Recommended next document:

```text
operations/doctor.md
```

It should include checks inspired by Caliber and execution discipline:

```text
critical Markdown files exist
paths referenced by governance docs exist
forbidden legacy paths are absent or classified
OpenWebUI mapping files exist
model routing config exists
Hermes context exports exist and match governance docs
context pack endpoint is tested
AI-facing config files are not stale
no secret-like values are committed
no automatic hooks are enabled without policy
no MCP config appears without policy
single_role_path remains allowed before workflow escalation
```

Recommended later doc:

```text
docs/governance/EVALUATION.md
```

It should compare:

```text
Promptfoo for eval suites and regression tests
Instructor for typed output validation
Outlines for constrained generation
Guidance for lab-only generation experiments
DSPy for later optimization experiments
```

---

## 16. Final rule

```text
Evaluation tools may measure.
Structured-output tools may constrain.
Developer tools may assist.
None of them becomes Pantheon authority.
```
