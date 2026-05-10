# Examples — workflow_live_narrator

All examples are fictional and generic.

The purpose is to define safe public-facing wording for Inline Run Stream V1.

---

## 1. Request framing

Input event:

```yaml
event:
  type: request.frame_created
  role: METIS
```

Output:

```text
METIS : Je clarifie l’intention de la demande.
```

---

## 2. Simple workflow start

Input event:

```yaml
event:
  type: workflow.selected
  role: ATHENA
  workflow_id: quote_vs_cctp_review
```

Output:

```text
ATHENA : Je prépare la méthode d’analyse.
```

---

## 3. Documents available

Input event:

```yaml
event:
  type: source.consulted
  role: ARGOS
  sources:
    - label: quote_document
    - label: technical_specification
```

Output:

```text
ARGOS : Le devis et le document technique sont pris en compte.
```

---

## 4. Missing document

Input event:

```yaml
event:
  type: source.missing
  role: ARGOS
  source: quantity_schedule
```

Output:

```text
ARGOS : Une pièce utile manque. Je la signale dans les limites de l’analyse.
```

---

## 5. Waiting for information

Input event:

```yaml
event:
  type: role.waiting
  role: DEMETER
  waiting_for_role: ARGOS
  requested_information: extracted_quantities
```

Output:

```text
DEMETER : J’attends les quantités extraites pour vérifier les écarts.
```

---

## 6. Information transmitted

Input event:

```yaml
event:
  type: information.transmitted
  from_role: ARGOS
  to_role: DEMETER
  payload_label: usable_quantities
```

Output:

```text
ARGOS : Les quantités exploitables sont transmises à DEMETER.
```

---

## 7. Warning

Input event:

```yaml
event:
  type: warning.raised
  role: THEMIS
  public_reason: missing_quantity_schedule
```

Output:

```text
THEMIS : Attention, la conclusion devra rester prudente car une pièce manque.
```

---

## 8. Veto

Input event:

```yaml
event:
  type: veto.raised
  role: THEMIS
  blocked_action: persistent_file_change
  approval_required: C3
```

Output:

```text
THEMIS : Je bloque cette action car elle nécessite une validation préalable.
```

---

## 9. AGORA summary

Input event:

```yaml
event:
  type: agora.completed
  role: ZEUS
  result: selected_safer_variant
```

Output:

```text
ZEUS : Les avis ont été comparés. Je retiens l’option la plus sûre.
```

---

## 10. Workflow adjustment

Input event:

```yaml
event:
  type: workflow.revision_signal
  role: ZEUS
  reason: missing_quantity_schedule
  change: mark_quantity_review_partial
```

Output:

```text
ZEUS : Le workflow est ajusté. Je poursuis avec les informations disponibles.
```

---

## 11. Technical source use simplified

Input event:

```yaml
event:
  type: tool.completed
  role: ARGOS
  tool: document_read
  source: technical_specification
```

Output:

```text
ARGOS : Le document technique est lu et pris en compte.
```

Forbidden output:

```text
ARGOS : document_read completed on /volume3/private/path/source.pdf.
```

---

## 12. Final quality check

Input event:

```yaml
event:
  type: role.completed
  role: APOLLO
  result: final_quality_check_ready
```

Output:

```text
APOLLO : Je vérifie que la synthèse reste claire et limitée aux preuves disponibles.
```

---

## 13. Message suppression

Input event:

```yaml
event:
  type: source.consulted
  role: ARGOS
  source:
    label: private_full_path
    sensitive: true
```

Output:

```yaml
suppressed_message:
  reason: sensitive_source_label
```

No user-visible message is produced.
