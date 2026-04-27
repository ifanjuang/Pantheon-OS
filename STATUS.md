# Pantheon OS — Project Status

> Source de vérité sur l’état actuel du projet après pivot architectural.
> Les fichiers Markdown de référence pilotent le développement : `README.md`, `ARCHITECTURE.md`, `MODULES.md`, `AGENTS.md`, `MEMORY.md`, `ROADMAP.md`, `STATUS.md`.

Dernière mise à jour : 2026-04-27

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
| Pivot Hermes-backed | ✅ Fait | Direction validée : Pantheon Domain Layer + Hermes + OpenWebUI |
| README produit | ✅ À mettre / aligner | README doit rester vision/compréhension, non duplicatif avec `MODULES.md` |
| AGENTS.md | 🔄 À mettre à jour | Panthéon étendu validé conceptuellement ; agents abstraits, non métier |
| MODULES.md | 🔄 À mettre à jour | Doit détailler modules réels : agents, skills, workflows, domains, memory, knowledge, hermes, operations |
| MEMORY.md | ⬜ À créer | Nouveau fichier de référence : session / candidates / project / system |
| ARCHITECTURE.md | 🔄 À aligner | Doit décrire architecture réelle : OpenWebUI / Pantheon / Hermes + legacy |
| Branche code post-pivot | ✅ Créée | `work/chatgpt/hermes-code-rewrite` |
| PR draft | ✅ Ouverte | PR #50 : `WIP: rewrite API around Hermes-backed domain layer` |
| Nouvelle API Domain Layer | ✅ Première passe | `platform/api/pantheon_domain/*` + `platform/api/main.py` |
| Ancien runtime autonome | ⚠️ Legacy non supprimé | Conservé dans le repo, mais plus booté par défaut dans la nouvelle entrée API |
| Tests Domain Layer | 🔄 Écrits, non exécutés ici | `tests/test_domain_layer_api.py` ajouté, exécution locale/CI à faire |
| Hermes Agent | ⬜ Non installé | À tester plus tard en Hermes Lab isolé |
| OpenWebUI Knowledge Strategy | ⬜ À faire | Collections et source policy à créer |
| Skills métier | 🔄 À formaliser | Première priorité : `quote_vs_cctp_analysis` / `quote_vs_cctp_review` |
| Mémoire validée Pantheon | 🔄 Modèle clarifié | Quatre niveaux actés : session, candidates, project, system |
| Installer UI existante | ⚠️ Legacy à classer | À réorienter vers Hermes Lab / NAS preflight si conservée |

---

# 3. Cohérence documentation / code

## 3.1 Documentation

Statut : 🔄 En cours de réalignement fin.

Décisions déjà actées dans la conversation :

- README doit être orienté produit/vision, sans duplication détaillée de `MODULES.md`.
- `AGENTS.md` doit intégrer le panthéon étendu.
- `MODULES.md` doit détailler le découpage fonctionnel réel.
- `MEMORY.md` doit être créé pour formaliser session / candidates / project / system.
- `ARCHITECTURE.md` doit rester technique et décrire les responsabilités réelles.
- Les agents restent abstraits ; le métier est porté par skills, workflows, knowledge et memory.

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

# 4. Panthéon retenu

Statut : 🔄 À inscrire dans `AGENTS.md`.

Agents abstraits retenus :

- ZEUS : orchestration, arbitrage, décision finale ;
- ATHENA : planification, structuration, stratégie ;
- ARGOS : extraction factuelle, données, contradictions ;
- THEMIS : règles, responsabilité, validation, veto ;
- APOLLO : validation finale, qualité, cohérence ;
- PROMETHEUS : contradiction, stress-test, angles morts ;
- HEPHAESTUS : technique, faisabilité, robustesse ;
- HESTIA : mémoire projet ;
- MNEMOSYNE : mémoire système ;
- IRIS : communication, rédaction, ton ;
- HERMES : interface vers runtime ;
- CHRONOS : planning, délais, dépendances ;
- HERA : supervision, amélioration continue ;
- HECATE : incertitude, manque d’informations ;
- ARES : urgence, mode dégradé ;
- DIONYSOS : créativité, contenu, storytelling ;
- DEMETER : budget, quantités, ressources ;
- POSEIDON : site, environnement, réseaux, eaux ;
- DAEDALUS : conception système, workflows, architecture.

Règle : aucun agent métier. Le métier est injecté par skills, workflows, domains, knowledge et memory.

---

# 5. Modèle mémoire retenu

Statut : 🔄 À formaliser dans `MEMORY.md`.

Quatre niveaux :

```text
session    = réflexion temporaire
candidates = propositions persistées non validées
project    = contexte projet validé
system     = vérité globale validée
```

Cycle :

```text
SESSION → CANDIDATES → validation THEMIS → PROJECT ou SYSTEM
```

Agents mémoire :

- ZEUS / ATHENA : mémoire session ;
- ARGOS : alimentation candidates ;
- THEMIS : validation ;
- HESTIA : mémoire project ;
- MNEMOSYNE : mémoire system.

---

# 6. Premier use case métier prioritaire

Statut : ✅ Priorisé conceptuellement, ⬜ fichiers à créer.

Use case : analyse de devis vis-à-vis d’un CCTP.

Skill cible :

```text
quote_vs_cctp_analysis
```

Workflow cible :

```text
quote_vs_cctp_review
```

Agents mobilisés :

- ATHENA : méthode ;
- ARGOS : extraction CCTP / devis ;
- HEPHAESTUS : cohérence technique ;
- DEMETER : quantités / économie ;
- THEMIS : périmètre, responsabilité, validation ;
- PROMETHEUS : pièges et contradictions ;
- APOLLO : validation finale ;
- IRIS : message client/entreprise si nécessaire ;
- ZEUS : arbitrage.

---

# 7. Tests

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

# 8. Chantiers immédiats

## P0 — Mettre à jour les Markdown structurants

À faire :

- remplacer `README.md` par une version produit/vision ;
- remplacer `AGENTS.md` par la version panthéon étendu ;
- remplacer `MODULES.md` par la version découpage fonctionnel ;
- créer `MEMORY.md` ;
- réaligner `ARCHITECTURE.md` ;
- mettre `ROADMAP.md` en cohérence si nécessaire.

## P0 — Tester la première couche Domain Layer

À faire :

- lancer `pytest tests/test_domain_layer_api.py` ;
- lancer l’API localement ;
- vérifier `/health` ;
- vérifier `/domain/snapshot` ;
- vérifier `/domain/approval/classify` ;
- corriger imports ou dépendances si nécessaire.

## P0/P1 — Créer les dossiers contractuels Markdown

À créer :

```text
agents/
domains/architecture/
skills/
workflows/
memory/session/
memory/candidates/
memory/project/
memory/system/
knowledge/
hermes/context/
operations/
```

## P1 — Formaliser le premier use case réel

À créer :

```text
skills/architecture/quote_vs_cctp_analysis/SKILL.md
workflows/architecture/quote_vs_cctp_review.yaml
domains/architecture/overlay.md
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
- distinguer documents projet, système, réglementaire, modèle, obsolète.

---

# 9. Chantiers ralentis ou dépriorisés

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

# 10. Points de vigilance

- Ne pas installer Hermes Agent globalement sur le NAS sans isolation.
- Ne pas donner à Hermes accès aux volumes Pantheon ou au Docker socket au début.
- Ne pas laisser OpenWebUI devenir source officielle des agents ou de la mémoire validée.
- Ne pas promouvoir automatiquement une mémoire Hermes dans Pantheon.
- Ne pas activer une skill générée par Hermes sans validation.
- Ne pas supprimer l’ancien code avant audit post-pivot.
- Ne pas merger la PR #50 sans tests locaux.
- Ne pas laisser `README.md` dupliquer `MODULES.md`.

---

# 11. Prochaine action recommandée

1. Mettre à jour `README.md`, `AGENTS.md`, `MODULES.md`, `ARCHITECTURE.md`.
2. Créer `MEMORY.md`.
3. Lancer `pytest tests/test_domain_layer_api.py`.
4. Créer le premier vrai use case : `quote_vs_cctp_analysis` + `quote_vs_cctp_review`.
5. Auditer le legacy avant suppression ou archivage.

---

# 12. Résumé final

Fiable maintenant : la direction documentaire, la première API Domain Layer et la séparation conceptuelle agents / skills / workflows / memory / knowledge.

Non fiable encore : exécution réelle des tests, compatibilité locale/NAS et alignement complet des Markdown modifiés manuellement dans la conversation.

Prochaine étape logique : écrire les Markdown structurants dans le repo, puis créer le premier workflow réel devis vs CCTP.
