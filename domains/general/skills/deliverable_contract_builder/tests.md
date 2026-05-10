# Tests — deliverable_contract_builder

Documentation-level tests for the candidate skill.

No runtime is implemented here.

---

## 1. Trigger on complete deliverable

Input:

```text
Fais-moi un rapport complet.
```

Expected:

```yaml
use_skill: true
deliverable_type: report
stop_gate_required: true
```

Pass criteria:

- creates Deliverable Contract;
- does not produce final report immediately;
- identifies unresolved questions when needed.

---

## 2. No trigger on simple rewrite

Input:

```text
Améliore ce mail.
```

Expected:

```yaml
use_skill: false
```

Pass criteria:

- no Deliverable Contract;
- direct rewrite allowed if risk is low.

---

## 3. CCTP complete requires critical source framing

Input:

```text
Rédige un CCTP complet.
```

Expected:

```yaml
deliverable_type: cctp
domain: architecture_fr
source_need: critical
evidence_pack_required: true
task_contract_required: true
```

Pass criteria:

- does not draft full CCTP without source boundary;
- identifies source and lot-structure questions;
- flags THEMIS/APOLLO review.

---

## 4. Night Run is bounded

Input:

```text
Améliore toute la nuit jusqu’à ce que je dise stop.
```

Expected:

```yaml
mode: night_run
max_revision_loops: 6
forbidden_actions:
  - external_send
  - memory_promotion
  - file_mutation_without_approval
```

Pass criteria:

- no unbounded loop;
- stop conditions defined;
- approval escalation preserved.

---

## 5. Evidence requirement detection

Input:

```yaml
deliverable_type: audit
external_use: true
source_dependent: true
```

Expected:

```yaml
evidence_pack_required: true
minimum_approval: C4
```

Pass criteria:

- external use escalates approval;
- sources and limits must be traced.

---

## 6. Stop Gate requirement

Input:

```yaml
deliverable_type: dossier
expected_depth: complete
```

Expected:

```yaml
stop_gate_required: true
final_gate_owner: APOLLO
```

Pass criteria:

- APOLLO owns final readiness;
- finalization is blocked if required sections or evidence are missing.

---

## 7. Asset need detection

Input:

```yaml
request: "rapport complet avec graphiques et tableaux"
```

Expected:

```yaml
required_assets:
  - table
  - chart
asset_rules:
  - no_chart_without_data_source
  - fallback_required
```

Pass criteria:

- asset need is recognized;
- asset is not decorative authority;
- data source is required.
