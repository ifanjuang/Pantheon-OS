# Skill — agent_forum_review

Status: candidate.

Domain: general.

Purpose: collect short structured opinions from selected Pantheon roles when variants, risk trade-offs or disagreements need comparison.

---

## 1. Role

`agent_forum_review` supports AGORA consultation mode.

AGORA is not an agent.

AGORA is a bounded consultation format.

It must remain short, structured and review-oriented.

---

## 2. Inputs

```text
purpose
candidate_variants
participants
selection_criteria
risk_flags optional
brief_adherence_context optional
```

---

## 3. Outputs

```yaml
agent_forum_review:
  purpose: "Compare response variants."
  participants:
    - ATHENA
    - THEMIS
    - APOLLO
    - IRIS
  max_rounds: 1
  opinions:
    - role: THEMIS
      preferred_variant: option_A
      reason: "Lowest responsibility risk."
    - role: IRIS
      preferred_variant: option_B
      reason: "Clearest for the user."
  unresolved_disagreement: true
  recommended_next_step: decision_arbitration
```

---

## 4. Rules

```text
short opinions only
one round by default
participants must be selected for a reason
THEMIS and APOLLO concerns must remain visible
ZEUS arbitrates when no consensus is safe or obvious
```

---

## 5. Guardrails

AGORA must not become an open-ended debate, a vote-based authority, or a hidden runtime loop.

---

## 6. Final rule

```text
AGORA compares. ZEUS arbitrates. THEMIS and APOLLO remain gates.
```
