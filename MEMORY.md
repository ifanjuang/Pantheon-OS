# MEMORY — Pantheon OS

> Document de référence sur la mémoire Pantheon.
> La mémoire est un système de sélection, validation et promotion. Ce n’est pas une archive brute.

---

# 1. Principe

La mémoire Pantheon doit rester compacte, utile et gouvernée.

Elle ne doit pas devenir :

- un journal complet ;
- une base documentaire ;
- une copie des conversations ;
- une archive projet ;
- un stockage automatique de tout ce que produit Hermes ou OpenWebUI.

Règle :

```text
moins de mémoire, mieux validée
```

---

# 2. Les quatre niveaux

Pantheon distingue quatre niveaux :

```text
session
candidates
project
system
```

---

## 2.1 Session

Mémoire temporaire.

Usage :

- contexte immédiat ;
- hypothèses de travail ;
- cadrage d’une demande ;
- état intermédiaire d’un raisonnement ;
- éléments utiles uniquement pendant l’échange.

Règles :

- non souveraine ;
- non persistée comme vérité ;
- supprimable ;
- ne doit pas être utilisée comme source durable.

---

## 2.2 Candidates

Mémoire persistée mais non validée.

Usage :

- fait potentiel ;
- règle proposée ;
- pattern détecté ;
- amélioration de skill ;
- amélioration de workflow ;
- source externe à évaluer ;
- proposition de mémoire project ou system.

Règles :

- jamais considérée comme fiable ;
- toujours marquée candidate ;
- doit être reviewée avant promotion ;
- peut être acceptée, corrigée, rejetée ou archivée.

---

## 2.3 Project

Mémoire validée propre à un projet ou à un dossier.

Usage :

- décision validée ;
- contrainte projet ;
- hypothèse confirmée ;
- risque identifié ;
- préférence spécifique à un dossier ;
- continuité utile sur un périmètre limité.

Règles :

- non généralisable automatiquement ;
- ne devient pas system sans validation distincte ;
- doit rester attachée à un périmètre explicite ;
- ne doit pas contenir de données réelles dans le repo sauf espace projet explicitement autorisé.

---

## 2.4 System

Mémoire globale validée.

Usage :

- règle stable ;
- méthode réutilisable ;
- pattern transversal ;
- standard de rédaction ;
- convention de nommage ;
- règle de sécurité ;
- règle de gouvernance ;
- principe de workflow ou skill.

Règles :

- validation obligatoire ;
- anonymisation obligatoire ;
- impact transversal assumé ;
- modification traçable ;
- rollback possible via Git.

---

# 3. Cycle de promotion

Cycle officiel :

```text
SESSION → CANDIDATES → REVIEW → PROJECT ou SYSTEM
```

Aucune promotion automatique.

Toute promotion doit indiquer :

- origine ;
- utilité ;
- niveau cible ;
- risque ;
- justification ;
- validation ;
- privacy check.

---

# 4. Triage avant écriture

Toute demande de modification doit être classée avant action.

Catégories :

```text
situation_specific
project_memory
system_memory
skill_update
workflow_update
new_capability
policy_update
no_memory
```

Règles :

- une situation ponctuelle ne devient pas règle système ;
- une préférence projet ne devient pas convention globale ;
- une amélioration de méthode va dans la skill ou le workflow concerné ;
- une capacité absente passe par création candidate ;
- une règle durable passe par system memory ou policy.

---

# 5. Interaction avec Hermes

Hermes peut avoir une mémoire opérationnelle.

Cette mémoire est utile pour l’exécution, mais elle n’est pas souveraine.

Règle :

```text
Hermes peut proposer.
Pantheon valide.
```

Hermes ne peut pas :

- promouvoir seul une mémoire durable ;
- modifier system memory ;
- activer une skill candidate ;
- généraliser un cas projet ;
- inscrire une donnée réelle dans le repo.

---

# 6. Interaction avec OpenWebUI

OpenWebUI porte la knowledge documentaire.

Pantheon ne doit pas transformer `MEMORY.md` en knowledge base.

Différence :

```text
Knowledge = documents, sources, corpus, références
Memory    = décisions, règles, méthodes, patterns validés
```

Les PDF, CCTP, devis, notices, PLU, normes, guides et documents lourds restent dans une couche documentaire dédiée, pas dans `MEMORY.md`.

---

# 7. Privacy by default

Règle absolue :

```text
Aucune information réelle identifiable dans la mémoire système du repo.
```

Interdits dans le repo :

- noms de clients ;
- noms de personnes ;
- noms d’entreprises ;
- adresses ;
- projets réels ;
- chantiers réels ;
- dossiers réels ;
- extraits identifiables de conversations privées.

Les exemples doivent être :

- fictifs ;
- neutres ;
- non traçables ;
- anonymisés ;
- non issus directement des discussions.

---

# 8. Candidate memory

Les candidates servent de sas.

Elles peuvent concerner :

- `pending_facts` ;
- `pending_rules` ;
- `pending_skills` ;
- `pending_workflows` ;
- `pending_policies` ;
- `pending_templates` ;
- `rejected`.

Une candidate doit toujours préciser :

```text
status
source_type
target_level
reason
privacy_check
review_required
```

---

# 9. Skills, updates et XP

Un bon résultat ne modifie pas directement une skill.

Cycle :

```text
résultat utile → UPDATES.md → review → optimisation → validation → SKILL.md
```

XP possible uniquement si :

- amélioration réelle ;
- simplification ;
- blocage détecté ;
- blocage résolu ;
- garde-fou ajouté ;
- sortie plus fiable.

Règles :

- pas d’XP automatique ;
- pas de level-up automatique ;
- changement de level uniquement après review ;
- privacy check obligatoire ;
- rollback via Git.

---

# 10. Mémoire et création à la volée

Si une skill ou un workflow n’existe pas :

```text
1. vérifier l’existant Pantheon ;
2. vérifier les skills Hermes built-in / optional ;
3. vérifier les noms proches ;
4. proposer une candidate ;
5. valider ;
6. créer seulement après accord.
```

La proposition reste candidate tant qu’elle n’est pas acceptée.

---

# 11. Anti-patterns

À éviter :

- stocker toute conversation ;
- transformer un cas ponctuel en règle ;
- promouvoir une mémoire Hermes sans validation ;
- utiliser OpenWebUI comme mémoire validée ;
- mélanger knowledge et memory ;
- écrire des données réelles dans le repo ;
- laisser une skill s’auto-améliorer ;
- multiplier les règles sans preuve d’usage.

---

# 12. Règle finale

Une bonne mémoire Pantheon est :

```text
compacte
sélective
validée
anonymisée
réversible
utile à l’action
```

Une mauvaise mémoire est :

```text
longue
brute
contextuelle
non validée
identifiable
impossible à maintenir
```
