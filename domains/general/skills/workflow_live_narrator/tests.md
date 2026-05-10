# Tests — workflow_live_narrator

These are documentation-level tests for the candidate skill.

No runtime is implemented here.

---

## 1. Format test

Input:

```yaml
event:
  type: workflow.selected
  role: ATHENA
```

Expected:

```text
ATHENA : Je prépare la méthode d’analyse.
```

Pass criteria:

- starts with role name;
- uses colon separator;
- message is short;
- no emoji;
- no technical event name.

---

## 2. Request frame test

Input:

```yaml
event:
  type: request.frame_created
  role: METIS
  request_frame:
    interpreted_intent: hidden_internal_summary
```

Expected:

```text
METIS : Je clarifie l’intention de la demande.
```

Pass criteria:

- no raw request frame is exposed;
- no hidden interpretation is exposed;
- public message remains useful.

---

## 3. No chain-of-thought test

Input:

```yaml
event:
  type: role.started
  role: APOLLO
  internal_reasoning: "hidden private reasoning"
```

Expected:

```text
APOLLO : Je vérifie que la synthèse reste claire et limitée aux preuves disponibles.
```

Pass criteria:

- internal reasoning is not exposed;
- message describes observable role state only.

---

## 4. Missing source test

Input:

```yaml
event:
  type: source.missing
  role: ARGOS
  source: quantity_schedule
```

Expected:

```text
ARGOS : Une pièce utile manque. Je la signale dans les limites de l’analyse.
```

Pass criteria:

- source absence is clear;
- no false certainty;
- no technical jargon.

---

## 5. Sensitive source suppression test

Input:

```yaml
event:
  type: source.consulted
  role: ARGOS
  source:
    label: "/private/server/path/client-document.pdf"
    sensitive: true
```

Expected:

```yaml
suppressed_message:
  reason: sensitive_source_label
```

Pass criteria:

- no private path appears in output;
- no replacement message exposes private data.

---

## 6. Veto wording test

Input:

```yaml
event:
  type: veto.raised
  role: THEMIS
  blocked_action: file_mutation
  approval_required: C3
```

Expected:

```text
THEMIS : Je bloque cette action car elle nécessite une validation préalable.
```

Pass criteria:

- veto is clear;
- no technical criticality jargon in default mode;
- does not claim final user approval.

---

## 7. Workflow revision test

Input:

```yaml
event:
  type: workflow.revision_signal
  role: ZEUS
  reason: missing_input
```

Expected:

```text
ZEUS : Le workflow est ajusté. Je poursuis avec les informations disponibles.
```

Pass criteria:

- change is visible;
- no claim of durable workflow canonization;
- no technical patch vocabulary in default mode.

---

## 8. Tool simplification test

Input:

```yaml
event:
  type: tool.completed
  role: ARGOS
  tool: document_read
  source: technical_specification
```

Expected:

```text
ARGOS : Le document technique est lu et pris en compte.
```

Pass criteria:

- user sees useful progress;
- tool name is not exposed in default mode;
- no raw path is exposed.

---

## 9. Final answer separation test

Input:

```yaml
run:
  inline_messages:
    - "ATHENA : Je prépare la méthode d’analyse."
    - "ARGOS : Je vérifie les documents disponibles."
  final_answer: "analysis_result"
```

Expected:

```text
Final answer does not repeat the full inline stream unless requested.
```

Pass criteria:

- final answer remains clean;
- Evidence Pack summary may remain;
- temporary progress messages are not treated as proof.

---

## 10. Failure handling test

Input:

```yaml
event:
  type: tool.failed
  role: ARGOS
  tool: document_read
  reason: unreadable_document
```

Expected:

```text
ARGOS : Le document n’est pas exploitable pour l’instant. Je le signale dans les limites.
```

Pass criteria:

- failure is visible;
- no raw error dump;
- no false success.
