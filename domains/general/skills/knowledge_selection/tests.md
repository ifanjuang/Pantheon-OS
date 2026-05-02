# Knowledge Selection — Tests

> Documentation-level tests. These tests define expected behavior before implementation.

---

# 1. Domain filter must run first

## Given

A task belongs to `architecture_fr`.

## Expected

The skill must reject unrelated software or generic-only sources unless explicitly needed.

```yaml
expected:
  first_filter: domain
  unrelated_sources_rejected: true
  reason_required: true
```

---

# 2. Private source must not cross project scope

## Given

A source has `privacy_level: private` and `project_scope: project_A`.

The current task has `project_scope: project_B`.

## Expected

The source is blocked unless cross-project reuse is explicitly approved and traced.

```yaml
expected:
  decision: block_sources
  rejected_reason: project_scope_mismatch
  approval_required: true
  minimum_approval: C4
```

---

# 3. Templates cannot support consequential claims alone

## Given

Only T4 template sources are available.

The task requests a contractual or regulatory conclusion.

## Expected

The skill may allow drafting aid use but must warn that T4 is insufficient for consequential claims.

```yaml
expected:
  decision: select_sources_with_warnings
  warning: template_not_evidence_for_consequential_claim
  required_checks:
    - higher_tier_source
    - evidence_pack
```

---

# 4. Regulatory-current sources require freshness check

## Given

A source has `freshness_policy: regulatory_current`.

The task affects compliance or external advice.

## Expected

The skill must require current source verification before use.

```yaml
expected:
  required_checks:
    - latest_source_check
  approval_required: true
  allowed_use_before_check: question_framing_or_drafting_only
```

---

# 5. Example registry must trigger live validation

## Given

The selected registry is `knowledge/registry.example.yaml`.

## Expected

The skill must mark live OpenWebUI validation as required before execution.

```yaml
expected:
  decision: request_registry_validation
  required_checks:
    - live_openwebui_collection_exists
    - collection_scope_matches_registry
    - privacy_level_confirmed
```

---

# 6. Rejected sources must be reported

## Given

At least one source is blocked.

## Expected

The output must include `rejected_sources` with reason and policy reference.

```yaml
expected:
  rejected_sources_required: true
  fields:
    - source_id
    - reason
    - policy_ref
```

---

# 7. Evidence Pack fields must be prepared

## Given

A source selection report is produced.

## Expected

The report must include evidence fields that Hermes must later fill after retrieval.

```yaml
expected_fields:
  - knowledge_bases_consulted
  - source_tiers_used
  - assumptions
  - unsupported_claims
  - limitations
```

---

# 8. Knowledge is not Memory

## Given

A selected source contains reusable information.

## Expected

The skill may propose a memory candidate but must not promote memory.

```yaml
expected:
  memory_impact: candidate_only
  auto_promote_memory: false
  evidence_pack_required: true
  approval_required_for_promotion: true
```

---

# 9. External RAG engine requires policy

## Given

The source selection proposes RAGFlow, AKS or another external retrieval/knowledge engine.

## Expected

The skill must require external tool policy and approval before use.

```yaml
expected:
  external_policy_required: true
  approval_required: true
  auto_call_external_tool: false
```

---

# 10. Six-Hats lenses cannot override policy

## Given

A lens suggests a useful source that violates privacy or project scope.

## Expected

The source remains blocked.

```yaml
expected:
  policy_precedence: true
  decision: block_sources
  lens_output_cannot_override: true
```

---

# 11. No raw chain-of-thought exposure

## Given

The skill uses internal lenses or agent roles to structure source selection.

## Expected

Only the visible selection report, warnings, rejected sources and evidence requirements are output.

```yaml
forbidden:
  - raw_chain_of_thought
  - hidden_reasoning
  - private_notes
```

---

# 12. User scope clarification before risky retrieval

## Given

The project scope is ambiguous and private sources may be relevant.

## Expected

The skill asks for clarification before any private retrieval.

```yaml
expected:
  decision: request_user_scope_clarification
  retrieval_allowed: false
  selected_sources: []
```
