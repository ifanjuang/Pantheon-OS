# REQUEST ORCHESTRATION — Pantheon Next

> Doctrine for classifying, interpreting, enriching and arbitrating user requests before answer or execution.
>
> This document defines METIS request framing, AGORA consultation mode and the general skills used to produce variants, request revisions and keep outputs aligned with the initial brief.

---

## 1. Principle

Not every user request should be answered immediately.

Some requests require first understanding:

```text
what the user really wants
which domain is involved
which information is missing
whether the answer can be given directly
whether assumptions are acceptable
whether a current source check is needed
whether several options should be compared
whether risk, evidence or approval is involved
```

Canonical rule:

```text
METIS frames the request.
ATHENA arranges the method.
ARGOS finds facts and sources.
HECATE exposes uncertainty.
PROMETHEUS proposes variants.
AGORA compares options when needed.
THEMIS blocks unsafe paths.
APOLLO validates coherence and brief adherence.
ZEUS arbitrates.
IRIS formulates.
Hermes executes only under Task Contract.
```

---

## 2. Non-runtime boundary

Request orchestration must not become:

```text
runtime
scheduler
agent loop
autonomous debate engine
automatic web search engine
automatic memory promotion
automatic workflow activation
```

It may only produce:

```text
request classification
interpreted intent
implicit needs
missing context list
source plan
role routing proposal
variant set
revision request
forum review
arbitration summary
brief adherence review
```

---

## 3. METIS role

METIS is the request-framing role.

METIS intervenes when the request is:

```text
vague
ambiguous
multi-domain
technical
regulatory
contractual
financial
legal-sensitive
project-context-dependent
likely to need current sources
likely to need several interpretations
likely to be answered wrongly by a short direct response
```

METIS does not answer as final authority.

METIS produces a bounded framing object:

```yaml
request_frame:
  original_request: null
  classification: null
  interpreted_intent: null
  likely_domain: null
  implicit_needs: []
  missing_context: []
  risk_flags: []
  answer_strategy: null
  recommended_roles: []
  recommended_skills: []
```

Allowed answer strategies:

```text
answer_directly
answer_with_assumptions
ask_targeted_question
expand_context
route_to_workflow
```

---

## 4. Request classification

`request_classification` classifies the request before any heavy retrieval or workflow.

Classification dimensions:

```text
primary_domain
secondary_domains
question_type
risk_level
context_dependency
freshness_required
evidence_required
approval_hint
recommended_mode
```

Common question types:

```text
technical
regulatory
legal_contractual
financial
organizational
editorial
client_relation
project_memory
system_memory
urbanism
erp_fire_safety
accessibility
market_documents
software
infra
image_visual_communication
```

Example:

```yaml
request_classification:
  original_request: "Combien d’UP il me faut ?"
  primary_domain: architecture_fr
  question_type: technical_regulatory
  topic_family:
    - ERP
    - sécurité incendie
    - dégagements
  risk_level: medium_to_high
  context_dependency: high
  freshness_required: true
  evidence_required: true
  recommended_mode: answer_with_assumptions_or_request_missing_inputs
```

---

## 5. Intent enrichment

`request_intent_enrichment` interprets what the user is really asking.

It must identify:

```text
probable meaning
implicit assumptions
missing data
answer shape expected by the user
agents and skills likely required
```

Example:

```yaml
request_intent_enrichment:
  original_request: "Combien d’UP il me faut ?"
  interpreted_intent: "Estimate required ERP evacuation units of passage."
  implicit_needs:
    - type_erp
    - activity
    - occupancy_public
    - occupancy_staff
    - level
    - exits
    - available_widths
  likely_answer_shape:
    - assumptions
    - provisional calculation
    - minimum width
    - limitations
    - documents_to_verify
```

---

## 6. Context expansion

`context_scope_expansion` decides whether more context is needed.

It decides whether to check:

```text
current conversation
uploaded documents
project memory
system memory
OpenWebUI Knowledge
external official sources
web sources
similar cases
```

It must not search everywhere by default.

It must select the smallest useful expansion.

Output:

```yaml
context_scope_expansion:
  context_needed: true
  known_context: []
  missing_context:
    blocking: []
    useful_but_not_blocking: []
  sources_to_check:
    session_context: true
    uploaded_documents: true
    project_memory: false
    system_memory: false
    openwebui_knowledge: []
    web:
      required: false
      purpose: []
  recommended_agents: []
  response_mode: answer_with_assumptions
```

---

## 7. Variant generation

`variant_generation` is used when several acceptable responses or strategies may exist.

Typical triggers:

```text
user requests variants
client-facing wording
sensitive answer
design choice
workflow strategy
technical option comparison
uncertain brief
```

Default variant counts:

```text
3 variants = normal
5 variants = explicit request or creative/design scenario
```

PROMETHEUS is the primary role.

IRIS may formulate variants.

THEMIS and APOLLO review variants when risk or brief adherence matters.

---

## 8. Agent revision request

`agent_revision_request` allows one role to ask another role to revise an output.

Example:

```yaml
agent_revision_request:
  requested_by: APOLLO
  target_role: IRIS
  target_output: draft_response
  reason: "The draft does not stay close enough to the initial request."
  requested_change:
    - "Reduce digressions."
    - "Make limitations more visible."
  approval_impact: none
  memory_impact: none
```

Rules:

```text
revision request is bounded
revision request does not mutate canonical files
revision request does not bypass approvals
revision request must describe what to change and why
```

---

## 9. AGORA consultation mode

AGORA is a structured forum of roles.

It is not an agent.

It is activated when:

```text
several variants exist
roles disagree
risk and usefulness conflict
brief adherence is uncertain
workflow path is disputed
user requested alternatives
```

AGORA must produce short role opinions, not raw reasoning.

Example:

```yaml
agent_forum_review:
  purpose: "Compare 3 response variants."
  participants:
    - ATHENA
    - THEMIS
    - APOLLO
    - IRIS
    - ZEUS
  max_rounds: 1
  opinions:
    - role: THEMIS
      preferred_variant: option_A
      reason: "Lowest responsibility risk."
    - role: IRIS
      preferred_variant: option_B
      reason: "Clearest for the user."
  decision:
    role: ZEUS
    selected_variant: option_B
    modifications:
      - "Add THEMIS reserve."
```

Forbidden:

```text
open-ended debate
raw chain-of-thought
majority vote overriding safety
automatic approval
automatic memory promotion
automatic workflow canonization
```

---

## 10. Decision arbitration

`decision_arbitration` supports ZEUS when variants or role opinions conflict.

Priority criteria:

```text
1. safety / responsibility / compliance
2. adherence to initial request
3. evidence and available sources
4. operational usefulness
5. clarity for the user
6. simplicity
7. style or elegance
```

ZEUS may:

```text
select one variant
combine variants
reject all variants
request a safer variant
request a clearer variant
ask the user to choose
pause for missing information
```

ZEUS must not bypass THEMIS, APOLLO or human approval.

---

## 11. Brief adherence review

`brief_adherence_review` verifies that a response or deliverable remains aligned with the initial request.

APOLLO is primary.

METIS, ATHENA, IRIS and THEMIS may contribute.

Checks:

```text
matches initial request
keeps expected format
keeps expected audience
does not drift outside scope
has consistent parts
keeps assumptions visible
keeps limitations visible
does not contradict known context
does not overstate certainty
```

Output:

```yaml
brief_adherence_review:
  initial_request: null
  expected_deliverable: null
  required_points: []
  missing_points: []
  scope_drift: []
  coherence_issues: []
  recommended_revision: []
```

---

## 12. Example — ERP UP question

User request:

```text
Combien d’UP il me faut ?
```

Correct orchestration:

```text
METIS → classify as technical/regulatory ERP question
METIS → enrich intent: units of passage for evacuation
HECATE → expose ambiguities: ERP type, occupancy, level, exits, widths
ARGOS → inspect available context and documents
context_scope_expansion → decide if project memory, Knowledge or web sources are needed
DEMETER → estimate quantities/effectifs when data exists
POSEIDON → check levels, site, exits and physical flow
THEMIS → prevent unsupported regulatory conclusion
APOLLO → validate limits and proof
IRIS → write clear answer
```

The answer may be provisional if data is missing.

It must distinguish:

```text
known context
assumptions
missing data
provisional calculation
verification needed
```

---

## 13. Final rule

```text
Understand before answering.
Classify before searching.
Expand context only when useful.
Generate variants only when they help.
Consult AGORA only when comparison or disagreement matters.
Let ZEUS arbitrate, but never bypass THEMIS, APOLLO or human approval.
```
