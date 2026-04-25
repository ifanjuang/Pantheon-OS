# Pantheon OS — Modules
## Overview
Pantheon Next is built from modular runtime blocks.
The system distinguishes between:
- core runtime logic
- reusable runtime modules
- domain overlays
- platform and infrastructure
This document defines how modules are organized, discovered, validated, activated, and composed.
A module is not just a folder.
A module is a runtime unit with:
- an identity
- a contract
- a manifest
- a lifecycle
- explicit dependencies
- controlled activation
---
# 1. Module Philosophy
## 1.1 Modular by default
Everything that may vary, evolve, or be replaced should live outside the core.
This includes:
- agents
- skills
- tools
- workflows
- prompts
- templates
The core provides execution, governance, contracts, state, and registries.
Modules provide behavior.
## 1.2 Filesystem is the source of truth
A module must be discoverable from the filesystem.
Adding or removing a module should primarily mean:
- adding or removing a folder
- adding or removing a manifest
- satisfying runtime contract requirements
The runtime should not require hardcoded registration for every new block.
## 1.3 Core and modules must stay separated
The core must not absorb domain logic.
Modules must not reimplement core governance.
The boundary is:
- core decides how execution works
- modules define what gets executed
## 1.4 Modules must be explicit
Every module must declare:
- what it is
- what it depends on
- what it produces
- when it should be used
- when it should not be used
---
# 2. Main Module Families
Pantheon uses six primary module families.
## 2.1 Agents
Agents are reasoning units.
They:
- interpret tasks
- produce structured outputs
- call skills and tools through runtime control
- participate in workflows
Agents do not own global orchestration by default unless that is their defined role.
## 2.2 Skills
Skills are reusable reasoning capabilities.
They:
- encapsulate repeatable cognitive work
- define narrow scope
- remain testable independently
- do not own side-effectful execution
A skill is not a persona.
It is a reusable capability block.
## 2.3 Tools
Tools are technical or external action interfaces.
They:
- fetch
- read
- transform
- call services
- write outputs
- perform bounded actions
Tools must be narrow, explicit, and governed by policy.
## 2.4 Workflows
Workflows structure execution.
They define:
- agent sequencing
- dependencies
- execution patterns
- pause points
- validation points
- fallback logic
A workflow is explicit execution structure, not a prompt chain.
## 2.5 Prompts
Prompts define behavioral framing and instructions.
They may include:
- system prompts
- domain overlays
- skill prompts
- output constraints
- style or tone rules where relevant
Prompts do not replace runtime logic.
## 2.6 Templates
Templates define output structure.
They may include:
- report templates
- dossier templates
- structured response skeletons
- communication formats
- domain-specific document shells
Templates should be reusable and independently versionable.
---
# 3. Repository Structure
## 3.1 Generic runtime modules
```text
modules/
  agents/
  skills/
  tools/
  workflows/
  prompts/
  templates/

3.2 Domain overlays

domains/
  architecture/
    agents/
    skills/
    workflows/
    prompts/
    templates/
    policies/
    trusted_sources/
  legal/
  software/

3.3 Core runtime

core/
  contracts/
  registry/
  decision/
  execution/
  state/
  policies/
  evaluation/
  learning/
  observability/
  memory/
  documents/
  llm/

3.4 Platform layer

platform/
  api/
  ui/
  data/
  infra/

⸻

4. Module Discovery

4.1 Discovery model

Modules are discovered at runtime through manifests.

The loader scans known directories such as:

* modules/agents/
* modules/skills/
* modules/tools/
* modules/workflows/
* domains/*/agents/
* domains/*/skills/
* domains/*/workflows/

4.2 Discovery rules

A module is considered loadable if:

* the folder exists
* a valid manifest exists
* required implementation files exist
* contract validation succeeds

If manifest validation fails, the module should not load silently.

4.3 Registries

The runtime should maintain separate registries for:

* AgentRegistry
* SkillRegistry
* ToolRegistry
* WorkflowRegistry
* PromptRegistry later if needed
* TemplateRegistry later if needed

Registries are runtime indexes, not the source of truth.
The source of truth remains the filesystem + manifest.

⸻

5. Manifest Model

5.1 Manifest purpose

A manifest is the runtime contract summary for a module.

It should be lightweight, explicit, and machine-readable.

5.2 Recommended manifest fields

Most modules should eventually support fields such as:

* id
* name
* type
* version
* description
* enabled
* layer
* domain
* inputs
* outputs
* dependencies
* constraints
* policy
* activation
* tags

Not every field is required in phase one, but the model should evolve in this direction.

5.3 Identity fields

id

Stable runtime identifier.

name

Human-readable name.

type

One of:

* agent
* skill
* tool
* workflow
* prompt
* template

version

Module version or revision marker.

5.4 Contract fields

inputs

Expected inputs.

outputs

Expected outputs.

dependencies

Required skills, tools, workflows, models, or runtime features.

constraints

What the module cannot or must not do.

policy

Approval or restriction metadata where relevant.

5.5 Runtime fields

enabled

Whether the module is available for loading.

activation

Optional hints about when the runtime may use the module.

domain

Optional domain association such as:

* core
* architecture
* legal
* software

⸻

6. Module Contracts by Type

6.1 Agent contract

An agent module should define:

* role
* responsibilities
* limits
* activation logic
* input shape
* output shape
* optional veto capability
* optional criticity triggers

An agent should usually include:

agent.py
manifest.yaml
SOUL.md
tests/

Optional:

skills/
config.yaml
examples/

6.2 Skill contract

A skill module should define:

* capability scope
* clear inputs
* clear outputs
* use conditions
* avoid conditions
* failure modes

A skill should usually include:

skill.py
manifest.yaml
SKILL.md
tests/

6.3 Tool contract

A tool module should define:

* what it does
* when to use it
* when not to use it
* side-effect profile
* policy requirements
* expected failure modes

A tool should usually include:

tool.py
manifest.yaml
README.md
tests/

6.4 Workflow contract

A workflow module should define:

* graph or sequence
* participating agents
* dependencies
* execution pattern
* checkpoints
* validation points
* fallback rules

A workflow should usually include:

workflow.py
manifest.yaml
workflow.yaml
tests/

6.5 Prompt contract

A prompt module should define:

* scope
* target module or role
* domain applicability
* constraints
* expected tone or instruction profile

6.6 Template contract

A template module should define:

* target artifact type
* expected sections
* optional domain association
* variable placeholders
* output constraints

⸻

7. Standard Folder Patterns

7.1 Agent module

modules/agents/control/zeus_orchestrator/
  manifest.yaml
  agent.py
  SOUL.md
  tests/

7.2 Skill module

modules/skills/research/crosscheck/
  manifest.yaml
  skill.py
  SKILL.md
  tests/

7.3 Tool module

modules/tools/context/smart_read/
  manifest.yaml
  tool.py
  README.md
  tests/

7.4 Workflow module

modules/workflows/review/decision_review/
  manifest.yaml
  workflow.yaml
  workflow.py
  tests/

7.5 Domain overlay skill

domains/architecture/skills/decision_scoring/
  manifest.yaml
  skill.py
  SKILL.md
  tests/

⸻

8. Domain Overlay Rules

8.1 Domain behavior must stay in overlays

If a capability is domain-specific, it should live under domains/{domain}/, not in generic modules/.

Examples:

* architecture decision debt handling
* legal citation enforcement
* software blast-radius review

8.2 Generic modules must remain portable

A generic module should not assume:

* a specific professional domain
* a specific project phase model
* a specific legal framework
* a specific document taxonomy

8.3 Overlay activation

The runtime should be able to activate overlays through configuration.

Possible dimensions include:

* active domain
* multiple enabled overlays
* overlay priority
* domain-specific policy injection

⸻

9. Activation and Enablement

9.1 Module enablement

A module may be:

* enabled
* disabled
* experimental
* deprecated later if needed

Disabled modules remain present on disk but are not active in runtime discovery.

9.2 Runtime activation is separate from presence

A module can be loadable but not automatically activated.

Examples:

* APHRODITE may exist but not auto-activate
* domain workflows may exist but activate only under one overlay
* some tools may require policy approval before use

9.3 Activation sources

Activation may depend on:

* criticity
* workflow structure
* domain overlay
* side-effect risk
* output type
* uncertainty level
* operator setting

⸻

10. Module Testing

10.1 Every critical module must be testable

Pantheon should support testing at multiple levels:

* unit tests for skills
* tool tests and mocks
* agent tests
* workflow integration tests
* regression tests

10.2 Test focus by module type

Agents

Test:

* role boundaries
* structured outputs
* activation behavior
* failure handling

Skills

Test:

* repeatability
* edge cases
* explicit scope
* output consistency

Tools

Test:

* API failures
* timeout handling
* side-effect boundaries
* policy integration

Workflows

Test:

* execution order
* dependencies
* pause/resume
* fallback behavior
* criticity handling

⸻

11. Versioning and Lifecycle

11.1 Modules evolve independently

Skills, workflows, and overlays should eventually support explicit versioning.

Examples:

* workflow versions
* skill revisions
* overlay revisions

11.2 Workflow lifecycle

A workflow pack may move through states such as:

* draft
* candidate
* active
* archived

11.3 Skills lifecycle

Skills may later support:

* versioned release
* test-backed promotion
* deactivation without deletion
* canonical registry identity

11.4 Backward compatibility

The system should try to preserve compatibility where reasonable.
Breaking changes must be explicit.

⸻

12. Governance Constraints for Modules

12.1 No uncontrolled side effects

No module may perform risky side effects outside runtime policy control.

12.2 No hidden business logic in core

If a module encodes business-specific behavior, it belongs in overlays or explicit modules, not the core runtime.

12.3 No silent module mutation

Learning may suggest improvements, but runtime should not silently rewrite active modules in place.

12.4 No implicit dependencies

A module must not depend on hidden files, hidden prompts, or undocumented sequencing assumptions.

Dependencies must be declared.

⸻

13. Hermes Console Expectations

The Hermes Console should eventually expose module-level visibility.

For each module, the console should be able to show:

* id
* type
* domain
* enabled state
* version
* dependencies
* usage metrics
* recent failures
* activation context

This is especially important for:

* skills
* workflows
* tools
* domain overlays

⸻

14. Recommended Naming Rules

14.1 Folder naming

Use stable, descriptive snake_case folder names.

Examples:

* zeus_orchestrator
* crosscheck
* smart_read
* decision_review

14.2 IDs

Module ids should be:

* stable
* machine-friendly
* unambiguous
* independent of temporary naming experiments

14.3 Identity vs role

Identity and role should remain separable.

Example:

* mythic identity: zeus
* role: orchestrator

This keeps naming expressive without weakening runtime clarity.

⸻

15. Anti-Patterns

Avoid the following:

* one module doing everything
* tools that make legal or policy judgments
* skills with vague scope
* workflows hidden inside prompts
* domain logic hardcoded into core
* modules that require undocumented ordering assumptions
* side effects outside policy gates
* silent runtime activation of decorative agents in critical runs

⸻

16. Final Rule

Modules are the execution fabric of Pantheon Next.

A good module is:

* explicit
* bounded
* testable
* discoverable
* replaceable
* governable

If a module cannot be understood through its manifest, contract, and tests, it is too implicit for production use.