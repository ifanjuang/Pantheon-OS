# Pantheon OS — Project Status

> Source de vérité sur l’état actuel du projet après pivot architectural.
> Les fichiers Markdown de référence pilotent le développement : `README.md`, `ARCHITECTURE.md`, `MODULES.md`, `AGENTS.md`, `ROADMAP.md`, `STATUS.md`.

Dernière mise à jour : 2026-04-26

---

# 1. Décision structurante

Statut : ✅ Décision documentaire actée.

Pantheon OS adopte une trajectoire Hermes-backed.

```text
OpenWebUI = interface chat + knowledge documentaire
Hermes Agent = runtime agentique + skills + tools + scheduler + doctor + gateway + mémoire opérationnelle
Pantheon OS = Domain Operating Layer + agents abstraits + workflows + skills contracts + mémoire validée + gouvernance
```

Formule de conception :

```text
Pantheon définit.
Hermes exécute.
OpenWebUI expose et retrouve.
```

Cette décision remplace la trajectoire antérieure où Pantheon devait devenir un runtime agentique autonome complet.

---

# 2. État global

| Élément | Statut | Commentaire |
|---|---|---|
| Pivot documentaire Hermes-backed | ✅ Fait | `README.md`, `ARCHITECTURE.md`, `AGENTS.md`, `MODULES.md`, `ROADMAP.md` mis à jour |
| Branche code post-pivot | ✅ Créée | `work/chatgpt/hermes-code-rewrite` |
| Nouvelle API Domain Layer | ✅ Première passe | `platform/api/pantheon_domain/*` + `platform/api/main.py` |
| Ancien runtime autonome | ⚠️ Legacy non supprimé | Conservé dans le repo, mais plus booté par défaut dans la nouvelle entrée API |
| Tests Domain Layer | 🔄 Écrits, non exécutés ici | `tests/test_domain_layer_api.py` ajouté, exécution locale/CI à faire |
| Hermes Agent | ⬜ Non installé | À tester plus tard en Hermes Lab isolé |
| OpenWebUI Knowledge Strategy | ⬜ À faire | Collections et source policy à créer |
| Agents abstraits | 🔄 Codés partiellement | Exposés dans le repository statique `DomainLayerRepository` |
| Skills métier | 🔄 Codées partiellement | Premières definitions candidates exposées via `/domain/skills` |
| Mémoire validée Pantheon | 🔄 Codée partiellement | Memory stores exposés via `/domain/memory`, fichiers Markdown à créer |
| Ancien Approval Gate API | ⚠️ Legacy à classer | Non supprimé ; remplacé par un classifier léger `/domain/approval/classify` pour la première passe |
| Installer UI existante | ⚠️ Legacy à classer | À réorienter vers Hermes Lab / NAS preflight si conservée |

---

# 3. Cohérence documentation / code

## 3.1 Documentation

Statut : ✅ Alignée sur la trajectoire Hermes-backed.

Les fichiers suivants décrivent Pantheon comme Domain Operating Layer :

- `README.md` ;
- `ARCHITECTURE.md` ;
- `AGENTS.md` ;
- `MODULES.md` ;
- `ROADMAP.md` ;
- `STATUS.md`.

## 3.2 Code nouveau

Statut : 🔄 Première couche alignée.

Ajouts et changements effectués sur `work/chatgpt/hermes-code-rewrite` :

- `platform/api/pantheon_domain/__init__.py` ;
- `platform/api/pantheon_domain/contracts.py` ;
- `platform/api/pantheon_domain/repository.py` ;
- `platform/api/pantheon_domain/router.py` ;
- `platform/api/main.py` remplacé par une entrée FastAPI simple Domain Layer ;
- `tests/test_domain_layer_api.py`.

Endpoints principaux :

- `/health` ;
- `/domain/health` ;
- `/domain/snapshot` ;
- `/domain/agents` ;
- `/domain/skills` ;
- `/domain/workflows` ;
- `/domain/memory` ;
- `/domain/knowledge` ;
- `/domain/legacy` ;
- `/domain/approval/classify`.

## 3.3 Code legacy

Statut : ⚠️ Présent, non supprimé.

Le dépôt contient encore les éléments de l’ancienne architecture autonome :

- `platform/api/apps/*` ;
- `modules.yaml` ;
- registries ;
- workflow loader ;
- `TaskDefinition` / `WorkflowDefinition` legacy ;
- module `approvals` legacy ;
- migration Alembic `approval_requests` ;
- Installer UI ;
- tests contractuels legacy.

Ces éléments sont classés dans `/domain/legacy` comme composants à auditer :

- `fastapi_runtime` ;
- `module_registry` ;
- `workflow_loader` ;
- `approval_api` ;
- `installer_ui`.

Aucune suppression n’a été faite.

---

# 4. Ce qui reste fiable

## 4.1 Source de vérité documentaire

Les Markdown de référence font foi. Toute évolution du code doit découler de ces documents.

## 4.2 Domain Layer API

La nouvelle API expose la doctrine Pantheon sans démarrer automatiquement les anciens modules dynamiques.

## 4.3 Agents abstraits

Les agents restent neutres métier. Le métier vient des domain overlays, workflows, skills et knowledge policies.

## 4.4 Séparation des mémoires

La règle cible reste :

```text
Hermes peut apprendre.
Pantheon valide.
OpenWebUI documente.
```

## 4.5 Séparation des responsabilités

OpenWebUI ne définit pas les agents. Hermes n’est pas autorisé à redéfinir la doctrine Pantheon. Pantheon ne réimplémente pas les capacités Hermes sans gain clair.

---

# 5. Tests

Statut : ⚠️ Non exécutés dans cette intervention.

Tests ajoutés :

```text
tests/test_domain_layer_api.py
```

Commandes à lancer localement :

```bash
pytest tests/test_domain_layer_api.py
```

Puis, si le legacy doit rester importable :

```bash
pytest
```

Points de vigilance :

- dépendances FastAPI / Pydantic / pytest / httpx à vérifier dans l’environnement ;
- ancien code susceptible d’avoir des imports devenus non utilisés ;
- CI non vérifiée ;
- pas de test Docker exécuté.

---

# 6. Chantiers immédiats

## P0 — Tester la première couche Domain Layer

À faire :

- lancer `pytest tests/test_domain_layer_api.py` ;
- lancer l’API localement ;
- vérifier `/health` ;
- vérifier `/domain/snapshot` ;
- vérifier `/domain/approval/classify` ;
- corriger imports ou dépendances si nécessaire.

## P0 — Audit post-pivot du legacy

Objectif : comparer l’ancien code à la nouvelle architecture documentaire.

À vérifier :

- `platform/api/apps/*` ;
- `platform/api/core/*` ;
- `modules/` ;
- `modules.yaml` ;
- `alembic/versions/` ;
- `docker-compose.yml` ;
- `scripts/install/` ;
- tests existants.

Livrable attendu : diagnostic de cohérence code/docs et décision de conservation/réorientation/archivage.

## P0/P1 — Créer les dossiers contractuels Markdown

À créer :

```text
agents/
domains/architecture/
skills/
workflows/
memory/
knowledge/
hermes/context/
operations/
```

## P1 — Hermes Lab isolé

À faire :

- installer Hermes Agent dans un environnement isolé ;
- ne pas donner accès au Docker socket ;
- ne pas donner accès aux volumes Pantheon ;
- ne pas exposer les secrets Pantheon ;
- tester CLI, doctor, mémoire, skills, Ollama LAN ;
- documenter les résultats.

## P1 — OpenWebUI Knowledge Strategy

À faire :

- définir collections ;
- définir source policy ;
- définir taxonomy ;
- distinguer documents projet, agence, réglementaire, modèle, obsolète.

## P1 — Skills métier initiales

À matérialiser en fichiers :

- `cctp_audit` ;
- `dpgf_check` ;
- `notice_architecturale` ;
- `repo_md_audit` ;
- `source_check` ;
- `client_message`.

---

# 7. Chantiers ralentis ou dépriorisés

Les éléments suivants ne doivent plus être traités comme cœur prioritaire :

- runtime agentique FastAPI complet ;
- scheduler maison ;
- gateway messagerie maison ;
- terminal backend maison ;
- runtime skills maison ;
- dashboard lourd ;
- marketplace interne ;
- Browser Tool avant discipline safety ;
- microservices.

Ils peuvent rester en option, être réorientés ou être archivés après audit.

---

# 8. Points de vigilance

- Ne pas installer Hermes Agent globalement sur le NAS sans isolation.
- Ne pas donner à Hermes accès aux volumes Pantheon ou au Docker socket au début.
- Ne pas laisser OpenWebUI devenir source officielle des agents ou de la mémoire validée.
- Ne pas promouvoir automatiquement une mémoire Hermes dans Pantheon.
- Ne pas activer une skill générée par Hermes sans validation.
- Ne pas supprimer l’ancien code avant audit post-pivot.
- Ne pas merger la branche `work/chatgpt/hermes-code-rewrite` sans tests locaux.

---

# 9. Prochaine action recommandée

1. Lancer `pytest tests/test_domain_layer_api.py`.
2. Corriger les éventuels imports/dépendances.
3. Lancer l’API et tester `/domain/snapshot`.
4. Créer les dossiers contractuels Markdown.
5. Auditer le legacy avant suppression ou archivage.

---

# 10. Résumé final

Fiable maintenant : la direction documentaire et la première API Domain Layer.

Non fiable encore : exécution réelle des tests et compatibilité complète avec l’environnement local/NAS.

Prochaine étape logique : test local ciblé, puis création du squelette contractuel Markdown.
