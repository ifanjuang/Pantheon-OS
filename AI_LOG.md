# AI LOG — Pantheon OS

Ce fichier sert de journal minimal de coordination entre l’utilisateur, ChatGPT, Claude et tout autre assistant IA intervenant sur le dépôt.

Objectif : éviter les doublons, conflits de branches, modifications contradictoires et incohérences entre code et documentation.

---

## Règles simples

1. Lire `AI_LOG.md` avant toute modification.
2. Lire les six fichiers Markdown de référence avant toute modification structurante :
   - `STATUS.md`
   - `ROADMAP.md`
   - `ARCHITECTURE.md`
   - `AGENTS.md`
   - `MODULES.md`
   - `README.md`
3. Ne jamais pousser directement sur `main`.
4. Travailler sur une branche dédiée.
5. Noter ici chaque intervention significative.
6. Si un fichier critique est touché, le signaler clairement.
7. Les Markdown de référence restent la base du développement.
8. Si le code est plus pertinent que les Markdown, proposer ou appliquer d’abord la mise à jour documentaire.

---

## Fichiers critiques

- `STATUS.md`
- `ROADMAP.md`
- `ARCHITECTURE.md`
- `AGENTS.md`
- `MODULES.md`
- `README.md`
- `modules.yaml`
- `platform/api/main.py`
- `platform/api/core/health.py`
- `platform/api/core/registry.py`
- `platform/api/core/registries/*`
- `platform/api/core/contracts/*`
- `platform/api/apps/*`
- `alembic/versions/*`
- `docker-compose.yml`
- `.env.example`

---

## Branches recommandées

- ChatGPT : `work/chatgpt/*` ou `feature/chatgpt/*`
- Claude : `work/claude/*` ou `feature/claude/*`
- Branche actuelle de travail : `feature/approval-gate-activation`
- `main` : stable uniquement

---

## Template d’entrée

```md
### YYYY-MM-DD — Assistant / outil

Branche :

Objectif :

Modifications :

Fichiers critiques touchés :

Tests lancés :

Points à vérifier :

Prochaine action recommandée :
```

---

## Log

### 2026-04-26 — ChatGPT

Branche : `feature/approval-gate-activation`

Objectif : renforcer les fondations de Pantheon OS avant activation des modules avancés.

Modifications :

- Ajout `CODE_AUDIT.md`.
- Ajout `ManifestLoader` runtime tolérant.
- Ajout contrat manifest progressif `ComponentManifest`.
- Branchement du contrat manifest dans `ModuleRegistry` et `ManifestLoader`.
- Ajout contrats `TaskDefinition` et `WorkflowDefinition`.
- Ajout loader `workflow.yaml` / `tasks.yaml`.
- Branchement du loader workflow au startup dans `platform/api/main.py`.
- Ajout workflow réel `modules/workflows/document_analysis/`.
- Ajout endpoint debug `/debug/runtime-registry`.
- Ajout module `approvals` avec modèle, schémas, service, router.
- Ajout migration `approval_requests`.
- Enregistrement `approvals` dans `modules.yaml` mais avec `enabled: false`.
- Ajout tests contractuels manifests, tasks, workflows, approval.
- Ajout Installer UI autonome NAS + Ollama LAN.
- Ajout script Windows pour préparer Ollama.
- Ajout gouvernance versions : `VERSION`, `CHANGELOG.md`, `VERSIONS.md`, `EXTERNAL_WATCHLIST.md`.
- Ajout scripts update partiels.
- Ajout `AI_LOG.md` comme journal simple de coordination IA.

Fichiers critiques touchés :

- `STATUS.md`
- `modules.yaml`
- `platform/api/main.py`
- `platform/api/core/health.py`
- `platform/api/core/registry.py`
- `platform/api/core/registries/loader.py`
- `platform/api/core/registries/workflows.py`
- `platform/api/core/contracts/manifest.py`
- `platform/api/core/contracts/tasks.py`
- `platform/api/apps/approvals/*`
- `alembic/versions/20260426_0001_add_approval_requests.py`

Tests lancés :

- Non exécutés dans cette session.

Points à vérifier :

- Migration Approval Gate : `down_revision = None` à vérifier avec `alembic heads`.
- Tests non exécutés.
- Installer UI non testée sur NAS.
- Module `approvals` toujours désactivé.
- Les workflows sont chargés et exposés, mais pas encore exécutés par un moteur runtime.
- `OpenWebUI` utilise encore un tag Docker potentiellement instable si `main` est conservé.

Prochaine action recommandée :

1. Lancer l’Installer UI sur NAS : `bash scripts/install/ui/launch_installer.sh`.
2. Vérifier Docker, Ollama, `.env`, containers, migrations, tests, `/health`, `/debug/runtime-registry`.
3. Vérifier Alembic avec `alembic heads`.
4. Corriger `down_revision` si nécessaire.
5. Exécuter les tests ciblés.
6. Activer `approvals` seulement après validation migration + tests.

---

### 2026-04-26 — ChatGPT

Branche : `feature/approval-gate-activation`

Objectif : ajouter `mage0535/hermes-memory-installer` à la roadmap comme source externe mémoire / installation, sans intégration code.

Modifications :

- Mise à jour de `ROADMAP.md` section `Memory Roadmap`.
- Ajout de `mage0535/hermes-memory-installer` dans `External Inspiration Map` sous `À intégrer plus tard`.
- Décision documentaire : retenir l’idée d’installation mémoire locale, injection mémoire, auto-mount de skills et archivage comme piste ultérieure.
- Décision de rejet : ne pas reprendre SQLite FTS5 comme source de vérité principale, ni installation intrusive non auditée, ni promotion mémoire non validée.

Fichiers critiques touchés :

- `ROADMAP.md`
- `AI_LOG.md`

Tests lancés :

- Non exécutés. Modification documentaire uniquement.

Points à vérifier :

- Le dépôt externe n’a pas encore été audité en profondeur fichier par fichier.
- L’idée doit rester en veille jusqu’à stabilisation du modèle mémoire Pantheon, Approval Gate et PolicyGate.

Prochaine action recommandée :

1. Ne pas intégrer de code depuis `hermes-memory-installer` maintenant.
2. Continuer d’abord Lot A : Installer UI, Alembic, tests.
3. Revenir à cette piste pendant le chantier mémoire multi-couches.

---

### 2026-04-26 — ChatGPT

Branche : `feature/approval-gate-activation`

Objectif : consolider tous les repos externes déjà évoqués dans `EXTERNAL_WATCHLIST.md`.

Modifications :

- Ajout ou clarification des entrées : `hermes-memory-installer`, `RAG-Evaluation`, `browser-harness`, `Langflow`, `Dify`, `n8n`, `OmniTools`, `StartOS`, `CommonMark`, `agents-towards-production`.
- Ajout d’une synthèse par chantier Pantheon : governance documentaire, runtime contracts, approval, memory, RAG quality, self-hosting, visual lab, automation périphérique, local tools, browser tool.
- Ajout de règles d’usage : pas de second runtime de vérité, pas d’import massif d’agents, pas de Browser Tool avant Approval/Policy/Observability, pas de mise à jour automatique sans consentement.

Fichiers critiques touchés :

- `EXTERNAL_WATCHLIST.md`
- `AI_LOG.md`

Tests lancés :

- Non exécutés. Modification documentaire uniquement.

Points à vérifier :

- Certains dépôts sont classés après analyse conceptuelle, sans audit fichier par fichier.
- Aucun code externe n’a été intégré.
- Les idées restent subordonnées aux Markdown de référence et au modèle Pantheon.

Prochaine action recommandée :

1. Continuer Lot A : Installer UI, Alembic, tests.
2. Ne pas ouvrir de nouveau chantier externe avant stabilisation.
3. Reprendre ensuite Approval Gate complet, puis mémoire et RAG Evaluation.

---

### YYYY-MM-DD — Claude

Branche :

Objectif :

Modifications :

Fichiers critiques touchés :

Tests lancés :

Points à vérifier :

Prochaine action recommandée :
