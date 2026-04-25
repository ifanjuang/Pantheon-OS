# Diagnostic Pantheon OS

## Synthèse

Audit initial réalisé après lecture des fichiers Markdown de référence et inspection ciblée du code accessible dans le dépôt.

Le dépôt confirme une base MVP réelle : FastAPI, PostgreSQL + pgvector, OpenWebUI, Ollama, Docker Compose, registry d’applications API et manifests API. La stack déclarée dans le README est donc partiellement alignée avec le code.

En revanche, plusieurs éléments structurants documentés comme direction stable ou backlog immédiat ne sont pas encore confirmés dans le code, ou sont explicitement désactivés : `decisions`, `memory`, `monitoring`, `control`, `flowmanager`, `evaluation`, `orchestra`. Le fichier `main.py` importe aussi un `ManifestLoader` pour agents, skills et workflows, mais l’audit ciblé n’a pas retrouvé son fichier d’implémentation. Ce point est critique car il peut bloquer le démarrage si le module est réellement absent.

Conclusion : Pantheon OS dispose d’un socle MVP, mais la couche runtime multi-agent documentée est encore partielle ou à vérifier. La prochaine étape prioritaire n’est pas d’ajouter un Browser Tool ou une UI avancée, mais de corriger ou confirmer les fondations : manifest loader, contrats, modules désactivés, mémoire, approval et observability.

## Cohérence documentation / code

### Aligné

| Élément | Documentation | Code observé | Statut |
|---|---|---|---|
| Stack Docker MVP | README.md décrit FastAPI, PostgreSQL + pgvector, OpenWebUI, Ollama | `docker-compose.yml` contient `db`, `api`, `openwebui`, `ollama` | Aligné |
| PostgreSQL + pgvector | README.md et ARCHITECTURE.md | `docker-compose.yml` utilise `pgvector/pgvector:pg16` | Aligné |
| OpenWebUI comme interface | README.md | `openwebui` configuré sur API OpenAI-compatible | Aligné |
| API FastAPI | README.md / ARCHITECTURE.md | `platform/api/main.py` crée une app FastAPI | Aligné |
| Registry API modulaire | README.md / ARCHITECTURE.md | `ModuleRegistry` charge les apps depuis `modules.yaml` | Aligné partiel |
| Manifests API | README.md / MODULES.md | `platform/api/apps/*/manifest.yaml` existe pour les modules vérifiés | Aligné partiel |

### Partiel

| Élément | Documentation | Code observé | Statut |
|---|---|---|---|
| Auto-discovery agents / skills / workflows | README.md et ARCHITECTURE.md annoncent `ManifestLoader` | `main.py` importe `core.registries.loader.ManifestLoader`, mais fichier non retrouvé par audit ciblé | Contradictoire / À vérifier |
| Hermes Console | README.md et `modules.yaml` activent `hermes_console` | manifest présent | Partiel, contenu fonctionnel non audité |
| Decisions | STATUS.md indique module à finaliser | `modules.yaml` désactive `decisions` | Documenté mais non actif |
| Memory | STATUS.md décrit refactoring mémoire prioritaire | `modules.yaml` désactive `memory` | Documenté mais non actif |
| Monitoring | STATUS.md décrit monitoring à compléter | `modules.yaml` désactive `monitoring` | Documenté mais non actif |
| Control / FlowManager | STATUS.md mentionne `FlowManager` livré historiquement | `modules.yaml` désactive `control` et `flowmanager` | Contradictoire / À vérifier |
| Evaluation | ROADMAP.md et STATUS.md prévoient scoring/evaluation | `modules.yaml` désactive `evaluation` et `scoring` | Documenté mais non actif |

### Non confirmé dans le code pendant cet audit

- `ApprovalRequest`
- `ApprovalService`
- Approval Gate branché sur PolicyGate
- `candidate_facts`
- `active_facts`
- `memory_context_preview`
- `consolidation_dry_run`
- `Task Contract`
- `tasks.yaml`
- `Action / Provider / Evaluator / Service contracts`
- `Skill Security Scan`
- Browser action traces

Ces éléments doivent rester marqués comme `Documenté mais non implémenté` ou `À vérifier` jusqu’à preuve contraire dans le code.

## Incohérences détectées

| Élément | Fichier MD concerné | Code concerné | Problème | Décision proposée | Priorité |
|---|---|---|---|---|---|
| `ManifestLoader` agents/skills/workflows | README.md, ARCHITECTURE.md, MODULES.md | `platform/api/main.py` | `main.py` importe `core.registries.loader.ManifestLoader`, mais l’implémentation n’a pas été retrouvée | Créer ou corriger `ManifestLoader`, ou retirer l’import si non utilisé | P0 |
| Modules avancés désactivés | STATUS.md, ROADMAP.md | `modules.yaml` | `decisions`, `memory`, `monitoring`, `control`, `flowmanager`, `evaluation`, `orchestra` sont désactivés alors que certains sont décrits comme livrés ou prioritaires | Mettre STATUS.md en statut réel : désactivé / partiel / à vérifier | P0 |
| Manifests API trop pauvres | MODULES.md | `platform/api/apps/*/manifest.yaml` | Manifests observés contiennent `name`, `version`, `description`, `prefix`, `depends_on`, mais pas `type`, `enabled`, `priority`, `inputs`, `outputs`, `risk_profile`, `side_effect_profile` | Implémenter ManifestSchema V2 compatible rétroactivement | P1 |
| Approval Gate | ARCHITECTURE.md, MODULES.md, AGENTS.md, STATUS.md | Non confirmé | Fonction critique documentée mais pas observée dans code | Implémenter modèle, service, API, pause/resume minimal | P1 |
| Mémoire auditable | ARCHITECTURE.md, MODULES.md, STATUS.md | Module `memory` désactivé | Doctrine documentée mais implémentation non active ou non confirmée | Auditer DB/models puis implémenter `context_preview` | P1 |
| Task Contract | MODULES.md, ROADMAP.md | Non confirmé | Workflows documentés mais tasks explicites non confirmées | Ajouter `TaskDefinition`, `tasks.yaml`, expected_output obligatoire | P1 |
| Observability | ARCHITECTURE.md, STATUS.md | Partiel non confirmé | Traces avancées non vérifiées | Standardiser `run_id`, events, task/tool/approval/memory traces | P2 |
| Browser Tool | ARCHITECTURE.md, STATUS.md | Non confirmé | Documenté comme futur et risqué | Reporter après Approval + Observability | P3 |

## Améliorations proposées

| Amélioration | Source | Fichier MD à modifier | Impact code | Risque | Priorité |
|---|---|---|---|---|---|
| Audit code/docs systématique | Doctrine Pantheon OS | STATUS.md | Faible | Faible | P0 |
| Corriger ou créer `ManifestLoader` | README / code actuel | ARCHITECTURE.md, MODULES.md si besoin | Moyen | Moyen | P0 |
| ManifestSchema V2 | Eliza, agentskills, doctrine Pantheon | MODULES.md | Moyen | Faible | P1 |
| Task Contract + `tasks.yaml` | CrewAI | MODULES.md, ROADMAP.md | Moyen | Faible | P1 |
| Approval Gate minimal | langgraph-approval-hub | ARCHITECTURE.md, STATUS.md | Moyen | Faible à moyen | P1 |
| Memory context preview | hermes-local-memory | ARCHITECTURE.md, STATUS.md | Moyen | Moyen | P1 |
| Evaluator contract | Eliza | MODULES.md, ROADMAP.md | Moyen | Faible | P2 |
| Skill Security Scan | HermesHub / agentskills | MODULES.md, STATUS.md | Moyen | Moyen | P2 |
| Browser Tool lecture seule | browser-harness | ROADMAP.md | Moyen | Élevé si mal gouverné | P3 |

## Décisions documentaires

### STATUS.md

Mettre à jour avec une section `Audit code/docs — 2026-04-26` :

- `ManifestLoader` : Contradictoire / À vérifier critique.
- `decisions` : Documenté mais désactivé.
- `memory` : Documenté mais désactivé.
- `monitoring` : Documenté mais désactivé.
- `control` / `flowmanager` : Mentionné livré historiquement mais désactivé, donc contradictoire jusqu’à audit complet.
- `Approval Gate` : Documenté mais non implémenté confirmé.
- `Browser Tool` : Futur, à reporter.

### ROADMAP.md

Conserver l’ordre prioritaire :

1. Audit code/docs.
2. Correction ManifestLoader.
3. Manifest hardening.
4. Task Contract.
5. Approval Gate.
6. Memory context preview.
7. Observability.
8. Evaluators.
9. Skill Security Scan.
10. Browser Tool plus tard.

### ARCHITECTURE.md

Pas de modification urgente. Le document est plus avancé que le code. Il doit rester la cible, mais `STATUS.md` doit clarifier l’écart.

### MODULES.md

Pas de modification urgente avant code. Les contrats sont déjà plus riches que l’implémentation actuelle.

### AGENTS.md

Pas de modification urgente avant code.

### README.md

Pas de modification urgente. Il décrit une ambition cohérente, mais `STATUS.md` doit mieux distinguer MVP actif et V2 documentaire.

## Décisions code

### P0 — Corriger le démarrage potentiel

Vérifier ou créer :

```text
platform/api/core/registries/loader.py
```

Le fichier doit fournir :

```python
class ManifestLoader:
    def __init__(self, base_path): ...
    def load_agents(self): ...
    def load_skills(self): ...
    def load_workflows(self): ...
```

Comportement minimal acceptable :

- ne pas crasher si `/modules` est absent ou vide ;
- retourner des listes vides ;
- logguer clairement les manifests invalides ;
- préparer validation future sans bloquer MVP.

### P1 — Manifest hardening

Créer `ManifestSchema` rétrocompatible pour les API apps, puis l’étendre aux agents, skills, tools et workflows.

Champs V2 recommandés :

```yaml
id: auth
type: api_app
version: "1.0.0"
enabled: true
priority: 0
dependencies: []
risk_profile: low
side_effect_profile: internal
inputs: []
outputs: []
```

### P1 — Approval minimal

Créer :

```text
platform/api/apps/approvals/
```

Avec modèle, service, router et migration.

### P1 — Memory context preview

Créer ou compléter :

```text
platform/api/apps/memory/
core/memory/
```

Objectif minimal : exposer ce qui serait injecté à un agent avant exécution.

## Plan d’action

### Immédiat

1. Mettre à jour `STATUS.md` avec cet audit.
2. Corriger ou créer `ManifestLoader` pour éviter un crash startup.
3. Ajouter un test de démarrage minimal.

### Court terme

1. ManifestSchema V2 rétrocompatible.
2. Task Contract + `tasks.yaml`.
3. Approval Gate minimal.
4. Memory context preview.

### Moyen terme

1. Observability events normalisés.
2. Evaluators post-run.
3. Skill Security Scan.
4. Console enrichie pour modules, memory, approvals, traces.

### À surveiller

- Browser Tool.
- Flowise-like visual builder.
- MCP / A2A.
- Voice.
- Neo4j.

## Résumé final

Le dépôt a une base MVP réelle et cohérente avec une partie du README : FastAPI, Docker, PostgreSQL/pgvector, OpenWebUI, modules API. En revanche, le runtime multi-agent complet documenté reste partiel : plusieurs modules structurants sont désactivés et certaines classes attendues ne sont pas confirmées dans le code.

La priorité logique est de sécuriser le démarrage et la cohérence : `ManifestLoader`, audit STATUS, manifests V2. Ensuite seulement : Approval Gate, mémoire auditable, task contracts et observability.
