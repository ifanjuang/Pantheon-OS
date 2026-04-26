# Pantheon OS — External Watchlist

Ce fichier suit les dépôts, guides et projets externes utilisés comme veille ou inspiration.

Règle : ces dépôts ne sont pas des dépendances runtime de Pantheon OS sauf décision explicite. Toute idée externe doit d’abord être comparée aux Markdown de référence avant modification du code.

---

## Table de veille

| Source | Usage Pantheon OS | Statut | Dernier audit | Décision |
|---|---|---|---|---|
| `smarzola/hermes-local-memory` | Doctrine mémoire locale | Veille active | 2026-04-26 | Retenir mémoire multi-couches, candidate facts, active facts, cards, context preview, dry-run ; pas de dépendance runtime |
| `mage0535/hermes-memory-installer` | Installation mémoire locale / bootstrap mémoire | Plus tard | 2026-04-26 | Retenir installation mémoire, injection mémoire, auto-mount skills, archivage local ; rejeter SQLite FTS5 comme source principale et promotion non validée |
| `suryamr2002/langgraph-approval-hub` | Approval Gate / HITL | Veille active | 2026-04-26 | Retenir statuts approval, pending queue, decision note, expiration, escalation, audit log ; pas de dashboard externe obligatoire |
| `sunny84patel/RAG-Evaluation` | Evaluation Harness RAG | Plus tard | 2026-04-26 | Retenir génération questions, comparaison configs RAG, métriques retrieval/source/faithfulness/latency ; rejeter Streamlit et Qdrant in-memory comme base |
| `HaroldConley/chunk-norris` | Sélection / comparaison de stratégies de chunking RAG | Veille active | 2026-04-26 | Retenir l’idée de tester plusieurs chunkers par corpus/document, questions générées et choix de stratégie ; à intégrer après Evaluation Harness, sans dépendance directe tant que licence/qualité non auditées |
| `browser-use/browser-harness` | Browser Tool gouverné | Plus tard | 2026-04-26 | À reporter après Approval Gate, PolicyGate et Observability ; retenir screenshots before/after et action traces |
| `elizaOS/eliza` | Actions / providers / evaluators / services | Veille | 2026-04-26 | Retenir vocabulaire runtime ; rejeter remplacement du runtime Pantheon |
| `crewAIInc/crewAI` | Task Contract / workflow crew pattern | Veille active | 2026-04-26 | Retenir Task, expected_output, Flow/Crew separation ; runtime rejeté |
| `agentscope-ai/agentscope` | Multi-agent runtime avancé | Veille | 2026-04-26 | Intéressant pour observability, HITL, planning, MCP/A2A ; non prioritaire, ne pas empiler un second runtime |
| `FlowiseAI/Flowise` | Visual workflow builder | Plus tard | 2026-04-26 | À utiliser seulement comme labo visuel optionnel ; ne doit pas devenir source de vérité |
| `langflow-ai/langflow` | Visual Prototype Lab Python | Plus tard | 2026-04-26 | Préférable à Flowise pour Pantheon car Python/custom components ; service Docker optionnel lab, pas runtime officiel |
| `langgenius/dify` | Plateforme RAG / agents / workflows / observability | Veille | 2026-04-26 | Référence UX/produit intéressante ; trop concurrent du cœur Pantheon pour intégration directe |
| `n8n-io/n8n` | Automatisation externe / webhooks | Plus tard | 2026-04-26 | Utile comme connecteur périphérique : n8n déclenche, Pantheon décide ; ne pas exposer publiquement |
| `iib0011/omni-tools` | Local Tools Hub / outils fichiers locaux | Plus tard | 2026-04-26 | Retenir outils self-hosted client-side PDF/image/CSV/JSON ; pas prioritaire avant mémoire/RAG/Approval |
| `Start9Labs/start-os` | Self-hosting OS / service lifecycle | Veille active | 2026-04-26 | Retenir lifecycle services, update consent, health, backup scope, registry ; rejeter OS complet et `.s9pk` |
| `commonmark.org` | Standard Markdown | Documentation standard | 2026-04-26 | Adopter convention Markdown CommonMark-compatible + tables GitHub ; pas de syntaxe propriétaire |
| `agentsmd/agents.md` | Convention agents | Veille active | 2026-04-26 | À intégrer comme convention documentaire agents/coding |
| `agentskills/agentskills` | Skill contract | Veille | 2026-04-26 | À intégrer plus tard pour formaliser les skills réutilisables |
| `canvascomputing/prompting` | Méthode de conception de prompts / systèmes prompts | À vérifier | 2026-04-26 | Référence utile pour structurer prompts, rôles, contraintes, exemples et évaluation ; audit fichier par fichier encore à faire |
| `caliber-ai-org/ai-setup` | AI setup, context rot, scoring config IA | Veille active | 2026-04-26 | Retenir audit local des configs IA, score de fraîcheur, génération/refresh de fichiers agents, sync multi-outils ; ne pas installer automatiquement sans validation |
| `NirDiamant/GenAI_Agents` | Patterns agents / RAG / memory | Veille | 2026-04-26 | Inspiration seulement, pas d’import massif |
| `NirDiamant/agents-towards-production` | Production hardening agents | Veille active | 2026-04-26 | Retenir checklist production : sécurité, evaluation, deployment, observability, RAG, memory |
| `e2b-dev/awesome-ai-agents` | Catalogue | Veille | 2026-04-26 | Pas d’import massif ; veille seulement |
| `ashishpatel26/500-AI-Agents-Projects` | Catalogue massif | Veille | 2026-04-26 | Pas d’import massif ; inspiration ponctuelle uniquement |
| `contains-studio/agents` | Catalogue agents | Veille | 2026-04-26 | Pas d’import massif |
| `msitarzewski/agency-agents` | Catalogue agents / agency patterns | Veille | 2026-04-26 | Inspiration seulement |
| `hermesguide.xyz` | Guide Hermes | Veille | 2026-04-26 | À utiliser pour patterns, pas comme source unique |

---

## Synthèse par chantier Pantheon

| Chantier | Sources utiles | Décision |
|---|---|---|
| Governance documentaire | CommonMark, agents.md, AI_LOG | À intégrer maintenant |
| Prompt systems | canvascomputing/prompting, GitHub prompt files, caliber-ai-org/ai-setup | À intégrer comme méthode documentaire et qualité prompts |
| AI coding setup | caliber-ai-org/ai-setup, agents.md, AI_LOG | À intégrer plus tard comme audit/refresh contrôlé, pas comme génération automatique non relue |
| Runtime contracts | CrewAI, ElizaOS, agentskills | À intégrer progressivement |
| Approval / Safety | langgraph-approval-hub | À finaliser avant actions sensibles |
| Memory | hermes-local-memory, hermes-memory-installer | À documenter maintenant, implémenter après stabilisation |
| RAG Quality | RAG-Evaluation, ChunkNorris, agents-towards-production | À intégrer après Approval Gate minimal ; évaluer d’abord le chunking sur corpus Pantheon |
| Self-hosting | StartOS, Installer UI interne | À intégrer maintenant côté doctrine + UI |
| Visual Lab | Langflow, Flowise, Dify | Optionnel, jamais runtime de vérité |
| Automation périphérique | n8n | Plus tard via webhooks |
| Local Tools | OmniTools | Plus tard comme service optionnel ou inspiration UI |
| Browser Tool | browser-harness | Après Approval Gate, PolicyGate et Observability |

---

## Classification obligatoire des idées externes

Chaque idée externe doit être classée :

- À intégrer maintenant
- À intégrer plus tard
- Intéressant mais non prioritaire
- À rejeter
- Risqué
- Redondant avec l’existant

---

## Fiche d’intégration obligatoire

Pour chaque idée retenue :

| Champ | Contenu attendu |
|---|---|
| Problème résolu | Ce que l’idée corrige réellement |
| Fichier MD à modifier | `STATUS.md`, `ROADMAP.md`, `ARCHITECTURE.md`, `AGENTS.md`, `MODULES.md`, `README.md` |
| Section concernée | Section précise |
| Impact architecture | Faible / moyen / fort |
| Impact code | Fichiers ou modules touchés |
| Risques | Dette, sécurité, couplage, complexité |
| Priorité | P0 / P1 / P2 / P3 |

---

## Règles d’usage

Ne pas copier mécaniquement une architecture externe.

Ne pas ajouter un second runtime de vérité.

Ne pas importer de catalogue massif d’agents.

Ne pas intégrer de Browser Tool avant Approval Gate, PolicyGate, traces et screenshots.

Ne pas faire de mise à jour automatique sans consentement explicite.

Ne pas régénérer automatiquement les fichiers d’instructions IA sans revue humaine, car les Markdown de référence restent souverains.

Ne pas intégrer un chunker externe comme dépendance obligatoire avant Evaluation Harness, benchmark sur documents Pantheon et vérification de licence.

Pantheon OS conserve son identité : modularité, agents spécialisés, orchestration contrôlée, mémoire projet, RAG, workflows, validation, observability, self-hosting.
