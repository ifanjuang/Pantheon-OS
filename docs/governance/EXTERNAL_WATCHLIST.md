# Pantheon OS — External Watchlist

Ce fichier suit les dépôts, guides et projets externes utilisés comme veille ou inspiration.

Règle : ces dépôts ne sont pas des dépendances runtime de Pantheon OS sauf décision explicite. Toute idée externe doit d’abord être comparée aux Markdown de référence avant modification du code.

---

## Table de veille

| Source | Usage Pantheon OS | Statut | Dernier audit | Décision |
|---|---|---|---|---|
| `smarzola/hermes-local-memory` | Doctrine mémoire locale | Veille active | 2026-04-26 | Retenir mémoire multi-couches, candidate facts, active facts, cards, context preview, dry-run ; pas de dépendance runtime |
| `mage0535/hermes-memory-installer` | Installation mémoire locale / bootstrap mémoire | Plus tard | 2026-04-26 | Retenir installation mémoire, injection mémoire, auto-mount skills, archivage local ; rejeter SQLite FTS5 comme source principale et promotion non validée |
| `Rangle2/mda` | Mémoire associative online / complément RAG | Veille active | 2026-04-26 | Retenir l’idée d’une couche mémoire associative apprenant pendant l’inférence, complémentaire au RAG ; à benchmarker après modèle mémoire Pantheon + Evaluation Harness. Ne pas intégrer comme dépendance : licence SSPL/commerciale, approche expérimentale, doit rester soumise à Approval/Policy pour promotion mémoire |
| `suryamr2002/langgraph-approval-hub` | Approval Gate / HITL | Veille active | 2026-04-26 | Retenir statuts approval, pending queue, decision note, expiration, escalation, audit log ; pas de dashboard externe obligatoire |
| `sunny84patel/RAG-Evaluation` | Evaluation Harness RAG | Plus tard | 2026-04-26 | Retenir génération questions, comparaison configs RAG, métriques retrieval/source/faithfulness/latency ; rejeter Streamlit et Qdrant in-memory comme base |
| `HaroldConley/chunk-norris` | Sélection / comparaison de stratégies de chunking RAG | Veille active | 2026-04-26 | Retenir l’idée de tester plusieurs chunkers par corpus/document, questions générées et choix de stratégie ; à intégrer après Evaluation Harness, sans dépendance directe tant que licence/qualité non auditées |
| `BartAmin/Clustered-Dynamic-RAG` | Retrieval dynamique / clustering documentaire | Veille active | 2026-04-26 | Retenir l’idée d’un retrieval adaptatif par clusters ou groupes sémantiques ; à benchmarker après Evaluation Harness, sans remplacer pgvector ni le pipeline RAG existant |
| `kreuzberg-dev/kreuzcrawl` | Crawling web / extraction documentaire | À vérifier | 2026-04-26 | Intéressant pour ingestion web contrôlée ; à reporter après PolicyGate, scope/robots/allowlist et observability. Ne pas utiliser pour crawl large non gouverné |
| `browser-use/browser-harness` | Browser Tool gouverné | Plus tard | 2026-04-26 | À reporter après Approval Gate, PolicyGate et Observability ; retenir screenshots before/after et action traces |
| `openensemble/openensemble` | Plateforme multi-user agents / skills / self-hosting | Veille active | 2026-04-26 | Retenir patterns : comptes isolés, per-user workspace, skill manifests, backup/restore, update prudent, sandbox shell, providers multiples. Ne pas intégrer comme dépendance : licence non-commerciale, stack Node, second runtime concurrent |
| `yassin123mom/the-spark-architecture` | Spécification conceptuelle AGI / boucle motivation-recherche-sécurité | Veille faible | 2026-04-26 | Retenir uniquement comme réflexion : boucle objectif → recherche → création outil → mémoire → sécurité. Ne pas intégrer tel quel : spéculation AGI, pas d’implémentation opérationnelle, risque de dérive proactive non gouvernée |
| `Saichandra2520/AgentForge` | Scaffold Python pour projets agents | Veille active | 2026-04-26 | Retenir génération de templates ReAct/RAG/multi-agent/HITL avec FastAPI/tests/Docker/observability ; utile comme inspiration pour générateurs de modules Pantheon, pas comme runtime |
| `zauberzeug/nicegui` | UI Python/FastAPI pour dashboards et consoles internes | Veille active | 2026-04-26 | Candidat sérieux pour Installer UI ou Hermes Console légère : backend-first Python, FastAPI, composants UI, tables, timers, routes custom, pytest. Ne pas remplacer OpenWebUI ; évaluer complexité et packaging avant adoption |
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
| Runtime contracts | CrewAI, ElizaOS, agentskills, OpenEnsemble, AgentForge | À intégrer progressivement ; sources externes comme références de patterns, pas runtimes |
| Approval / Safety | langgraph-approval-hub | À finaliser avant actions sensibles |
| Memory | hermes-local-memory, hermes-memory-installer, MDA | À documenter maintenant, implémenter après stabilisation ; MDA seulement comme piste complémentaire benchmarkée |
| RAG Quality | RAG-Evaluation, ChunkNorris, Clustered-Dynamic-RAG, agents-towards-production | À intégrer après Approval Gate minimal ; évaluer d’abord chunking, clustering et retrieval dynamique sur corpus Pantheon |
| Web ingestion / crawling | kreuzcrawl, browser-harness | À reporter après PolicyGate, allowlist, scope, robots, traces et observability |
| Self-hosting | StartOS, OpenEnsemble, Installer UI interne | À intégrer maintenant côté doctrine + UI ; retenir lifecycle, backup, update prudent, isolation utilisateurs |
| Admin / Installer UI | NiceGUI, StartOS, Installer UI interne | NiceGUI est candidat pour UI Python légère ; à évaluer avant migration de l’Installer UI existante |
| Visual Lab | Langflow, Flowise, Dify | Optionnel, jamais runtime de vérité |
| Automation périphérique | n8n | Plus tard via webhooks |
| Local Tools | OmniTools | Plus tard comme service optionnel ou inspiration UI |
| Browser Tool | browser-harness | Après Approval Gate, PolicyGate et Observability |
| Controlled learning | the-spark-architecture, agents-towards-production | Retenir uniquement comme réflexion encadrée ; toute proactivité doit rester gouvernée par policies, approvals et objectifs documentés |

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

Ne pas lancer de crawler large sans allowlist, respect du périmètre, traçabilité, politique d’usage et validation humaine pour les sources sensibles.

Ne pas intégrer de boucle proactive type AGI sans objectif utilisateur/documentaire explicite, PolicyGate, Approval Gate, limites de ressources, logs et possibilité d’arrêt.

Ne pas reprendre de dépendance à licence non-commerciale dans Pantheon sans validation juridique explicite.

Ne pas multiplier les frameworks UI : OpenWebUI reste l’interface chat ; une UI Python type NiceGUI ne peut servir qu’à l’administration, l’installation ou la console interne.

Ne pas intégrer une mémoire online non auditée comme source de vérité. Toute mémoire associative ou apprise pendant l’inférence doit rester candidate, inspectable, benchmarkée et soumise aux règles de promotion mémoire Pantheon.

Pantheon OS conserve son identité : modularité, agents spécialisés, orchestration contrôlée, mémoire projet, RAG, workflows, validation, observability, self-hosting.
