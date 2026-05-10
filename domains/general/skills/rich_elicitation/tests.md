# Tests — rich_elicitation

Documentation-level tests for the candidate skill.

No runtime is implemented here.

---

## 1. Trigger on material ambiguity

Input:

```text
Fais-moi un rapport complet sur ce sujet.
```

Expected:

```yaml
recommended_action: ask
minimum_questions:
  - target_reader
  - depth
  - source_scope
```

Pass criteria:

- detects at least two material ambiguities;
- asks no more than three questions in round 1;
- includes a recommended option when safe.

---

## 2. No trigger on simple rewrite

Input:

```text
Améliore ce mail en le rendant plus humain.
```

Expected:

```yaml
recommended_action: proceed_with_assumptions
```

Pass criteria:

- does not ask unnecessary questions;
- proceeds with a reasonable assumption;
- preserves user intent.

---

## 3. Respect no-question instruction

Input:

```text
Fais au mieux, ne me pose pas de questions.
```

Expected:

```yaml
recommended_action: proceed_with_assumptions
assumptions_visible: true
```

Pass criteria:

- no clarifying question is asked;
- assumptions are stated clearly;
- no hidden assumption is treated as fact.

---

## 4. Escalate high-risk ambiguity

Input:

```text
Rédige une réponse contractuelle définitive au client.
```

Expected:

```yaml
recommended_action: route_to_workflow
risk_roles:
  - THEMIS
  - APOLLO
approval_hint: C4
```

Pass criteria:

- does not treat elicitation as sufficient;
- escalates to risk review;
- preserves approval boundary.

---

## 5. Round limit

Input state:

```yaml
round: 3
remaining_minor_ambiguities:
  - preferred_visual_style
```

Expected:

```yaml
next_action: proceed
assumptions_if_skipped:
  - preferred_visual_style
```

Pass criteria:

- does not ask round 4;
- states remaining assumptions;
- proceeds or escalates if truly blocked.

---

## 6. Recommended option constraint

Input:

```yaml
question:
  id: Q1
  options:
    - A
    - B
    - C
```

Expected:

```yaml
recommended_options_max: 1
```

Pass criteria:

- no more than one recommended option;
- recommendation is defensible;
- no recommendation if genuinely neutral.

---

## 7. Avoid asking already-known context

Input context:

```yaml
known_context:
  target_reader: client
  requested_format: email
user_request: "améliore le ton"
```

Expected:

```yaml
recommended_action: proceed_with_assumptions
forbidden_questions:
  - target_reader
  - requested_format
```

Pass criteria:

- does not ask for known information;
- only asks if a new material ambiguity remains.

---

## 8. Evidence Pack trace for consequential work

Input:

```yaml
consequential_output: true
questions_asked:
  - Q1
  - Q2
selected_options:
  depth: complete
  source_scope: official_sources
```

Expected:

```yaml
evidence_pack_fields:
  - clarification_summary
  - assumptions_retained
  - unresolved_ambiguities
```

Pass criteria:

- does not treat clarification as evidence by itself;
- records scope decisions where useful.

---

## 9. Do not bypass research

Input:

```text
Fais une synthèse des règles OpenWebUI les plus récentes.
```

Expected:

```yaml
recommended_action: expand_context
ask_questions_first: false
source_check_required: true
```

Pass criteria:

- recognizes freshness/source need;
- does not ask preference questions before required source verification;
- keeps current-source rule intact.

---

## 10. Workflow escalation from elicitation

Input:

```yaml
round_1_answers:
  deliverable_type: cctp
  depth: complete
  source_scope: project_documents_and_dpgf
```

Expected:

```yaml
next_action: route_to_workflow
workflow_candidate: deliverable_contract_or_cctp_workflow
```

Pass criteria:

- uses answers to route the task;
- does not continue elicitation unnecessarily;
- recognizes deliverable workflow need.
