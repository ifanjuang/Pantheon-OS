# Examples — deliverable_contract_builder

All examples are fictional and generic.

---

## 1. Complete report

User request:

```text
Fais-moi un rapport complet sur ce sujet.
```

Expected output:

```yaml
deliverable_contract:
  type: report
  owner_role: HERA
  method_owner: ATHENA
  final_gate_owner: APOLLO
  risk_owner: THEMIS
  source_owner: ARGOS
  expected_depth: complete
  source_need: required
  required_sections:
    - executive_summary
    - context
    - sources_and_method
    - analysis
    - risks_and_limits
    - recommendations
    - conclusion
  milestones:
    - request_brief
    - source_inventory
    - outline
    - draft_sections
    - global_review
    - stop_gate
  definition_of_done:
    - required_sections_present
    - source_limits_visible
    - unsupported_claims_removed
    - stop_gate_passed
  evidence_pack_required: true
  unresolved_questions:
    - target_reader
    - source_scope
```

---

## 2. Complete CCTP

User request:

```text
Rédige un CCTP complet.
```

Expected output:

```yaml
deliverable_contract:
  type: cctp
  domain: architecture_fr
  expected_depth: expert
  risk_level: C4
  source_need: critical
  external_use: true
  required_sections:
    - general_requirements
    - lot_structure
    - technical_requirements_by_lot
    - execution_constraints
    - tests_and_acceptance
    - limits_and_exclusions
  milestones:
    - source_inventory
    - lot_structure_validation
    - lot_by_lot_drafting
    - duplication_check
    - risk_review
    - stop_gate
  evidence_pack_required: true
  task_contract_required: true
  unresolved_questions:
    - project_documents_available
    - market_type
    - lot_structure
    - diagnostics_available
```

Action:

```text
Do not draft the full CCTP immediately if sources and lot structure are missing.
Build contract first or ask blocking questions.
```

---

## 3. Long article

User request:

```text
Écris un article long sur ce thème.
```

Expected output:

```yaml
deliverable_contract:
  type: article
  expected_depth: complete
  source_need: light
  required_sections:
    - angle
    - introduction
    - development_sections
    - examples
    - conclusion
  milestones:
    - intention
    - research_or_context
    - outline
    - first_draft
    - style_review
    - final_review
  definition_of_done:
    - angle_clear
    - audience_matched
    - no_repetition
    - final_style_reviewed
```

---

## 4. Night Run

User request:

```text
J’ai une nuit devant moi, améliore jusqu’à ce que je dise stop.
```

Expected output:

```yaml
extended_refinement_run:
  mode: night_run
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

Action:

```text
The run must be bounded. It cannot be an unbounded Pantheon runtime loop.
```

---

## 5. Simple email — no trigger

User request:

```text
Améliore ce mail.
```

Expected action:

```text
Do not create a Deliverable Contract.
Rewrite directly unless risk or ambiguity is material.
```
