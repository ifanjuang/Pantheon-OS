# ROADMAP — Pantheon OS

> Feuille de route post-pivot.
> Pantheon OS devient un Domain Operating Layer Hermes-backed : Pantheon définit et gouverne, Hermes Agent exécute, OpenWebUI expose l’interface et les knowledge bases.

---

# 1. Vision

Pantheon OS n’est plus une tentative de reconstruire un runtime agentique complet.

La trajectoire retenue :

```text
OpenWebUI = interface + knowledge documentaire
Hermes Agent = runtime agentique + skills + tools + scheduler + doctor + gateway + mémoire opérationnelle
Pantheon OS = agents abstraits + domain overlays + workflows + skills contracts + mémoire validée + gouvernance
```

Objectif : construire une couche métier portable, lisible, gouvernée et exploitable par Hermes Agent et OpenWebUI.

---

# 2. Principes de préservation

## 2.1 Documentation source de vérité

Les fichiers Markdown de référence pilotent le développement :

- `README.md`
- `ARCHITECTURE.md`
- `AGENTS.md`
- `MODULES.md`
- `ROADMAP.md`
- `STATUS.md`

## 2.2 Agents abstraits

Les agents restent neutres métier. Le métier est injecté par overlays, workflows, skills et knowledge.

## 2.3 Hermes-backed execution

Hermes Agent fournit l’exécution agentique et procédurale. Pantheon ne réimplémente pas scheduler, gateway, terminal backends, doctor, runtime de skills ou mémoire opérationnelle sans gain clair.

## 2.4 OpenWebUI knowledge

OpenWebUI porte les knowledge collections documentaires. Pantheon définit les règles de classement, fiabilité, usage et obsolescence.

## 2.5 Mémoire validée

Hermes peut apprendre opérationnellement. Pantheon valide durablement.

## 2.6 Approval discipline

Toute action sensible reste soumise à validation : modification fichier, email, suppression, shell hors allowlist, promotion mémoire, activation skill, action web à effet de bord, accès secrets ou volumes sensibles.

---

# 3. Architecture cible

```text
Pantheon-OS/
  README.md
  STATUS.md
  ROADMAP.md
  ARCHITECTURE.md
  AGENTS.md
  MODULES.md
  AI_LOG.md
  EXTERNAL_WATCHLIST.md

  agents/
    zeus.md
    athena.md
    argos.md
    themis.md
    apollo.md
    prometheus.md
    hestia.md
    mnemosyne.md
    iris.md
    hephaestus.md

  domains/
    architecture/
      overlay.md
      rules.md
      knowledge_policy.md
      output_formats.md
      workflows/
      skills/
      templates/
    software/
    legal/
    consulting/

  skills/
    generic/
    architecture/
    software/

  workflows/
    generic/
    architecture/
    software/

  memory/
    project/
    agency/
    candidates/

  knowledge/
    openwebui_collections.md
    source_policy.md
    document_taxonomy.md

  hermes/
    context/
    exports/

  operations/
    install.md
    update.md
    backup.md
    doctor.md
```

---

# 4. Phases d’implémentation

## Phase 0 — Audit post-pivot

Objectif : classer l’ancien code autonome.

Actions :

- auditer `platform/`, `core/`, `modules/`, `alembic/`, `scripts/` ;
- identifier ce qui reste utile pour Hermes-backed Pantheon ;
- marquer chaque composant : conserver, réorienter, archiver, supprimer plus tard, à vérifier ;
- ne supprimer aucun code avant validation documentaire.

Livrable : `STATUS.md` mis à jour + tableau d’incohérences code/docs.

Priorité : P0.

## Phase 1 — Recentrage documentaire

Objectif : transformer Pantheon en référentiel contractuel.

Actions :

- créer `agents/*.md` pour les agents abstraits principaux ;
- créer `domains/architecture/overlay.md` ;
- créer `knowledge/openwebui_collections.md` ;
- créer `knowledge/source_policy.md` ;
- créer `memory/project`, `memory/agency`, `memory/candidates` ;
- créer `hermes/context/pantheon_context.md` ;
- créer `hermes/context/agents_context.md` ;
- créer `hermes/context/rules_context.md`.

Priorité : P0/P1.

## Phase 2 — Hermes Lab isolé

Objectif : tester Hermes Agent sans risque sur le NAS.

Actions :

- installer Hermes dans un environnement isolé ;
- ne pas lui donner accès aux volumes Pantheon ;
- ne pas lui donner accès au Docker socket ;
- tester CLI, doctor, mémoire, skills ;
- tester accès Ollama LAN ;
- documenter limites, secrets, permissions et commandes autorisées.

Livrable : `operations/install.md` et `operations/doctor.md`.

Priorité : P1.

## Phase 3 — Skills métier Pantheon

Objectif : créer les premières skills contractuelles.

Skills prioritaires :

- `skills/architecture/cctp_audit/` ;
- `skills/architecture/dpgf_check/` ;
- `skills/architecture/notice_architecturale/` ;
- `skills/software/repo_md_audit/` ;
- `skills/generic/source_check/` ;
- `skills/generic/client_message/`.

Chaque skill doit avoir : `SKILL.md`, `manifest.yaml`, `examples.md`, `tests.md` si utile.

Priorité : P1.

## Phase 4 — Workflows métier

Objectif : formaliser les procédures importantes.

Workflows prioritaires :

- `workflows/architecture/cctp_review.yaml` ;
- `workflows/architecture/dpgf_review.yaml` ;
- `workflows/architecture/sdis_notice_review.yaml` ;
- `workflows/software/repo_consistency_audit.yaml` ;
- `workflows/generic/memory_promotion.yaml` ;
- `workflows/generic/skill_promotion.yaml`.

Priorité : P1/P2.

## Phase 5 — OpenWebUI Knowledge Strategy

Objectif : organiser les collections documentaires.

Actions :

- définir collections ;
- définir politique de nommage ;
- distinguer documents projet, agence, réglementaire, modèle, obsolète ;
- définir mise à jour et fiabilité ;
- relier knowledge collections aux skills et workflows.

Collections initiales :

- `pantheon_governance` ;
- `architecture_cctp_models` ;
- `architecture_dpgf_models` ;
- `architecture_contract_clauses` ;
- `architecture_plu` ;
- `architecture_sdis_erp` ;
- `architecture_notices` ;
- `software_repo_docs`.

Priorité : P1/P2.

## Phase 6 — Mémoire validée

Objectif : distinguer mémoire vivante Hermes et mémoire fiable Pantheon.

Actions :

- créer fichiers mémoire projet/agence/candidates ;
- définir règle de promotion ;
- définir règle de rétractation ;
- définir candidate facts, candidate skills, candidate rules ;
- définir revue humaine minimale.

Priorité : P2.

## Phase 7 — Hermes Integration Layer

Objectif : faire consommer Pantheon par Hermes proprement.

Actions :

- exporter agents context ;
- exporter rules context ;
- exporter domain context ;
- exporter skills candidates / actives ;
- définir sync manuel ou scripté ;
- empêcher divergences Hermes/Pantheon.

Priorité : P2.

## Phase 8 — Exploitation NAS et versions

Objectif : installer et maintenir sans casser Portainer/OpenWebUI/PostgreSQL existants.

Actions :

- documenter preflight ;
- documenter détection OpenWebUI existant ;
- documenter détection PostgreSQL existant ;
- documenter Ollama LAN ;
- définir backup avant modification ;
- définir check versions ;
- définir update dry-run ;
- bannir les updates automatiques sans validation.

Priorité : P2.

## Phase 9 — Options avancées

À traiter plus tard seulement si besoin :

- LangGraph runner ;
- RAG dédié PostgreSQL + pgvector ;
- Evaluation Harness RAG ;
- Browser Tool gouverné ;
- NiceGUI console ;
- n8n webhooks ;
- Local Tools Hub ;
- MDA mémoire associative.

Priorité : P3/P4.

---

# 5. Chantiers à ralentir ou abandonner

À ne plus prioriser comme cœur Pantheon :

- runtime agentique FastAPI complet ;
- scheduler maison ;
- gateway messagerie maison ;
- terminal backend maison ;
- runtime skills maison ;
- dashboard lourd ;
- marketplace interne ;
- Browser Tool avant sécurité ;
- microservices ;
- remplacement d’Hermes par un framework externe.

Ces éléments peuvent devenir options, outils internes ou artefacts à archiver après audit.

---

# 6. External inspiration

Référence majeure : `NousResearch/hermes-agent`.

À retenir :

- skills ;
- doctor ;
- setup ;
- mémoire opérationnelle ;
- command approval ;
- cron scheduler ;
- gateways ;
- terminal backends ;
- model/provider switching.

À ne pas faire :

- installation globale non isolée sur NAS ;
- Hermes comme second runtime non gouverné ;
- auto-activation de skills ;
- promotion mémoire sans validation ;
- accès volumes/secrets/Docker socket sans policy.

Les autres références restent dans `EXTERNAL_WATCHLIST.md`.

---

# 7. Prochaine action

Ordre immédiat :

1. Finaliser les Markdown post-pivot.
2. Mettre `STATUS.md` à jour : pivot acté, code non aligné à réauditer.
3. Créer les dossiers contractuels minimaux.
4. Installer Hermes en lab isolé.
5. Définir les premières skills architecture.
6. Définir la stratégie OpenWebUI Knowledge.
7. Auditer l’ancien code et décider quoi conserver.

---

# 8. Résultat cible

Pantheon OS doit devenir une couche métier contractuelle, portable et maintenable, qui transforme Hermes Agent et OpenWebUI en assistant professionnel gouverné.

Sa valeur n’est pas de tout exécuter. Sa valeur est de définir les règles, rôles, workflows, skills, sources et mémoires qui rendent l’exécution fiable.
