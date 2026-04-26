# Pantheon OS — Modules

> Document de référence.
> Dans la trajectoire Hermes-backed, les modules Pantheon sont principalement des contrats, overlays, workflows, skills et règles. Hermes exécute les capacités ; Pantheon les définit et les gouverne.

---

# 1. Principe

Pantheon OS ne cherche plus à tout exécuter lui-même.

Le système distingue :

- les modules contractuels Pantheon ;
- les capacités exécutables Hermes ;
- les knowledge collections OpenWebUI ;
- les outils ou scripts d’exploitation ;
- les éventuels restes de l’ancien runtime autonome, à réauditer.

Règle :

```text
Un module Pantheon doit être lisible, versionnable, exportable et gouvernable.
```

---

# 2. Familles de modules

## 2.1 Agents

Les agents sont des rôles cognitifs abstraits.

Emplacement cible :

```text
agents/
  zeus.md
  athena.md
  argos.md
  themis.md
  apollo.md
```

Ils définissent responsabilités, limites, activation, output attendu et règles de sécurité.

Ils ne contiennent pas de logique métier spécifique.

## 2.2 Domain overlays

Les overlays portent le métier.

```text
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
```

Un overlay spécialise les agents abstraits pour un domaine donné.

## 2.3 Skills

Les skills sont les capacités procédurales réutilisables.

Pantheon définit les skills. Hermes les exécute.

```text
skills/
  generic/
  architecture/
    cctp_audit/
      SKILL.md
      manifest.yaml
      examples.md
      tests.md
  software/
```

Une skill doit indiquer : objectif, inputs, outputs, agents mobilisés, sources autorisées, risques, approval requis, exemples, tests et état.

États : draft, candidate, active, archived.

## 2.4 Workflows

Les workflows définissent les séquences de travail.

```text
workflows/
  generic/
  architecture/
    cctp_review.yaml
    dpgf_review.yaml
  software/
    repo_consistency_audit.yaml
```

Un workflow peut être exécuté par Hermes comme procédure. LangGraph reste une option future pour formaliser les workflows complexes si Hermes ne suffit plus.

## 2.5 Knowledge policy

Pantheon ne stocke pas nécessairement les documents lourds. Il définit leur stratégie.

```text
knowledge/
  openwebui_collections.md
  source_policy.md
  document_taxonomy.md
```

OpenWebUI peut porter les collections documentaires. Pantheon définit les noms, usages, statuts, règles de fiabilité et exclusions.

## 2.6 Memory

Pantheon porte la mémoire validée.

```text
memory/
  project/
    facts.md
    decisions.md
    risks.md
  agency/
    patterns.md
    clauses.md
    preferences.md
  candidates/
    pending_facts.md
    pending_skills.md
    pending_rules.md
```

Hermes peut garder une mémoire opérationnelle. Celle-ci ne devient pas vérité Pantheon sans promotion explicite.

## 2.7 Hermes integration

Module d’intégration vers Hermes Agent.

```text
hermes/
  context/
    pantheon_context.md
    agents_context.md
    rules_context.md
    domain_architecture.md
  exports/
    skills/
    prompts/
    workflows/
```

Objectifs : fournir à Hermes les contextes et skills validés, sans redéfinition divergente.

## 2.8 Operations

Modules d’exploitation documentaire et scripts éventuels :

```text
operations/
  install.md
  update.md
  backup.md
  doctor.md
```

Ces fichiers décrivent les procédures NAS, Portainer, OpenWebUI, Hermes Lab, Ollama LAN, versions et backups.

---

# 3. Skill contract

Chaque skill doit contenir au minimum :

```text
id
name
domain
status
purpose
inputs
outputs
agents
knowledge_sources
approval_required_if
risks
failure_modes
examples
tests
```

`manifest.yaml` doit rester machine-readable. `SKILL.md` doit rester lisible par humain et par Hermes.

Exemple minimal :

```yaml
id: cctp_audit
domain: architecture
status: candidate
agents:
  - ATHENA
  - ARGOS
  - THEMIS
  - APOLLO
approval_required_if:
  - modifies_source_document
  - sends_external_message
  - promotes_memory
outputs:
  - diagnostic
  - inconsistency_table
  - risks
  - corrections
```

---

# 4. Workflow contract

Chaque workflow doit contenir :

```text
id
domain
purpose
inputs
steps
agents
skills
knowledge_sources
outputs
approval_points
memory_targets
fallback
```

Un workflow ne doit pas être un prompt long déguisé. Il doit être une procédure structurée.

---

# 5. Domain overlay contract

Un overlay doit définir :

- périmètre ;
- règles métier ;
- sources de référence ;
- workflows actifs ;
- skills actives ;
- templates ;
- output formats ;
- règles d’approbation ;
- règles de mémoire ;
- exclusions.

Le domaine ne doit pas modifier les agents abstraits. Il les spécialise contextuellement.

---

# 6. Memory contract

Toute mémoire Pantheon doit rester :

- sourcée ;
- datée ;
- liée à un projet, une agence, une règle ou une skill ;
- révisable ;
- rétractable ;
- différenciée entre candidate et active.

Hermes peut proposer :

- candidate fact ;
- candidate skill ;
- candidate rule ;
- candidate workflow improvement.

Pantheon valide ou rejette.

---

# 7. Approval contract

Une action doit être classée avant exécution.

Actions sans approval forte :

- diagnostic ;
- lecture ;
- extraction ;
- brouillon ;
- proposition.

Actions avec approval :

- modification de fichier ;
- envoi email ;
- suppression ;
- commande shell hors allowlist ;
- promotion mémoire ;
- activation skill candidate ;
- action web à effet de bord ;
- accès secret, volume sensible ou Docker socket.

Au départ, cette discipline peut être documentaire et opératoire. Un module logiciel peut être conservé ou réorienté si nécessaire après audit.

---

# 8. OpenWebUI collections

Collections recommandées :

```text
pantheon_governance
architecture_cctp_models
architecture_dpgf_models
architecture_contract_clauses
architecture_plu
architecture_sdis_erp
architecture_notices
software_repo_docs
```

Chaque collection doit avoir :

- objectif ;
- types de documents ;
- statut ;
- règle de mise à jour ;
- sources obsolètes ;
- niveau de fiabilité ;
- usage autorisé.

---

# 9. Modules hérités de l’ancien runtime

Le dépôt contient encore des modules et fichiers liés à l’ancienne trajectoire autonome :

- FastAPI apps ;
- manifests runtime ;
- workflow loader ;
- approval API ;
- Installer UI ;
- tests contractuels ;
- registries.

Statut : à réauditer.

Décisions possibles après audit :

- conserver comme utilitaire ;
- réorienter vers Hermes integration ;
- archiver ;
- supprimer ;
- documenter comme option avancée.

Aucun code ne doit être supprimé avant clarification documentaire et audit de cohérence.

---

# 10. Anti-patterns

À éviter :

- module qui réimplémente Hermes sans gain ;
- skill active non validée ;
- agent métier figé ;
- workflow caché dans un prompt ;
- knowledge OpenWebUI qui remplace les Markdown ;
- mémoire Hermes promue automatiquement ;
- plusieurs sources de vérité pour les agents ;
- duplication d’un scheduler, gateway ou terminal backend sans besoin clair ;
- accès Docker socket ou secrets sans policy.

---

# 11. Règle finale

Un module Pantheon est bon s’il rend le système plus clair, plus gouverné, plus portable ou plus réutilisable.

Un module est mauvais s’il recrée une capacité déjà fournie par Hermes, ajoute une source de vérité concurrente ou masque des effets de bord derrière du prompt engineering.
