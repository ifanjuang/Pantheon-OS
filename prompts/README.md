# Pantheon Next — System Prompts Registry

This directory contains governed prompt fragments used to align ChatGPT, Hermes Agent and OpenWebUI with Pantheon Next doctrine.

These prompts are governance assets. They do not implement runtime behavior by themselves.

Core doctrine:

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

## Status

```text
status: candidate registry
runtime binding: not implemented
OpenWebUI import: not performed
Hermes activation: not performed
```

The registry is source material only until a separate approved integration maps prompts into a real runtime layer.

## Hermes loading distinction

Hermes and similar operator runtimes may use several context layers.

Pantheon prompt files must not be treated as automatically loaded.

Use these files as source material for:

```text
Hermes project context
OpenWebUI Workspace Model instructions
operator prompts
future context exports
```

Before claiming activation, verify the real runtime loading path and record it in an Evidence Pack.

## Prompt files

- `system/general.md` — default Pantheon Next assistant prompt.
- `system/pantheon_next_governance.md` — strict governance and architecture boundary prompt.
- `system/hermes_operator.md` — Hermes execution behavior under Task Contracts.
- `system/openwebui_cockpit.md` — OpenWebUI cockpit and Knowledge boundary.
- `system/request_orchestration.md` — METIS / AGORA request orchestration prompt.
- `system/architecture_fr.md` — French architecture and maîtrise d’œuvre domain prompt.
- `system/software_repo_audit.md` — repository and Markdown audit prompt.
- `system/client_communication.md` — client-facing communication prompt.
- `system/evidence_pack.md` — Evidence Pack prompt.
- `system/memory_governance.md` — memory candidate and canonical memory prompt.
- `system/prompt_router.md` — governed prompt selection policy.
- `system/manifest.yaml` — registry and routing metadata.

## Rules

Before any technical answer about Hermes Agent or OpenWebUI, verify the latest official documentation:

- Hermes Agent / Nous Research docs and wiki;
- OpenWebUI docs;
- official GitHub pages if needed.

Before proposing repository changes, read:

1. `ai_logs/README.md`
2. `docs/governance/STATUS.md`
3. `README.md`
4. `CHANGELOG.md`
5. relevant governance Markdown files.

Prompt routing must remain governed by Pantheon.

Hermes may select prompts under policy, but must not invent or expand its own authority.

Any persistent change must follow approval policy and be logged in `ai_logs/`.
