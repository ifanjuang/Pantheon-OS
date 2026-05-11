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
| `inspiration_only` | May inspire doctrine or style, but must not be imported verbatim or treated as authority |
| `candidate_dev_tool` | Possible local/operator aid after review |
| `hermes_lab_only` | May be tested only in isolated Hermes Lab |
| `openwebui_ops_candidate` | May support OpenWebUI administration only |
| `knowledge_publication_candidate` | May publish source docs into Knowledge, never memory |
| `blocked_for_core` | Must not enter Pantheon core |
| `rejected_for_core` | Not useful or too dangerous for core |
| `untrusted_discovery_only` | May be read as an untrusted index; no download, install, sign-in or authority |
| `evaluation_candidate` | May inform future benchmark/evaluation workflows after review |
| `documentation_retrieval_candidate` | May help local/read-only Markdown navigation after review |

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

### 3.5 `hermesguide.xyz/directory`

Classification:

```yaml
name: hermesguide.xyz/directory
category:
  - hermes_ecosystem_directory
  - community_index
  - discovery_surface
status:
  - untrusted_discovery_only
  - watch
  - blocked_for_core
```

Evidence notes:

```text
The site presents itself as a Hermes-related directory / guide surface.
External reputation checks classify the domain as suspicious / low-trust at the time of review.
It is not an official Hermes Agent or Nous Research source.
```

Allowed use:

```text
manual discovery of candidate repositories
source leads for later independent verification
no authentication
no downloads
no copy-paste install commands
```

Forbidden:

```text
Do not use as official Hermes documentation.
Do not use as source of configuration truth.
Do not install anything directly from the directory.
Do not sign in.
Do not enter secrets.
Do not treat listed projects as reviewed.
Do not feed client/project data into any linked service.
```

Decision:

```text
Untrusted discovery only. Every linked project must be reviewed from its primary source before any classification or experiment.
```

---

### 3.6 `PrinceGabriel-lgtm/freshcontext-mcp`

Classification:

```yaml
name: PrinceGabriel-lgtm/freshcontext-mcp
category:
  - mcp_connector
  - web_intelligence
  - web_scraping
  - research_expansion
  - freshness_envelope
status:
  - hermes_lab_only
  - watch
  - blocked_for_core
```

Useful patterns:

```text
freshness timestamp envelope
source discovery across GitHub, Hacker News, Reddit, arXiv and market/release sources
research expansion for non-sensitive tasks
tool-level gateway control and call logging as a pattern
```

Allowed use:

```text
non-sensitive Hermes Lab tests
source discovery benchmarks
comparison against SearXNG / official source search
research expansion only under Task Contract
```

Forbidden:

```text
No Pantheon core integration.
No production MCP connector.
No client/project data queries.
No automatic source authority.
No memory promotion.
No external calls without Task Contract and tool policy.
No reliance when connector health is degraded or unknown.
```

Decision:

```text
Potential research-expansion benchmark. Hermes Lab only, non-sensitive data only, blocked for core.
```

---

### 3.7 `lightfeed/resurf`

Classification:

```yaml
name: lightfeed/resurf
category:
  - browser_agent_benchmark
  - reproducible_test_environment
  - evaluation_harness
  - browser_agent_regression
status:
  - evaluation_candidate
  - hermes_lab_only
  - blocked_for_core
  - to_verify
```

Useful patterns:

```text
reproducible browser-agent tests
synthetic or controlled web interaction environments
recorded user interaction trajectories
failure-mode testing
browser automation regression harness
```

Allowed use:

```text
non-sensitive Hermes Lab browser-agent benchmark
future evaluation of browser skills
static review for EVALUATION.md patterns
no live client sites
```

Forbidden:

```text
No Pantheon runtime.
No production browser automation.
No real client web actions.
No external site automation from core.
No OpenWebUI direct tool.
No approval bypass for browser operations.
```

Verification required:

```text
Primary GitHub README must be reviewed directly before any experiment.
License must be checked.
Runtime dependencies must be checked.
Network behavior must be checked.
```

Decision:

```text
Promising evaluation candidate, but not adopted. Keep as Hermes Lab benchmark lead only.
```

---

### 3.8 `Dreeseaw/mdlens`

Classification:

```yaml
name: Dreeseaw/mdlens
category:
  - markdown_retrieval_cli
  - documentation_navigation
  - evidence_pack_helper
  - local_developer_tool
status:
  - documentation_retrieval_candidate
  - candidate_dev_tool
  - watch
  - blocked_for_core_runtime
```

Useful patterns:

```text
Markdown retrieval for AI agents
natural-language question over documentation corpus
bounded evidence pack output
section-level navigation
highlight extraction
context-window discipline
local governance doc search
```

Allowed use:

```text
local read-only repository documentation navigation
ARGOS source inventory helper candidate
Evidence Pack preparation helper candidate
Claude Code local helper candidate
Hermes Lab read-only helper candidate
```

Forbidden:

```text
No Pantheon runtime dependency.
No autonomous agent loop.
No memory promotion.
No approval decision.
No file mutation.
No replacement for ARGOS or APOLLO.
No use as source authority without reading primary files.
```

Verification required:

```text
Primary GitHub README must be reviewed directly before install.
License, release status, binary/install path and dependency surface must be checked.
Name collision with other `mdlens` packages must be avoided.
```

Decision:

```text
Strong candidate for local Markdown navigation and evidence preparation, but only after a small sandbox test on a cloned repo. Not core runtime.
```

---

### 3.9 User-provided `anti-glaze` response style prompt image

Classification:

```yaml
name: anti_glaze_response_style_prompt_image
source: user_provided_image_reference_2026_05_11
category:
  - response_style_pattern
  - critical_review_pattern
  - anti_flattery_pattern
  - epistemic_discipline_pattern
status:
  - inspiration_only
  - blocked_for_core
  - blocked_as_raw_prompt
```

Useful patterns:

```text
No flattery.
No automatic premise validation.
State when a premise is weak, false or unsupported.
Lead with the strongest counterargument when the user appears to assume a fragile position.
Separate fact, hypothesis, risk, decision and confidence.
Use explicit confidence levels when useful.
Do not capitulate under pushback without new evidence.
Accuracy is more important than approval.
```

Pantheon extraction:

```text
IRIS may use the clarity pattern for user-facing language without adopting aggression.
APOLLO may use the non-complacency pattern for final readiness review.
THEMIS may use the risk and limits clarity pattern.
ARGOS may use the evidence-before-confidence pattern.
HECATE may use the uncertainty and hidden-assumption exposure pattern.
ZEUS may use the strongest-counterargument pattern during arbitration.
```

Forbidden:

```text
Do not import the prompt verbatim.
Do not override safety, privacy, legal or ethical constraints.
Do not expose raw chain-of-thought.
Do not remove required limitations or warnings.
Do not adopt aggressive or humiliating tone.
Do not turn contradiction into a style reflex.
Do not treat confidence labels as proof.
Do not use this as a system prompt for Pantheon, Hermes or OpenWebUI.
```

Recommended Pantheon formulation:

```text
Critical clarity, not brutality.
Evidence before confidence.
No flattery.
No hidden certainty.
No raw prompt import.
```

Decision:

```text
Keep as a response-style inspiration pattern only. It may inform future edits to ROLE_SIGNAL_PROFILES.md, REQUEST_ORCHESTRATION.md or EPISTEMIC_CONTROL.md, but only through a separate governance PR.
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
Create markdown_retrieval_tool_review skill candidate.
Create browser_agent_benchmark_review skill candidate.
Create critical_response_style_review candidate.
Create operations/hermes_lab.md.
Create operations/hermes_skill_sandbox.md.
Create operations/hermes_memory_lab.md only if memory lab is approved.
Create operations/markdown_retrieval_lab.md only if mdlens-style tooling is prioritized.
Create operations/browser_agent_eval_lab.md only if browser-agent benchmarking is prioritized.
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
untrusted directory based installation
production browser automation
remote MCP connector use on private data
raw prompt import from social media images
response style prompt as system prompt
safety or approval bypass through style instructions
```

---

## 5. Final rule

```text
Study external repositories.
Extract patterns.
Do not import authority.
Do not import runtime.
Do not import memory.
Do not import raw prompts.
```
