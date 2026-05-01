# Example — Pantheon Repository Audit

Use this example when the user asks Hermes to audit the Pantheon OS repository.

---

# User request

```text
Audit the Pantheon OS repository and check documentation/code consistency.
```

---

# Required sequence

1. Read recent entries in `ai_logs/` (start with `ai_logs/README.md` for the rules).
2. Read `docs/governance/STATUS.md`.
3. Read the relevant reference Markdown files under `docs/governance/`.
4. Read code only after the reference Markdown files.
5. Produce an Evidence Pack.
6. Propose documentation updates before code changes when documentation is unclear.
7. Work only on a dedicated branch.
8. Never push to `main`.
9. Add an `ai_logs/YYYY-MM-DD-slug.md` entry after intervention.

---

# Expected output

```markdown
# Pantheon OS Repository Audit

## Summary

## Documentation/code consistency

## Inconsistencies detected

## Documentation updates proposed

## Code updates proposed

## Evidence Pack

## Tests

## Risks and limits

## Next action
```
