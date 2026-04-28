# Adaptive Orchestration — Updates

> Candidate updates for the `adaptive_orchestration` skill.

---

# 1. Current status

```yaml
state: candidate
level: 0
validated_xp: 0
pending_xp: 0
```

This skill is not active yet.

---

# 2. Candidate improvements

No candidate improvements yet.

---

# 3. Review checklist before activation

Before activation, review must confirm:

- `SKILL.md` is aligned with `hermes/skill_policy.md`;
- `manifest.yaml` contains lifecycle and XP metadata;
- examples are fictional and privacy-safe;
- tests cover preflight, runtime adaptation, context expansion, user fallback and no chain-of-thought exposure;
- no action can create active workflows automatically;
- no action can promote memory automatically;
- no action can level-up a skill automatically;
- risky or durable adaptations require approval.

---

# 4. Future update candidates

Possible future improvements:

- add `workflow_preflight_report` template;
- add `runtime_adaptation_report` template;
- add `agent_status_report` template;
- add `workflow_adaptation_report` template;
- connect to `skill_health_check` once that skill exists;
- connect to `memory_candidate_review` once that skill exists.
