# Skill — deliverable_contract_builder

Status: candidate.

Domain: general.

Purpose: transform a user request for a complete deliverable into a bounded Deliverable Contract before production starts.

---

## 1. Role in Pantheon

`deliverable_contract_builder` supports the Deliverable Operating Model.

It helps create:

```text
Request Brief
Deliverable Contract
Production Plan outline
Milestone Gates
Section Gates
Definition of Done
Stop Gate requirements
```

It does not produce the complete deliverable by itself.

It does not execute tools.

It does not activate Hermes.

It does not approve external use.

---

## 2. Use when

Use this skill when the user asks for:

```text
rapport complet
dossier complet
audit complet
CCTP complet
article long
documentation package
mémoire technique
presentation pack
long improvement session
Night Run
```

Use it when wrong framing would cause high revision cost.

Use it when the deliverable requires several sections, sources, assets, gates or approvals.

---

## 3. Do not use when

Do not use this skill for:

```text
simple answer
short rewrite
simple email
translation
minor correction
single factual question
small table
small calculation
```

If the user explicitly asks for a quick answer, respond directly and state assumptions.

---

## 4. Inputs

Expected input:

```yaml
request_input:
  original_request: null
  available_context: []
  known_domain: general | architecture_fr | software | mixed | unknown
  intended_external_use: false
  known_deadline: null
  known_format: null
  known_sources: []
```

---

## 5. Outputs

Expected output:

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
  target_reader: null
  expected_depth: standard | complete | expert
  external_use: false
  risk_level: C0 | C1 | C2 | C3 | C4 | C5
  source_need: none | light | required | critical
  required_sections: []
  required_assets: []
  milestones: []
  definition_of_done: []
  stop_gate_required: true
  evidence_pack_required: true | false
  task_contract_required: true | false
  unresolved_questions: []
  assumptions_if_no_answer: []
```

Optional output:

```yaml
production_plan_outline:
  mode: direct | stepwise | extended_refinement
  stages: []
  escalation_conditions: []
```

---

## 6. Question policy

The skill may use `rich_elicitation` when critical framing information is missing.

Ask only blocking questions.

Ask no more than three questions in the first pass.

If the user asks not to be interrupted, proceed with explicit assumptions.

Do not ask cosmetic questions before structural questions.

---

## 7. Required decisions

The skill should decide or propose:

```text
deliverable type
domain
reader
scope
source need
risk level
production mode
required sections
milestone gates
section gates
asset need
evidence requirement
approval requirement
stop gate requirement
```

---

## 8. Evidence relationship

Evidence Pack is required when the deliverable is:

```text
source-dependent
external-facing
contractual
financial
legal-sensitive
high-confidence
persistent
based on web or Knowledge sources
```

For lower-risk internal drafts, Evidence Pack may be light but limitations must be explicit.

---

## 9. Approval relationship

Default mapping:

```text
internal draft = C1
internal persistent document = C3
external-facing package = C4
contractual / financial / legal-sensitive package = C4
secret, destructive or irreversible action = C5
```

THEMIS may escalate.

APOLLO may block finalization.

ZEUS may reroute.

---

## 10. Role mapping

```text
METIS frames the request.
HERA owns trajectory.
ATHENA arranges method.
ARGOS owns sources.
HECATE exposes uncertainty.
THEMIS owns approval and risk.
APOLLO owns stop gate.
ZEUS arbitrates.
IRIS drafts wording.
DAEDALUS structures diagrams.
DEMETER reviews quantities and tables.
CHRONOS handles sequence and freshness.
HEPHAESTUS reviews robustness.
```

---

## 11. Forbidden actions

The skill must not:

```text
produce the final deliverable without contract acceptance when risk is high
execute tools
mutate files
send externally
promote memory
activate skill
canonize workflow
hide assumptions
claim evidence without sources
start unbounded refinement
```

---

## 12. Hermes mapping

This is a candidate Pantheon skill.

Hermes execution is not active by default.

Future Hermes use would require:

```text
skill review
Task Contract
Evidence Pack rules
approval classification
sandbox test
```

---

## 13. Final rule

```text
Frame before producing.
Contract before complete deliverable.
Evidence before authority.
Stop Gate before finalization.
```
