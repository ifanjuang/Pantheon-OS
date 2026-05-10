# DELIVERABLE OPERATING MODEL — Pantheon Next

> Governance model for complete deliverables such as reports, dossiers, audits, CCTP packages, long articles, documentation packages and extended refinement runs.
>
> A complete deliverable is not a single long answer.

---

## 1. Doctrine

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

The Deliverable Operating Model defines how Pantheon governs substantial outputs.

It must not become:

```text
runtime
scheduler
agent loop
message bus
workflow engine
content factory without validation
memory promotion engine
```

---

## 2. When to use

Use this model when the user asks for:

```text
rapport complet
dossier complet
audit complet
CCTP complet
article long
documentation package
mémoire technique
étude comparative structurée
livrable avec annexes
livrable avec tableaux, schémas ou assets
long improvement session / Night Run
```

Do not use it for:

```text
simple answer
simple rewrite
short email
translation
small calculation
single factual lookup
minor correction
```

---

## 3. Core principle

A complete deliverable should move through governed stages:

```text
Request Brief
→ Deliverable Contract
→ Production Plan
→ Task Cards
→ Milestone Gates
→ Section Gates
→ Global Review
→ APOLLO Stop Gate
→ Output Package
```

Rule:

```text
No premature final answer for complete deliverables.
```

---

## 4. Deliverable Contract

A Deliverable Contract defines the output before production.

```yaml
deliverable_contract:
  id: DC-YYYY-NNNN
  title: null
  type: report | dossier | audit | article | cctp | documentation | technical_note | presentation_pack
  domain: general | architecture_fr | software | mixed
  owner_role: HERA
  method_owner: ATHENA
  final_gate_owner: APOLLO
  risk_owner: THEMIS
  arbitration_owner: ZEUS
  source_owner: ARGOS
  wording_owner: IRIS
  structure_owner: DAEDALUS
  quantity_owner: DEMETER
  time_owner: CHRONOS
  target_reader: null
  expected_depth: short | standard | complete | expert
  external_use: false
  risk_level: C0 | C1 | C2 | C3 | C4 | C5
  source_need: none | light | required | critical
  required_sections: []
  optional_sections: []
  forbidden_sections: []
  required_assets: []
  milestones: []
  definition_of_done: []
  stop_gate_required: true
  evidence_pack_required: false
  task_contract_required: false
  memory_impact: none | candidate | possible_promotion
  file_impact: none | candidate_patch | persistent_change
```

A Deliverable Contract is a governance artifact.

It is not a runtime execution plan by itself.

---

## 5. Production Plan

The Production Plan breaks the deliverable into controlled stages.

```yaml
production_plan:
  deliverable_contract_id: DC-YYYY-NNNN
  mode: direct | stepwise | extended_refinement
  stages:
    - id: framing
      owner_role: METIS
      expected_output: request_brief
    - id: source_inventory
      owner_role: ARGOS
      expected_output: source_inventory
    - id: structure
      owner_role: ATHENA
      expected_output: outline
    - id: drafting
      owner_role: IRIS
      expected_output: draft_sections
    - id: review
      owner_role: APOLLO
      expected_output: stop_gate_signal
  escalation_conditions:
    - missing_required_source
    - themis_veto
    - scope_drift
    - unresolved_contradiction
```

Production plans may be executed by Hermes only if translated into an approved Task Contract.

---

## 6. Task Cards

Task Cards are bounded work units inside a deliverable.

```yaml
task_card:
  id: TC-YYYY-NNNN-01
  deliverable_contract_id: DC-YYYY-NNNN
  title: null
  owner_role: ARGOS
  objective: null
  inputs: []
  expected_output: null
  evidence_required: true
  approval_level: C1
  dependencies: []
  done_when: []
  blocked_by: []
```

Task Cards must not bypass Task Contracts when Hermes executes tools, edits files or performs consequential work.

---

## 7. Milestone Gates

Milestone Gates check whether progress is sufficient before continuing.

```yaml
milestone_gate:
  id: MG-YYYY-NNNN-01
  deliverable_contract_id: DC-YYYY-NNNN
  milestone: source_inventory
  owner_role: HERA
  status: not_started | in_progress | satisfactory | insufficient | blocked | needs_user_input | requires_route_change
  evidence_refs: []
  issues: []
  next_action: continue | revise | ask_user | escalate_to_zeus | block
```

HERA owns trajectory and milestone satisfaction.

HERA does not validate final truth.

---

## 8. Section Gates

Section Gates review individual parts of a deliverable.

```yaml
section_gate:
  id: SG-YYYY-NNNN-01
  section: null
  owner_role: APOLLO
  status: draft | acceptable | needs_revision | blocked
  checks:
    - matches_request
    - no_unsupported_claim
    - limitations_visible
    - no_duplicate_content
    - no_missing_required_part
  requested_revision: null
```

Section Gates prevent long deliverables from failing only at the end.

---

## 9. Global Review

Global Review checks the whole deliverable.

```yaml
global_review:
  owner_role: APOLLO
  checks:
    - brief_adherence
    - section_consistency
    - evidence_quality
    - limitation_visibility
    - contradiction_resolution
    - risk_alignment
    - asset_alignment
  result: ready | ready_with_limits | needs_revision | blocked
```

THEMIS may block finalization if risk, approval or external-use issues remain.

ZEUS may arbitrate if revision paths conflict.

---

## 10. APOLLO Stop Gate

APOLLO owns final readiness.

```yaml
stop_gate:
  owner_role: APOLLO
  deliverable_contract_id: DC-YYYY-NNNN
  can_finalize_if:
    - required_sections_present
    - section_gates_satisfactory
    - no_unresolved_major_contradiction
    - required_limitations_visible
    - evidence_status_acceptable
    - no_themis_veto
  must_continue_if:
    - missing_required_section
    - unresolved_contradiction
    - unsupported_claim
    - hidden_limitation
    - scope_drift
  decision: ready | ready_with_limits | needs_revision | needs_user_input | blocked
```

No complete deliverable should be finalized against an APOLLO block.

---

## 11. Output Package

The Output Package is what the user receives or validates.

```yaml
output_package:
  deliverable_contract_id: DC-YYYY-NNNN
  format: markdown | docx | pdf | slides | mixed
  sections: []
  annexes: []
  assets: []
  evidence_pack_ref: null
  limitations: []
  assumptions: []
  next_safe_action: null
```

External-facing packages require the relevant approval level.

---

## 12. Asset relationship

Complete deliverables may include assets only when useful.

Allowed asset types:

```text
diagram
table
chart
timeline
D3.js visualization
image reference
map
annex
bibliography
risk matrix
Evidence map
```

Rules:

```text
No chart without data source.
No decorative visual that implies evidence.
No external image reuse without rights check.
No D3.js without static fallback.
No asset without purpose.
No asset that bypasses Evidence Pack traceability.
```

Candidate asset schema:

```yaml
asset_contract:
  id: ASSET-YYYY-NNNN
  deliverable_contract_id: DC-YYYY-NNNN
  type: diagram | table | chart | d3_chart | image_reference | map | annex
  purpose: null
  owner_role: DAEDALUS | DEMETER | ARGOS | IRIS
  data_source: []
  evidence_required: true
  fallback: markdown_table | static_svg | text_summary
  rights_check_required: false
```

---

## 13. Extended Refinement / Night Run

A user may request that a response improve over a long period.

This is allowed only as a bounded mode.

```yaml
extended_refinement_run:
  mode: night_run
  deliverable_contract_id: DC-YYYY-NNNN
  objective: null
  max_revision_loops: 6
  checkpoint_policy: after_each_milestone
  stop_conditions:
    - user_stop
    - definition_of_done_reached
    - repeated_no_improvement
    - missing_required_input
    - approval_required
    - max_revision_loops_reached
  forbidden_actions:
    - external_send
    - memory_promotion
    - file_mutation_without_approval
    - destructive_tool
    - bypass_themis
    - bypass_apollo
```

Extended refinement may be executed by Hermes under Task Contract.

Pantheon does not become a long-running runtime.

---

## 14. Evidence relationship

Evidence Pack is required when the deliverable is consequential, source-dependent, contractual, external-facing or claims high confidence.

Evidence Pack may record:

```text
request_brief
deliverable_contract
production_plan
task_cards
milestone_gates
section_gates
global_review
stop_gate
role_signals
asset_contracts
source_inventory
assumptions
limitations
unsupported_claims
```

A complete deliverable without evidence must state its limits visibly.

---

## 15. Approval relationship

Default approval mapping:

| Case | Minimum level |
|---|---|
| Internal draft | C1 |
| Internal persistent document | C3 |
| External-facing package | C4 |
| Contractual / financial / legal-sensitive package | C4 |
| Secret, destructive or irreversible action | C5 |

THEMIS may escalate.

ZEUS may reroute.

APOLLO may block finalization.

---

## 16. Role split

```text
METIS frames the request.
HERA keeps trajectory and milestone satisfaction.
ATHENA arranges method and production plan.
ARGOS inventories sources and facts.
HECATE exposes ambiguity and hidden risk.
THEMIS owns risk and approval.
APOLLO owns final readiness.
ZEUS arbitrates route changes.
IRIS drafts and formats user-facing language.
DAEDALUS structures diagrams and system boundaries.
DEMETER reviews quantities, costs and tables.
CHRONOS handles sequence, dependencies and freshness.
HEPHAESTUS reviews method robustness and missing skills.
Hermes Agent executes only under Task Contract.
OpenWebUI exposes progress, review and validation.
```

---

## 17. Forbidden drift

The Deliverable Operating Model must not be used to justify:

```text
hidden autonomous loops
unbounded night runs
workflow execution inside Pantheon
automatic memory promotion
automatic file mutation
external send without approval
Evidence-free authoritative claims
chart/image authority without source
```

---

## 18. Final rule

```text
Small answers can be direct.
Complete deliverables require a contract.
Long refinement requires bounds.
Finalization requires a Stop Gate.
Consequential claims require evidence.
Hermes executes only under Task Contract.
Pantheon governs the deliverable.
```
