# Skill — variant_generation

Status: candidate.

Domain: general.

Purpose: produce a bounded set of candidate variants when several valid answers, strategies, plans or formulations may exist.

---

## 1. Role

`variant_generation` is normally led by PROMETHEUS.

It may be used for:

```text
answer strategies
client-facing wording
technical options
workflow options
plans
article structures
design or communication alternatives
```

It produces candidate variants only.

---

## 2. Inputs

```text
initial_request
interpreted_intent
constraints
variant_count
selection_criteria
risk_flags optional
```

---

## 3. Outputs

```yaml
variant_set:
  requested_by: ATHENA
  generated_by: PROMETHEUS
  count: 3
  purpose: "Compare possible response strategies."
  variants:
    - id: option_A
      title: "Prudent option"
      strengths: []
      weaknesses: []
```

---

## 4. Rules

Default count:

```text
3 variants = normal
5 variants = explicit request or creative case
```

Each variant must include:

```text
id
title
purpose
strengths
weaknesses
risk notes when relevant
```

---

## 5. Guardrails

Variants must be meaningfully different.

They must not be cosmetic synonyms, unbounded options, or unsafe options without warning.

---

## 6. Final rule

```text
Generate variants only when comparison improves the answer.
```
