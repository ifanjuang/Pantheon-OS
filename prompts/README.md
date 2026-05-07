# Pantheon Next — System Prompts Registry

This directory contains governed prompts used to align ChatGPT, Hermes Agent and OpenWebUI with the Pantheon Next doctrine.

These prompts are governance assets. They do not implement runtime behavior by themselves.

## Core doctrine

OpenWebUI exposes.  
Hermes Agent executes.  
Pantheon Next governs.

## Important Hermes loading distinction

Hermes uses different context layers.

- `SOUL.md` is the durable Hermes identity. It belongs to the Hermes home directory and should contain stable identity and global behavior.
- Project-specific instructions belong in `.hermes.md`, `HERMES.md`, `AGENTS.md` or equivalent project context files.
- Pantheon prompt files are source material. They must be copied, linked or exported into the right runtime layer before they affect Hermes.

Therefore:

- use `system/hermes_operator.md` as source material for Hermes identity or project context;
- do not assume this registry is consumed automatically;
- verify Hermes runtime loading with a real test before claiming activation.

## Prompt files

- `system/general.md` — default project assistant prompt.
- `system/pantheon_next_governance.md` — strict doctrine and architecture boundary prompt.
- `system/hermes_operator.md` — Hermes execution behavior under Task Contracts.
- `system/openwebui_cockpit.md` — OpenWebUI cockpit and Knowledge boundary.
- `system/architecture_fr.md` — French architecture and maîtrise d’œuvre domain prompt.
- `system/software_repo_audit.md` — repository and Markdown audit prompt.
- `system/client_communication.md` — client-facing communication prompt.
- `system/evidence_pack.md` — Evidence Pack prompt.
- `system/memory_governance.md` — memory candidate and canonical memory prompt.
- `system/prompt_router.md` — governed prompt selection policy.
- `system/manifest.yaml` — registry and routing metadata.

## Rules

Before any technical answer about Hermes Agent or OpenWebUI, verify the latest official documentation:

- Hermes Agent / Nous Research docs and wiki.
- OpenWebUI docs.
- Official GitHub pages if needed.

Before proposing repository changes, read:

1. `ai_logs/README.md`
2. `docs/governance/STATUS.md`
3. `README.md`
4. `CHANGELOG.md`
5. the relevant governance Markdown files.

Prompt routing must remain governed by Pantheon. Hermes may select prompts under policy, but must not invent or expand its own authority.

Any persistent change must follow the approval policy and be logged in `ai_logs/`.
