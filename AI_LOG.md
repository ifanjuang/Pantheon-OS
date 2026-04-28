# AI LOG — Pantheon OS

Ce fichier sert de journal minimal de coordination entre l’utilisateur, ChatGPT, Claude et tout autre assistant IA intervenant sur le dépôt.

Objectif : éviter les doublons, conflits de branches, modifications contradictoires et incohérences entre code et documentation.

---

## Règles simples

1. Lire `AI_LOG.md` avant toute modification.
2. Lire les fichiers Markdown de référence avant toute modification structurante :
   - `STATUS.md`
   - `ROADMAP.md`
   - `ARCHITECTURE.md`
   - `AGENTS.md`
   - `MODULES.md`
   - `MEMORY.md`
   - `README.md`
3. Ne jamais pousser directement sur `main`.
4. Travailler sur une branche dédiée.
5. Noter ici chaque intervention significative.
6. Si un fichier critique est touché, le signaler clairement.
7. Les Markdown de référence restent la base du développement.
8. Si le code est plus pertinent que les Markdown, proposer ou appliquer d’abord la mise à jour documentaire.
9. Ne jamais inscrire dans le repo des informations issues de conversations privées, projets réels, clients, entreprises, adresses, chantiers ou personnes identifiables.

---

## Fichiers critiques

- `STATUS.md`
- `ROADMAP.md`
- `ARCHITECTURE.md`
- `AGENTS.md`
- `MODULES.md`
- `MEMORY.md`
- `README.md`
- `AI_LOG.md`
- `hermes/skill_policy.md`
- `hermes/external_skill_repos.md`
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
- Branche actuelle de travail : `work/chatgpt/hermes-docs-architecture-fr`
- Branche divergente à éviter : `work/chatgpt/hermes-code-rewrite`
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

### 2026-04-26 — ChatGPT

Branche : `feature/approval-gate-activation`

Objectif : acter le pivot documentaire Hermes-backed / Domain Operating Layer.

Modifications :

- Réécriture de `README.md` : Pantheon devient Domain Operating Layer ; Hermes Agent devient runtime agentique ; OpenWebUI devient interface + knowledge documentaire.
- Réécriture de `ARCHITECTURE.md` : architecture en trois couches, responsabilités OpenWebUI / Hermes Agent / Pantheon OS, memory model, approval discipline, Hermes Integration Layer.
- Réécriture de `AGENTS.md` : agents abstraits et neutres métier ; spécialisation uniquement par domain overlays, workflows, skills et knowledge policies.
- Réécriture de `MODULES.md` : modules recentrés sur contrats, domain overlays, skills, workflows, memory, knowledge, hermes integration et operations.
- Réécriture de `ROADMAP.md` : priorité à l’audit post-pivot, Hermes Lab isolé, skills métier, OpenWebUI Knowledge Strategy, mémoire validée et Hermes Integration Layer.
- Mise à jour de `STATUS.md` : pivot documentaire confirmé ; code existant marqué comme partiellement obsolète et à réauditer.
- Aucune modification de code.

Fichiers critiques touchés :

- `README.md`
- `ARCHITECTURE.md`
- `AGENTS.md`
- `MODULES.md`
- `ROADMAP.md`
- `STATUS.md`
- `AI_LOG.md`

Tests lancés :

- Non exécutés. Modification documentaire uniquement.

Points à vérifier :

- Le code existant reste majoritairement orienté ancienne trajectoire autonome : FastAPI, registries, workflow loader, approval API, Installer UI.
- Ces éléments doivent être audités avant conservation, réorientation, archivage ou suppression.
- Hermes Agent n’est pas installé. L’installation éventuelle doit se faire en Hermes Lab isolé, sans accès Docker socket, volumes Pantheon ou secrets.
- OpenWebUI Knowledge Strategy reste à créer.
- Les dossiers contractuels `agents/`, `domains/`, `skills/`, `workflows/`, `memory/`, `knowledge/`, `hermes/context/`, `operations/` restent à créer.

Prochaine action recommandée :

1. Faire l’audit post-pivot code/docs.
2. Créer le squelette contractuel Pantheon Domain Layer.
3. Préparer `hermes/context/pantheon_context.md`, `agents_context.md` et `rules_context.md`.
4. Définir la stratégie OpenWebUI Knowledge.
5. Préparer un plan d’installation Hermes Lab isolé.

---

### 2026-04-26 — ChatGPT

Branche : `work/chatgpt/hermes-code-rewrite`

Objectif : créer une première couche code alignée avec le pivot Hermes-backed, sans supprimer brutalement l’ancien runtime autonome.

Modifications :

- Création de la branche dédiée `work/chatgpt/hermes-code-rewrite`.
- Ajout du package `platform/api/pantheon_domain/`.
- Ajout de contrats Pydantic : agents, skills, workflows, memory stores, knowledge collections, legacy components et approval classification.
- Ajout d’un repository statique `DomainLayerRepository` représentant la doctrine Pantheon côté code.
- Ajout des routes FastAPI `/domain/*` : snapshot, agents, skills, workflows, memory, knowledge, legacy, approval classifier.
- Remplacement de `platform/api/main.py` par une entrée FastAPI simple Domain Layer.
- Ajout des tests ciblés `tests/test_domain_layer_api.py`.
- Mise à jour de `STATUS.md` pour indiquer que la première couche code existe, mais que les tests n’ont pas été exécutés ici.
- Aucun code externe intégré.
- Ancien runtime conservé dans le dépôt et marqué legacy à auditer.

Fichiers critiques touchés :

- `platform/api/main.py`
- `platform/api/pantheon_domain/__init__.py`
- `platform/api/pantheon_domain/contracts.py`
- `platform/api/pantheon_domain/repository.py`
- `platform/api/pantheon_domain/router.py`
- `tests/test_domain_layer_api.py`
- `STATUS.md`
- `AI_LOG.md`

Tests lancés :

- Non exécutés dans cette session.
- Tests ajoutés mais à lancer localement : `pytest tests/test_domain_layer_api.py`.

Points à vérifier :

- Compatibilité imports dans l’environnement local.
- Dépendances FastAPI / Pydantic / pytest / httpx.
- Ancien code legacy potentiellement cassé si `pytest` complet est lancé sans adaptation.
- Docker/NAS non testé.
- L’API ne charge plus automatiquement l’ancien runtime dynamique.
- Les endpoints `/debug/runtime-registry` et anciens modules ne sont plus le chemin principal.

Prochaine action recommandée :

1. Lancer `pytest tests/test_domain_layer_api.py`.
2. Démarrer l’API localement et vérifier `/health` et `/domain/snapshot`.
3. Créer les dossiers contractuels Markdown : `agents/`, `domains/`, `skills/`, `workflows/`, `memory/`, `knowledge/`, `hermes/context/`, `operations/`.
4. Auditer le legacy avant toute suppression.
5. Préparer Hermes Lab isolé seulement après validation de la couche Domain Layer.

---

### 2026-04-28 — ChatGPT

Branche : `work/chatgpt/hermes-docs-architecture-fr`

Objectif : formaliser le système de progression des skills Pantheon avec XP, niveaux, anti-farming et feedback utilisateur non intrusif.

Modifications :

- Mise à jour de `hermes/skill_policy.md`.
- Ajout des états de lifecycle : `candidate`, `active`, `probation`, `quarantine`, `archived`, `rejected`.
- Ajout d’un modèle XP qualitatif basé sur les améliorations validées, pas sur le volume d’usage.
- Ajout d’une table XP : feedback utile, clarification, correction de blocage, checklist, garde-fou, extraction de workflow, upgrade majeur.
- Ajout de règles anti-farming : pas de XP pour volume brut, doublons, auto-évaluation ou cosmétique.
- Ajout des niveaux : Candidate, Usable, Stable, Reliable, Expert, Core.
- Ajout des conditions de level-up : XP validée, absence de critique ouverte, exemples/tests/checklists à jour, privacy check, rollback, validation humaine.
- Ajout d’une politique de feedback non intrusif : demander seulement après réponse substantielle, méthode réutilisable, correction de blocage ou proposition de workflow/skill.
- Ajout du modèle `lifecycle` dans `manifest.yaml`.

Fichiers critiques touchés :

- `hermes/skill_policy.md`
- `AI_LOG.md`

Tests lancés :

- Non exécutés. Modification documentaire uniquement.

Points à vérifier :

- Reporter les règles XP/levels dans `MODULES.md` lors de l’alignement.
- Prévoir les champs `lifecycle` dans les futurs `manifest.yaml`.
- Ne pas transformer le feedback utilisateur en demande systématique après chaque réponse.
- Garder les XP comme `pending_xp` tant qu’une review n’a pas validé l’amélioration.

Prochaine action recommandée :

1. Aligner `MODULES.md` sur lifecycle + XP.
2. Créer les premières skills `domains/general` avec `manifest.yaml` incluant `lifecycle`.
3. Prévoir un workflow `skill_review.yaml` avant tout level-up.

---

### 2026-04-29 — ChatGPT

Branche : `work/chatgpt/hermes-docs-architecture-fr`

Objectif : poser le P0 de l’interaction OpenWebUI / Hermes / Pantheon et ajouter la résolution de contexte projet.

Modifications :

- Mise à jour de `STATUS.md` avec `OpenWebUI / Hermes / Pantheon interaction layer — planned`.
- Mise à jour de `MODULES.md` pour ajouter les modules planifiés : Consultation, Evidence Pack, Run Graph, Runtime Context Pack, Knowledge Selection.
- Ajout du package `platform/api/pantheon_runtime/`.
- Ajout d’un endpoint statique read-only `GET /runtime/context-pack`.
- Branchement du router runtime dans `platform/api/main.py`.
- Ajout de la skill candidate `domains/general/skills/project_context_resolution/`.
- Ajout de règles de résolution de contexte projet : alias, fautes de frappe, indices partiels, commune, rue, client, sujet, mémoire session/projet, Knowledge Registry, Notion read-only éventuel.
- Ajout de la règle inverse : ne pas forcer le contexte projet si la question est générale ou répondable sans contexte spécifique.
- Ajout de la politique Notion : lecture seule par défaut, écriture uniquement après affichage des champs à modifier et validation explicite.
- Ajout du template local Hermes `hermes/templates/pantheon-os/` avec `SKILL.md`, exemple d’audit repo et helper read-only `pantheon_context_pack.py`.

Fichiers critiques touchés :

- `STATUS.md`
- `MODULES.md`
- `AI_LOG.md`
- `platform/api/main.py`
- `platform/api/pantheon_runtime/__init__.py`
- `platform/api/pantheon_runtime/router.py`
- `domains/general/skills/project_context_resolution/SKILL.md`
- `domains/general/skills/project_context_resolution/manifest.yaml`
- `domains/general/skills/project_context_resolution/examples.md`
- `domains/general/skills/project_context_resolution/tests.md`
- `domains/general/skills/project_context_resolution/UPDATES.md`
- `hermes/templates/pantheon-os/SKILL.md`
- `hermes/templates/pantheon-os/examples/audit_repo.md`
- `hermes/templates/pantheon-os/scripts/pantheon_context_pack.py`

Tests lancés :

- Non exécutés dans cette session.

Points à vérifier :

- Lancer les tests existants ciblés après checkout local.
- Vérifier le démarrage FastAPI et les routes `/health`, `/domain/snapshot`, `/runtime/context-pack`.
- Le Context Pack est statique : il oriente Hermes mais ne remplace pas les Markdown de référence.
- Le template Hermes `pantheon-os` n’est pas installé localement ; il doit être copié vers `~/.hermes/skills/pantheon-os/` avant usage.
- La connexion Notion n’est pas implémentée ; seule la politique de lecture/écriture candidate est documentée.
- Le template Evidence Pack exécutable ou YAML n’a pas été ajouté : deux tentatives de création ont été bloquées par le contrôle de sécurité de l’outil GitHub. La structure reste documentée dans `MODULES.md` et `hermes/templates/pantheon-os/SKILL.md`.
- Le legacy autonome reste à auditer avant conservation, réorientation ou suppression.

Prochaine action recommandée :

1. Lancer `pytest tests/test_domain_layer_api.py` et vérifier l’import du nouveau router runtime.
2. Démarrer l’API localement et tester `GET /runtime/context-pack`.
3. Créer `knowledge/registry.yaml` et la skill candidate `knowledge_selection`.
4. Définir un mapping Notion read-only avant toute écriture possible.
5. Créer une spécification OpenWebUI Router Pipe + Actions.

---

### YYYY-MM-DD — Claude

Branche :

Objectif :

Modifications :

Fichiers critiques touchés :

Tests lancés :

Points à vérifier :

Prochaine action recommandée :
