# Changelog

Toutes les évolutions notables de Pantheon OS doivent être consignées ici.

Le projet suit SemVer : `MAJOR.MINOR.PATCH`.

---

## [Unreleased]

### Fixed

- Migration Alembic `20260426_0001_add_approval_requests` reconnectée à `down_revision = "0028"` (résout le known issue de tête détachée).
- `platform/infra/docker/api/Dockerfile` : remplace le `COPY modules/` (chemin inexistant) par `COPY agents/ skills/ tools/ workflows/` — déblocage du build image API.

### Added

- Section `[project]` dans `pyproject.toml` (PEP 621) avec dépendances explicites — la source de vérité runtime reste `platform/api/requirements.txt`.
- `docs/governance/` : 14 documents de gouvernance déplacés depuis la racine (AGENTS, APPROVALS, ARCHITECTURE, EVIDENCE_PACK, EXTERNAL_TOOLS_POLICY, EXTERNAL_WATCHLIST, HERMES_INTEGRATION, KNOWLEDGE_TAXONOMY, MEMORY, MODULES, ROADMAP, STATUS, TASK_CONTRACTS, VERSIONS) + `docs/governance/README.md`.
- `ai_logs/README.md` : hub canonique du journal IA (règles, fichiers critiques, conventions branches, template d'entrée).
- `ai_logs/0000-historical-archive.md` : entrées historiques de l'ancien `AI_LOG.md` préservées.

### Removed

- `docs/governance/AI_LOG.md` (déplacé/scindé) : règles + template → `ai_logs/README.md`, entrées historiques → `ai_logs/0000-historical-archive.md`. Convention unifiée : un fichier par session sous `ai_logs/YYYY-MM-DD-slug.md`.

### Changed

- `config/domains.yaml` réduit au scope MVP : conserve `architecture_fr` (actif) et ajoute `general` comme socle. Les overlays aspirationnels `legal_fr` / `medical_fr` sont retirés (à recréer en V2 quand les dossiers existeront).
- `config/policies.yaml` retire les `trusted_sources` `legal_fr` / `medical_fr` ; commentaire scope MVP-only.
- `platform/api/pantheon_runtime/router.py` : retire la référence orpheline `domains/software` du context-pack ; `truth_files` mis à jour vers `docs/governance/*.md`.
- `domains/general/skills/{adaptive_orchestration,project_context_resolution}/manifest.yaml` : `required_documents` mis à jour vers `docs/governance/*.md`.
- `pyproject.toml` exclut désormais `legacy/` au lieu de `benchmarks/` (Ruff).
- `CLAUDE.md` aligné sur la structure réelle : pas de wrapper `modules/`, 24 agents, domaines `architecture_fr` + `general`, 27 apps FastAPI, 6 fichiers de config, table Alembic à jour, mention de `docs/governance/`.

### Removed (modules)

- `modules.yaml` : entrées `control` et `monitoring` retirées (apps archivées).

### Archived (legacy/)

- `platform/api/apps/control/` : stub sans tests, sans migration, sans modèle.
- `platform/api/apps/monitoring/` : stub sans tests, sans migration, sans modèle.
- `benchmarks/` (ClawMark runner) : exclu du linting, plus appelé par la CI.
- `INSTALL.md` : supplanté par `scripts/install/ui/`.
- Convention : `legacy/` n'est jamais importé par le runtime (voir `legacy/README.md`).

---

## 0.5.0-alpha.1 — 2026-04-26

### Added

- Audit initial documentation / code dans `CODE_AUDIT.md`.
- `ManifestLoader` runtime tolérant pour agents, skills et workflows.
- Contrat manifest progressif `ComponentManifest`.
- Contrats `TaskDefinition` et `WorkflowDefinition`.
- Loader `workflow.yaml` / `tasks.yaml`.
- Workflow réel `document_analysis`.
- Endpoint debug `/debug/runtime-registry`.
- Module Approval Gate minimal, désactivé par défaut.
- Migration `approval_requests`.
- Installer UI autonome pour NAS + Ollama LAN.
- Script Windows pour préparer Ollama.
- `VERSION`, `CHANGELOG.md`, `VERSIONS.md`, `EXTERNAL_WATCHLIST.md`.

### Changed

- `platform/api/main.py` charge désormais les registries runtime et les workflow definitions au startup.
- `ModuleRegistry` normalise les manifests API via le contrat commun.
- `STATUS.md` distingue plus précisément les états : livré, partiel, désactivé, à vérifier.

### Known issues

- La migration Approval Gate contient `down_revision = None` et doit être vérifiée localement avec `alembic heads`.
- Le module `approvals` reste désactivé tant que migration et tests ne sont pas validés.
- L’Installer UI est ajoutée mais non testée sur NAS dans cette session.
- Les workflows sont chargés et exposés, mais pas encore connectés à un moteur d’exécution.
- Les traces `task_run` et `approval_event` ne sont pas encore implémentées.
