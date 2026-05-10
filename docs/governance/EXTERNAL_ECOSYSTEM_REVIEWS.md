# EXTERNAL ECOSYSTEM REVIEWS — Pantheon Next

> Candidate review register for external repositories and ecosystems.
>
> External tools may inspire Pantheon, Hermes Lab or OpenWebUI operations, but must not redefine Pantheon architecture.

---

## 1. Doctrine

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

External repositories are not authorities.

They may become:

```text
benchmark
inspiration
watch item
Hermes Lab candidate
OpenWebUI operations candidate
Knowledge publication candidate
skill candidate inspiration
blocked for core
rejected
```

They must not become:

```text
Pantheon runtime
Pantheon memory authority
Pantheon approval authority
Pantheon scheduler
Pantheon tool runtime
Pantheon provider router
Pantheon orchestration engine
```

---

## 2. Review states

| State | Meaning |
|---|---|
| `benchmark` | Useful pattern source only |
| `watch` | Track, do not use yet |
| `candidate_dev_tool` | Possible local/operator aid after review |
| `hermes_lab_only` | May be tested only in isolated Hermes Lab |
| `openwebui_ops_candidate` | May support OpenWebUI administration only |
| `knowledge_publication_candidate` | May publish source docs into Knowledge, never memory |
| `blocked_for_core` | Must not enter Pantheon core |
| `rejected_for_core` | Not useful or too dangerous for core |

---

## 3. Reviewed options

### 3.1 `delivstat/swarmkit`

Classification:

```yaml
name: delivstat/swarmkit
category:
  - declarative_multi_agent_runtime
  - yaml_topology
  - langgraph_compiler
  - mcp_tool_runtime
  - governance_runtime
status:
  - benchmark
  - hermes_lab_only
  - blocked_for_core
```

Useful patterns:

```text
YAML topology as data
agent / skill / governance in declarative schema
IAM-like scopes per agent
pre-tool evaluate_action policy
human-in-the-loop approval gates
hash-chained audit trail
run status / logs / why / gaps / review queue
skill gap detection
knowledge-pack / llms.txt style documentation bundles
sandboxed MCP server pattern
```

Pantheon extraction:

```text
WORKFLOW_SCHEMA.md may borrow topology vocabulary.
APPROVALS.md may borrow IAM-scope vocabulary.
TASK_CONTRACTS.md may borrow pre-action evaluation vocabulary.
EVIDENCE_PACK.md and RUN_GRAPH.md may borrow audit and why/gaps concepts.
SKILL_LIFECYCLE.md may borrow skill-gap reporting concepts.
HERMES_INTEGRATION.md may borrow knowledge-pack export concepts.
```

Forbidden:

```text
Do not install as Pantheon runtime.
Do not compile Pantheon workflows to LangGraph from Pantheon core.
Do not wire MCP servers through Pantheon core.
Do not replace Hermes Agent.
```

Decision:

```text
Reference only for roadmap-external-ecosystem and Hermes Lab experiments.
```

---

### 3.2 `RivoLink/leaf`

Classification:

```yaml
name: RivoLink/leaf
category:
  - markdown_previewer
  - terminal_ui
  - developer_tool
  - documentation_review_aid
status:
  - candidate_dev_tool
```

Useful patterns:

```text
Markdown terminal preview
watch mode for generated Markdown
inline rendering for fzf preview
stdin support for AI-generated Markdown
syntax highlighting and tables
local operator review aid
```

Allowed use:

```text
local Markdown preview
ai_logs review
governance docs review
live preview of generated Markdown
Hermes Lab operator aid
```

Forbidden:

```text
Do not treat as governance authority.
Do not use as Evidence Pack replacement.
Do not install automatically.
Do not mutate files.
```

Decision:

```text
Optional local developer/operator tool only.
```

---

### 3.3 `affaan-m/everything-claude-code`

Classification:

```yaml
name: affaan-m/everything-claude-code
category:
  - claude_code_plugin_ecosystem
  - skills_pack
  - agent_harness_optimization
  - hooks_runtime
  - security_scanning
  - continuous_learning
  - cross_harness_prompting
status:
  - benchmark
  - inspiration_only
  - sandbox_after_review
```

Useful patterns:

```text
selective install profiles
minimal / core / full context surfaces
rules copied by selected language/domain only
advisor for component selection
doctor / repair / uninstall workflow
hook profiles minimal / standard / strict
security scan pattern
skill stocktake
search-first workflow
long-form article writing skill pattern
presentation / frontend slides workflow pattern
market research workflow pattern
eval harness and verification loop patterns
cross-harness packaging discipline
```

Pantheon extraction:

```text
Context modes: lean / standard / full.
Skill loading policy: index first, load only selected skill body.
Use when / Do not use when sections in every skill.
Skill stocktake and benchmark pack before activation.
Deliverable Blueprints for article, report, dossier and presentation.
Security and install discipline for external skill packs.
```

Forbidden:

```text
No full install into Pantheon.
No Claude plugin installation as Pantheon dependency.
No hook runtime in Pantheon.
No continuous learning auto-write.
No automatic skill import.
No automatic memory import.
No marketplace or billing surface adoption.
```

Decision:

```text
Major benchmark for skills, prompts, hooks, security, long-form deliverables and install discipline.
No direct runtime adoption.
```

---

### 3.4 `mage0535/hermes-memory-installer`

Classification:

```yaml
name: mage0535/hermes-memory-installer
category:
  - hermes_memory_extension
  - long_term_memory
  - fts5_retrieval
  - knowledge_graph
  - pgvector
  - embedding_server
  - self_evolution
status:
  - blocked_for_core
  - hermes_lab_only
  - external_memory_runtime_candidate
```

Useful patterns:

```text
memory doctor
backup / restore
weekly cleanup
orphan detection
embedding model selection
AI-assisted install warning
cross-platform path detection
live store vs archive store distinction
Markdown archive philosophy
retrieval pipeline test router
```

Pantheon extraction:

```text
MEMORY_STORAGE_MODEL.md may borrow backup / restore / doctor concepts.
EXTERNAL_TOOLS_POLICY.md should block automatic memory installers by default.
operations/hermes_memory_lab.md may define safe non-sensitive tests later.
```

Forbidden:

```text
No curl | bash install.
No production install.
No cron auto-archive.
No auto-summary on real project data.
No curator self-evolution.
No gbrain production sidecar.
No pgvector backend as Pantheon canonical memory.
No automatic memory consolidation.
No automatic memory promotion.
No client/project data ingestion.
```

Decision:

```text
Useful memory benchmark, but high-risk. Sandbox only, non-sensitive data only, never canonical Pantheon Memory.
```

---

## 4. Extracted roadmap actions

Candidate actions:

```text
Create external_repo_review Task Contract.
Create skill_candidate_security_review skill candidate.
Create openwebui_kb_sync_review skill candidate.
Create hermes_skill_sandbox_review skill candidate.
Create diagram_asset_review skill candidate.
Create operations/hermes_lab.md.
Create operations/hermes_skill_sandbox.md.
Create operations/hermes_memory_lab.md only if memory lab is approved.
Define context modes lean / standard / full.
Add Use when / Do not use when to SKILL_LIFECYCLE.md.
Add skill benchmark packs before activation.
Add source-material prompt registry activation policy.
```

Blocked actions:

```text
batch install from GitHub
runtime adoption from external repo
memory backend replacement
community skill activation without review
MCP server installation without policy
self-evolution auto-merge
hook runtime activation without review
OpenWebUI cockpit replacement
Hermes runtime replacement
```

---

## 5. Final rule

```text
Study external repositories.
Extract patterns.
Do not import authority.
Do not import runtime.
Do not import memory.
```
