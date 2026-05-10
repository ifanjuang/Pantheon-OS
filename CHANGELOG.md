# Changelog

Toutes les évolutions notables de Pantheon OS doivent être consignées ici.

Le projet suit SemVer : `MAJOR.MINOR.PATCH`.

---

## [Unreleased]

### Fixed

- Migration Alembic `20260426_0001_add_approval_requests` reconnectée à `down_revision = "0028"` (résout le known issue de tête détachée).
- `platform/infra/docker/api/Dockerfile` : remplace le `COPY modules/` (chemin inexistant) par `COPY agents/ skills/ tools/ workflows/` — déblocage du build image API.

### Added

- `docs/governance/EPISTEMIC_CONTROL_PROPAGATION.md` : carte d’adoption pour appliquer `EPISTEMIC_CONTROL.md` dans Evidence Packs, Task Contracts, Role Signals, Skill Lifecycle, Workflow Adaptation, STATUS et ROADMAP. Documentation uniquement, sans runtime ni enforcement automatique.
- `docs/governance/EPISTEMIC_CONTROL.md` : doctrine de contrôle des affirmations à l’échelle du claim, avec Claim Register, `epistemic_payload` pour Role Signals, `epistemic_contract` pour manifests de skills, `epistemic_requirements` pour Task Contracts et gates Source/Uncertainty/Risk/Final Claim. Documentation uniquement, sans runtime, sans agent supplémentaire et sans auto-canonisation.
- `docs/governance/REQUEST_ORCHESTRATION.md` : doctrine de cadrage des demandes par METIS, mode AGORA, variantes, demandes de révision, arbitrage ZEUS et adhérence au brief. Documentation uniquement, sans runtime ni boucle agentique.
- `domains/general/skills/{request_classification,request_intent_enrichment,context_scope_expansion,brief_adherence_review,agent_revision_request,variant_generation,agent_forum_review,decision_arbitration}/` : skill candidates de pré-cadrage, enrichissement de demande, extension contrôlée du contexte, cohérence du livrable, variantes, forum AGORA et arbitrage. Aucun skill actif, aucun binding Hermes, aucun outil ou endpoint ajouté.
- `docs/governance/DEVELOPMENT_PHASES.md` : lecture P0-P8 de la roadmap sans remplacer ni raccourcir `ROADMAP.md`.
- `docs/governance/HERMES_CAPABILITY_MAP.md` : cartographie opérationnelle des capacités entre Hermes, OpenWebUI, Pantheon et legacy.
- `docs/governance/GOVERNANCE_METHODS.md` : méthodes standard de classification, Task Contract, approvals, Evidence Packs et mémoire candidate.
- `docs/governance/MEMORY_STORAGE_MODEL.md` : modèle de stockage mémoire canonique, candidates, evidence, approvals, index Postgres et miroirs optionnels.
- `docs/governance/OPENWEBUI_PLUGIN_POLICY.md` : policy de sécurité pour Functions, Tools, Pipes, Filters, Actions et plugins OpenWebUI.
- Section `[project]` dans `pyproject.toml` (PEP 621) avec dépendances explicites — la source de vérité runtime reste `platform/api/requirements.txt`.
- `docs/governance/` : 14 documents de gouvernance déplacés depuis la racine (AGENTS, APPROVALS, ARCHITECTURE, EVIDENCE_PACK, EXTERNAL_TOOLS_POLICY, EXTERNAL_WATCHLIST, HERMES_INTEGRATION, KNOWLEDGE_TAXONOMY, MEMORY, MODULES, ROADMAP, STATUS, TASK_CONTRACTS, VERSIONS) + `docs/governance/README.md`.
- `ai_logs/README.md` : hub canonique du journal IA (règles, fichiers critiques, conventions branches, template d'entrée).
- `ai_logs/0000-historical-archive.md` : entrées historiques de l'ancien `AI_LOG.md` préservées.

### Removed

- `docs/governance/AI_LOG.md` (déplacé/scindé) : règles + template → `ai_logs/README.md`, entrées historiques → `ai_logs/0000-historical-archive.md`. Convention unifiée : un fichier par session sous `ai_logs/YYYY-MM-DD-slug.md`.

### Changed

- `docs/governance/EVIDENCE_PACK.md` : ajout du Claim Register, de l’epistemic summary et des règles empêchant l’augmentation de certitude sans nouvelle preuve dans les Evidence Packs.
- `docs/governance/SKILL_LIFECYCLE.md` : ajout d’un bloc `epistemic_contract` pour les manifests de skills, avec types de claims autorisés, preuves minimales, claims interdits et triggers d’escalade.
- `docs/governance/README.md` indexe désormais `EPISTEMIC_CONTROL_PROPAGATION.md` comme carte d’adoption de la doctrine épistémique.
- `docs/governance/README.md` indexe désormais `EPISTEMIC_CONTROL.md` comme document de gouvernance dédié au contrôle claim-level, à l’incertitude, aux payloads épistémiques et aux contrats épistémiques de skills.
- `docs/governance/AGENTS.md` : METIS devient le rôle de cadrage initial des demandes ; AGORA est défini comme mode de consultation borné et non comme agent autonome ; APOLLO reçoit explicitement l’adhérence au brief ; ZEUS arbitre les variantes et désaccords sans contourner THEMIS, APOLLO ou les approvals humains.
- `docs/governance/README.md` indexe `REQUEST_ORCHESTRATION.md`, `DEVELOPMENT_PHASES.md` et les nouveaux documents de gouvernance opératoire : capability map, methods, memory storage model et OpenWebUI plugin policy.
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
