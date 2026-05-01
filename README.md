# Pantheon Next

Pantheon Next est une couche de gouvernance documentaire, métier et opérationnelle pour piloter l’usage d’agents IA, de workflows, d’outils externes et de mémoire projet sans recréer un runtime agentique autonome.

La règle structurante du projet est simple :

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

Pantheon Next ne remplace pas Hermes Agent, OpenWebUI ou les outils spécialisés. Il définit le cadre dans lequel ils travaillent.

---

## Vision

Pantheon Next sert à rendre une architecture agentique contrôlée, traçable et exploitable dans un contexte professionnel.

Le système doit permettre de :

- définir des domaines métier ;
- cadrer des agents abstraits ;
- formaliser des workflows ;
- produire des task contracts ;
- imposer des approvals ;
- exiger des Evidence Packs ;
- distinguer Knowledge et Memory ;
- encadrer les outils externes ;
- produire des context packs pour Hermes Agent ;
- conserver une mémoire canonique validée ;
- éviter les actions non gouvernées.

Pantheon Next est donc une autorité documentaire et métier.

Hermes Agent reste le runtime d’exécution.

OpenWebUI reste le cockpit utilisateur.

---

## Principe d’architecture

```text
Utilisateur
  ↓
OpenWebUI
  ↓
Hermes Agent Gateway
  ↓
Pantheon API
  ↓
Pantheon Markdown Source of Truth
```

### OpenWebUI

OpenWebUI est l’interface utilisateur.

Il expose :

- le chat ;
- les Knowledge Bases ;
- les conversations ;
- les résultats ;
- les demandes de validation ;
- les Evidence Packs ;
- les actions utilisateur.

OpenWebUI ne doit pas devenir :

- la mémoire canonique ;
- le moteur de gouvernance ;
- le runtime agentique ;
- la source de vérité documentaire.

### Hermes Agent

Hermes Agent est le runtime d’exécution.

Il exécute :

- les skills exécutables ;
- les tools ;
- les traitements locaux ;
- les opérations sandboxées ;
- les analyses ;
- les patch candidates ;
- les Evidence Packs.

Hermes Agent agit dans le cadre fourni par Pantheon Next.

Il ne doit pas :

- canoniser une mémoire ;
- modifier les Markdown source de vérité sans validation ;
- contourner les approvals ;
- pousser sur `main` ;
- installer des plugins hors allowlist ;
- accéder aux secrets par défaut.

### Pantheon Next

Pantheon Next gouverne.

Il définit :

- la doctrine ;
- les domaines ;
- les agents abstraits ;
- les workflows ;
- les task contracts ;
- les approvals ;
- les Evidence Packs ;
- la mémoire canonique ;
- les context packs ;
- les policies d’outils externes ;
- les règles d’intégration OpenWebUI ;
- les règles d’intégration Hermes.

Pantheon Next ne doit pas implémenter :

- un Execution Engine autonome ;
- un Agent Runtime ;
- un Tool Runtime ;
- un Provider Router LLM ;
- un scheduler interne ;
- un LangGraph central ;
- une mémoire auto-promue ;
- une self-evolution automatique ;
- un dashboard lourd en P0.

---

## Source de vérité documentaire

Les fichiers Markdown pilotent le projet.

La documentation n’est pas un commentaire du code. Elle est la source de vérité. Le code doit suivre les documents de gouvernance, sauf lorsqu’un élément existant dans le code apporte une solution manifestement supérieure. Dans ce cas, la documentation doit d’abord être mise à jour avant de généraliser l’amélioration.

Emplacement canonique :

```text
docs/governance/
```

Documents principaux :

```text
docs/governance/STATUS.md
docs/governance/ROADMAP.md
docs/governance/ARCHITECTURE.md
docs/governance/MODULES.md
docs/governance/AGENTS.md
docs/governance/MEMORY.md
docs/governance/APPROVALS.md
docs/governance/TASK_CONTRACTS.md
docs/governance/EVIDENCE_PACK.md
docs/governance/HERMES_INTEGRATION.md
docs/governance/OPENWEBUI_INTEGRATION.md
docs/governance/EXTERNAL_TOOLS_POLICY.md
docs/governance/CODE_AUDIT_POST_PIVOT.md
```

`README.md` reste la porte d’entrée du projet.

Le journal des interventions IA vit dans `ai_logs/`, conformément à `ai_logs/README.md`.

---

## Structure cible du dépôt

```text
Pantheon-Next/
  README.md

  ai_logs/
    README.md
    YYYY-MM-DD-slug.md

  docs/
    governance/
      README.md
      STATUS.md
      ROADMAP.md
      ARCHITECTURE.md
      MODULES.md
      AGENTS.md
      MEMORY.md
      APPROVALS.md
      TASK_CONTRACTS.md
      EVIDENCE_PACK.md
      HERMES_INTEGRATION.md
      OPENWEBUI_INTEGRATION.md
      EXTERNAL_TOOLS_POLICY.md
      CODE_AUDIT_POST_PIVOT.md

  domains/
    general/
      domain.md
      rules.md
      knowledge_policy.md
      output_formats.md
      skills/
      workflows/
      templates/

    architecture_fr/
      domain.md
      rules.md
      knowledge_policy.md
      output_formats.md
      skills/
      workflows/
      templates/

    software/
      domain.md
      rules.md
      knowledge_policy.md
      output_formats.md
      skills/
      workflows/
      templates/

  memory/
    session/
    candidates/
    project/
    system/

  knowledge/
    registry.yaml
    source_tiers.md
    freshness_policy.md
    openwebui_collections.md

  hermes/
    context/
      pantheon_context.md
      agents_context.md
      rules_context.md
      memory_context.md
      tools_policy.md
      openwebui_context.md
      architecture_fr_context.md
      software_context.md

  operations/
    install.md
    update.md
    backup.md
    doctor.md
    hermes_lab.md
    openwebui_knowledge.md
    domain_api.md

  platform/
    api/
      pantheon_domain/
```

---

## Domaines canoniques

Pantheon Next est organisé par domaines.

Les domaines initiaux sont :

```text
domains/general
domains/architecture_fr
domains/software
```

### general

Domaine transversal.

Il porte :

- approvals ;
- Evidence Packs ;
- task contracts ;
- source checks ;
- privacy checks ;
- memory candidates ;
- external tool reviews ;
- remediation candidates ;
- context pack exports.

### architecture_fr

Domaine métier principal.

Il porte :

- CCTP ;
- DPGF ;
- CCAP ;
- devis ;
- notices architecturales ;
- permis ;
- ERP / SDIS ;
- PLU ;
- ABF ;
- RE2020 ;
- marchés privés ;
- marchés publics ;
- chantier ;
- situations ;
- avenants ;
- réserves ;
- DOE ;
- réception.

### software

Domaine d’audit technique.

Il porte :

- audit Markdown / code ;
- audit legacy ;
- analyse API ;
- sécurité minimale ;
- dépendances ;
- context exports ;
- conventions ;
- tests ;
- patch candidates.

---

## Knowledge et Memory

Pantheon Next distingue strictement Knowledge et Memory.

```text
Knowledge = documents consultables.
Memory = faits validés.
```

OpenWebUI Knowledge peut contenir des documents, PDF, CCTP, devis, notices, modèles et corpus métier.

Pantheon Memory ne contient que des informations validées.

Structure canonique :

```text
memory/session
memory/candidates
memory/project
memory/system
```

Cycle de promotion :

```text
Session
  ↓
Candidate
  ↓
Evidence Pack
  ↓
Validation C3
  ↓
Project memory ou System memory
```

Règles :

- pas d’auto-promotion ;
- pas de mémoire canonique sans preuve ;
- pas de mémoire canonique sans validation ;
- OpenWebUI history n’est pas une mémoire Pantheon ;
- Hermes local memory n’est pas une mémoire Pantheon ;
- toute promotion mémoire est au minimum C3.

---

## Approvals

Pantheon Next utilise une classification C0-C5.

| Niveau | Définition |
|---|---|
| C0 | lecture, diagnostic, extraction sans mutation |
| C1 | brouillon, suggestion, proposition |
| C2 | action réversible faible risque |
| C3 | changement interne persistant |
| C4 | action externe, contractuelle, financière ou engageante |
| C5 | critique, irréversible, secrets, destruction, permissions fortes |

Règles générales :

- C0-C1 : possible sans validation forte ;
- C2 : possible si réversible et borné ;
- C3 : validation nécessaire ;
- C4 : validation explicite nécessaire ;
- C5 : bloqué par défaut sauf procédure dédiée.

---

## Task Contracts

Un Task Contract est le cadre transmis à Hermes Agent avant exécution.

Il définit :

- l’objectif ;
- le domaine ;
- la criticité ;
- les inputs ;
- les outputs attendus ;
- les outils autorisés ;
- les outils interdits ;
- les agents abstraits concernés ;
- les approvals nécessaires ;
- les preuves attendues ;
- les limites ;
- le fallback autorisé ;
- l’impact mémoire.

Pantheon Next ne lance pas l’exécution.

Pantheon Next formalise le contrat.

Hermes Agent exécute dans ce cadre.

---

## Evidence Packs

Un Evidence Pack est la preuve structurée d’une action ou d’une analyse.

Il doit contenir :

- la tâche ;
- le task contract ;
- les fichiers lus ;
- les sources utilisées ;
- les Knowledge Bases consultées ;
- les outils utilisés ;
- les commandes exécutées ;
- les hypothèses ;
- les limites ;
- les affirmations non prouvées ;
- les veto éventuels ;
- les approvals nécessaires ;
- les outputs ;
- la prochaine action sûre.

Règle centrale :

```text
Une affirmation du modèle n’est pas une preuve.
```

Lineage attendu :

```text
claim → source → chunk/fichier → outil → rôle agent → task contract → evidence pack → validation
```

---

## Outils externes

Tout outil externe est bloqué tant qu’il n’est pas revu.

Règle par défaut :

```text
blocked until reviewed
```

Les outils externes incluent :

- extensions OpenWebUI ;
- plugins Hermes ;
- outils PDF ;
- OCR ;
- conversion documentaire ;
- outils de recherche ;
- MCP servers ;
- outils CLI ;
- APIs distantes ;
- services locaux ;
- dashboards ;
- outils d’automatisation.

Chaque outil doit être classé dans `docs/governance/EXTERNAL_TOOLS_POLICY.md`.

Statuts possibles :

```text
allowed
test
blocked
rejected
watch
```

---

## Intégration OpenWebUI

OpenWebUI doit pointer vers Hermes Gateway, pas vers Pantheon API.

Exemple cible :

```text
OPENAI_API_BASE_URL = http://hermes_agent_gateway:8642/v1
OPENAI_API_KEY = API_SERVER_KEY / HERMES_API_SERVER_KEY
```

Pantheon API n’est pas un backend OpenAI-compatible.

OpenWebUI peut afficher :

- résultats ;
- Evidence Packs ;
- approval requests ;
- sources ;
- limites ;
- actions proposées.

OpenWebUI ne canonise rien.

---

## Intégration Hermes

Hermes Agent Gateway est la frontière d’exécution.

Pantheon fournit à Hermes :

- context packs ;
- task contracts ;
- policies ;
- approval rules ;
- evidence requirements ;
- domain snapshots ;
- memory policy ;
- external tools policy.

Hermes retourne :

- résultat ;
- Evidence Pack ;
- sources ;
- limites ;
- hypothèses ;
- veto ;
- approval requests ;
- patch candidates ;
- memory candidates.

La variable `PANTHEON_CONTEXT_URL` peut exposer un endpoint de contexte Pantheon à Hermes, mais sa présence ne prouve pas que Hermes consomme réellement ce contexte. L’intégration doit être vérifiée par test, trace ou Evidence Pack.

---

## Pantheon API

Pantheon API est une Domain API légère.

Elle expose la gouvernance.

Endpoints cibles :

```text
GET  /health
GET  /runtime/context-pack
GET  /domain/snapshot
GET  /domain/agents
GET  /domain/skills
GET  /domain/workflows
GET  /domain/memory/policy
GET  /domain/knowledge/taxonomy
GET  /domain/approval/policy
POST /domain/approval/classify
GET  /domain/legacy
GET  /domain/tools-policy
GET  /domain/task-contracts
GET  /domain/evidence-schema
```

Endpoints à ne pas créer maintenant :

```text
POST /agents/run
POST /agents/create
POST /runtime/execute
POST /tools/install
POST /plugins/install
POST /memory/promote/auto
POST /scheduler/create
POST /browser/action
```

Ces endpoints feraient glisser Pantheon Next vers un runtime autonome.

---

## Déploiement local recommandé

Structure NAS / Portainer recommandée :

```text
/volume3/docker/
  pantheon-next/
    repo Pantheon-Next

  hermes-agent/
    .hermes/
    config/

  openwebui/
    data/

  postgres/
    openwebui/
    pantheon/

  searxng/
    settings.yml
```

Services logiques :

```text
postgres_openwebui
postgres_pantheon
pantheon_api
hermes_agent_gateway
hermes_dashboard
openwebui
searxng
ollama
```

Règles :

- séparer la base OpenWebUI et la base Pantheon ;
- éviter les images `latest` pour PostgreSQL / pgvector ;
- préférer un tag stable comme `pgvector/pgvector:pg16` ;
- GHCR n’est pas obligatoire en P0 ;
- le build local NAS est acceptable ;
- Hermes Dashboard doit rester local-only, non exposé publiquement sans auth/VPN.

---

## Ce que Pantheon Next ne doit pas devenir

Pantheon Next ne doit pas recréer :

- un runtime agentique autonome ;
- un Execution Engine ;
- un Agent Runtime ;
- un Tool Runtime ;
- un LLM Provider Router ;
- un scheduler ;
- un LangGraph central ;
- une queue agentique obligatoire ;
- un dashboard lourd ;
- une mémoire auto-promue ;
- une self-evolution automatique ;
- un système d’installation libre de plugins.

---

## Roadmap synthétique

### P0 — Gouvernance documentaire

- canoniser `docs/governance/` ;
- stabiliser `ARCHITECTURE.md` ;
- mettre à jour `STATUS.md` ;
- mettre à jour `ROADMAP.md` ;
- créer ou finaliser `APPROVALS.md` ;
- créer ou finaliser `TASK_CONTRACTS.md` ;
- créer ou finaliser `EVIDENCE_PACK.md` ;
- créer ou finaliser `HERMES_INTEGRATION.md` ;
- créer ou finaliser `OPENWEBUI_INTEGRATION.md` ;
- créer ou finaliser `EXTERNAL_TOOLS_POLICY.md` ;
- créer ou finaliser `MEMORY.md` ;
- créer `CODE_AUDIT_POST_PIVOT.md`.

### P1 — Intégration Hermes / OpenWebUI

- vérifier Hermes → Pantheon context pack ;
- créer les exports `hermes/context/*.md` ;
- créer `operations/install.md` ;
- créer `operations/hermes_lab.md` ;
- créer `operations/openwebui_knowledge.md` ;
- définir `hermes_context_consultation` ;
- ajouter SearXNG à la policy ;
- ajouter Hermes Dashboard à la policy local-only ;
- créer `SKILL_RESOLVER.md` ;
- créer `SKILL_LIFECYCLE.md`.

### P2 — Validation et schemas

- créer `WORKFLOW_SCHEMA.md` ;
- créer `MEMORY_EVENT_SCHEMA.md` ;
- créer `KNOWLEDGE_TAXONOMY.md` ;
- créer `operations/doctor.md` ;
- ajouter des checks CI ;
- ajouter les premières skills candidates utiles ;
- ajouter un scoring simple des Evidence Packs.

### P3 — Avancé

- RAG avancé ;
- RRF hybrid search ;
- pgvector / MinIO si besoin réel ;
- Run Graph léger ;
- Graph Memory ;
- multimodal Evidence Packs ;
- Promptfoo / OpenEvals ;
- channels externes ;
- operations view légère.

---

## Règles de contribution

Avant toute modification du dépôt :

1. lire `ai_logs/README.md` et les entrées récentes ;
2. lire `docs/governance/STATUS.md` ;
3. ne pas pousser sur `main` ;
4. travailler sur une branche dédiée ;
5. respecter les Markdown source de vérité ;
6. proposer une mise à jour documentaire avant tout changement de code ambigu ;
7. ajouter une entrée dans `ai_logs/` après intervention.

Si le code contredit les Markdown, les Markdown font foi.

Exception : si le code existant contient une solution techniquement meilleure que la documentation, ne pas le supprimer automatiquement. Proposer d’abord une mise à jour documentaire pour intégrer cette amélioration.

---

## Statut

Pantheon Next est en phase de consolidation post-pivot.

Objectif immédiat :

```text
stabiliser la gouvernance documentaire avant toute extension runtime
```

La priorité n’est pas d’ajouter des agents.

La priorité est de rendre le système gouvernable, traçable, maintenable et aligné avec ses Markdown.
