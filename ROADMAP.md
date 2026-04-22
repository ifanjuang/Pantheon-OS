# ROADMAP — Pantheon OS

> Feuille de route V2 / V3 consolidant les acquis et traçant l'évolution vers une
> plateforme **portable par conception** : un **core générique** (runtime, agents,
> RAG, orchestration) et des **overlays métier** (`domains/{domain}/`) qui
> contiennent les skills et workflows spécifiques.
>
> Référentiel d'architecture : `CLAUDE.md` · Backlog détaillé : `DEVLIST.md`
> · Scoring décisionnel : `DECISION.md` · Mémoires : `MEMORY.md`

---

## 1. Acquis à préserver

Briques stables qui constituent la base intangible. Toute évolution doit les
protéger.

### 1.1 Architecture hexagonale — core portable
- **API FastAPI** (`platform/api/`) avec apps auto‑découvertes
  (`auth`, `admin`, `affaires`, `documents`, `agent`, `openai_compat`,
  `hermes_console`).
- Séparation stricte **stockage** (PostgreSQL + pgvector) / **traitements**
  (Hermes Runtime) / **interface** (OpenWebUI).
- En V2 : réintroduction maîtrisée de **LangGraph** (machines à états),
  **Redis + ARQ** (jobs asynchrones), **MinIO** (S3 fichiers volumineux).

### 1.2 Pipeline RAG et retrieval hybride
- Extraction → chunking → embedding → index pgvector (HNSW, cosinus).
- **Hybride BM25 + sémantique** via `search_hybrid()` + **Reciprocal Rank
  Fusion** + `SentenceWindowNodeParser` (contexte enrichi pour CCTP / DTU).
- Index GIN `ix_chunks_contenu_fts` (migration 0010) — rétrocompat totale.

### 1.3 Panthéon d'agents (22 rôles) et chaîne de veto
- Couches : `meta`, `analysis`, `memory`, `output`, `system`.
- MVP actifs : **@ZEUS**, **@ATHENA**, **@APOLLO**, **@Hermes**, **@Argos**,
  **@Prometheus**, **@Hecate**, **@Hestia**, **@Hades**, **@Kairos**,
  **@Daedalus**, **@Iris**.
- **Veto** : **@THEMIS** (intégrité process, déclenché en C4+).
- Source de vérité : `modules/agents/{layer}/{myth}_{role}/` — manifest,
  `SOUL.md`, skills, tests.

### 1.4 Orchestration multi‑patterns
- Zeus décompose en sous‑tâches avec **4 patterns de collaboration** :
  - `cascade` — séquence avec contexte cumulatif ;
  - `arena` — round parallèle + round d'arbitrage ;
  - `parallel` — `asyncio.gather` ;
  - `solo` — agent unique.
- `dispatch_subtasks` + `_topological_levels` — exécution par niveaux de
  dépendances.
- Streaming SSE enrichi (`subtask_done`), état typé (`OrchestraState`,
  `Subtask`).

### 1.5 Criticité C1–C5 et décisionnel
- **Scoring /100** (`DECISION.md`) : Technique /25 · Contractuel /25 ·
  Planning /20 · Cohérence /15 · Robustesse /15.
- Interprétation : 80–100 robuste · 60–80 acceptable · 40–60 fragile
  · <40 dangereux.
- **HITL** activé en C4/C5, politique **draft first**, règles d'escalade.
- **Dette décisionnelle D0–D3** (D0 résolue → D3 bloquée) — concept
  distinctif à capitaliser.

### 1.6 Trois couches de mémoire
- **@Hestia** — mémoire projet : décisions, contraintes, hypothèses, dette.
- **@Mnemosyne** — mémoire agence : patterns, capitalisation inter‑projets.
- **Mémoire fonctionnelle** — état de run partagé entre agents.

### 1.7 Principes d'ingénierie agent
Planning avant exécution · tool design explicite · gestion d'erreurs ·
évaluation mesurable · réversibilité. Voir `AGENT_ENGINEERING_PRINCIPLES.md`.

### 1.8 Portabilité multi‑domaine — overlays
- Structure déjà posée : `domains/architecture/`, `domains/legal/`,
  `domains/medical/`.
- Chaque overlay porte : `prompts/`, `skills/`, `workflows/`, `policies/`.
- Activation via `config/domains.yaml` (`active_domain`, `overlays`).

---

## 2. Roadmap V2 — modernisation du core

### 2.1 Contrat agent unifié et registre dynamique
- Signature unique `run(context, task, artifacts)` sur `AgentBase`.
- Chaque agent : `agent.py` · `manifest.yaml` · `SOUL.md` · `skills/` ·
  `tests/`.
- **`ManifestLoader`** parcourt `modules/agents/` et `modules/skills/` au
  démarrage → ajout/retrait sans toucher au code cœur.

### 2.2 Modularisation des services
- Découplage net **API** / **orchestrateur Hermes** / **UI** en packages.
- Orchestrateur réutilisable hors contexte BTP.
- Config centralisée : 5 YAML canoniques (`runtime`, `settings`, `sources`,
  `ui`, `domains`) + loader générique. Secrets isolés dans `.env`.

### 2.3 State manager et reprise sur plantage
- Persistance runs en PostgreSQL (`agent_runs`, `orchestra_runs`) +
  snapshots `platform/data/runtime-state/`.
- Reprise après crash + simplification SSE.
- **Redis** pour la mémoire fonctionnelle partagée inter‑agents.

### 2.4 Chaîne de veto séquencée (LangGraph)
- Architecture cible :
  `execute_agents → veto_check → [C4+] veto_themis → veto_zeus → zeus_judge`.
- Chaque nœud retourne `{"verdict": "approved"|"vetoed", "justification"}`.
- Multi‑rounds arène extensible.

### 2.5 Hestia post‑orchestration automatique
Après chaque `synthesize` : décision mémorisable ? → stockage `scope=projet` ;
pattern agence détecté ? → proposition de capitalisation `scope=agence`.
Impact : mémoire projet auto‑alimentée.

### 2.6 Hermes Console et monitoring
- Onglet Next.js dans OpenWebUI — API `/console` déjà prévue (dashboard,
  agents, skills, workflows, settings, logs).
- Activation/désactivation à chaud.
- Monitoring `agent_runs`, `orchestra_runs`, jobs ARQ — durée, taux d'échec,
  agents les plus sollicités.

### 2.7 Pipelines OpenWebUI
Déclencher `zeus/orchestra` directement depuis le chat via pipeline
OpenWebUI — raccourcit le chemin utilisateur → orchestration.

### 2.8 Retrieval multimodal
- Chunks images (plans, coupes, photos chantier) + description générée par
  **@Argos** + qualification **@Hephaestus**.
- Même pipeline RAG hybride — embedding vision + fusion RRF.

### 2.9 DSPy — plan phasé d'optimisation
- **Phase 1 (instrumentation)** : annoter `agent_runs`, structurer les
  exemples (instruction → result). Aucun code DSPy encore.
- **Phase 2 (≈100 runs annotés)** : DSPy ciblé sur modules structurés —
  classification C1‑C5 de Hermès, extraction CR → actions, extraction
  métadonnées documents. Optimizer `MIPROv2` ou `BootstrapFewShot`.
- **Phase 3 (V2+)** : Zeus et Hermès si exemples suffisants.
- **Exclus** : agents créatifs, `SOUL.md` — la personnalité est le produit.

### 2.10 Tests automatisés
- Unitaires : `agent/tools.py`, skills critiques.
- Intégration : `orchestra/service.py` sur cycles C1–C5.
- End‑to‑end : RAG hybride, orchestration multi‑patterns, veto, mémoire —
  cas limites (devis incomplet, contradiction planning…).

---

## 3. Roadmap V2 — overlay métier `domains/architecture/`

Le métier BTP/MOE vit **hors du core** dans `domains/architecture/` — skills
modulaires, activables/désactivables, remplaçables par d'autres overlays
métier (legal, medical…).

Chaque skill métier :
- `domains/architecture/skills/{nom}/` — manifest, tools, prompts, tests ;
- migrations Alembic pour ses tables ;
- visibilité Hermes Console (toggle, logs, monitoring).

### 3.1 skill `decisions`
Dette décisionnelle **D0–D3** + scoring /100.
- Table `project_decisions` (migration 0008 déjà en place).
- `GET /affaires/{id}/decisions[?dette=D2,D3]` · `POST /decisions` ·
  `PATCH /decisions/{id}` · `POST /decisions/{id}/resolve`.
- Alertes automatiques sur D3 (date dépassée).

### 3.2 skill `planning`
Gantt, lots, jalons, impacts cascade.
- Tables `lots`, `jalons`, `dependances`.
- Calcul automatique des dérives si un lot glisse.
- Vue Gantt (JSON front).
- Alerte si dérive > seuil (intégration future avec un agent *Chronos*
  overlay).
- Trigger depuis actions CR → mise à jour lot.

### 3.3 skill `chantier`
Observations terrain, non‑conformités, photos.
- Tables `observations`, `non_conformites`.
- Pipeline photo → **@Argos** analyse → **@Hephaestus** qualifie → statut NC.
- Localisation XY sur plan.
- Suivi levée des réserves AOR.

### 3.4 skill `finance`
Situations de travaux, avenants, budget.
- Tables `situations`, `avenants`, `lignes_budget`.
- Montant marché, cumul facturé, reste à facturer par lot.
- Gestion avenants (proposition **@Themis** si hors contrat).
- Alertes dépassement budget.

### 3.5 skill `communications`
Registre courrier entrant/sortant.
- Table `courriers` (référence, expéditeur, objet, statut).
- Ingest RAG des courriers importants.
- Relances automatiques (**@Iris**).
- Lien avec actions CR.

### 3.6 skill `webhooks`
Bots Telegram / WhatsApp conversationnels.
- Réception messages → routing par **@mention** (`@zeus`, `@themis`, `@argos`).
- Sans mention → **@Hermes** qualifie et route.
- Historique maintenu par **@Hestia**.
- **Support photos** : photo → Argos → Héphaïstos → réponse au fil.
- Auth par numéro/compte autorisé.
- Stack : `python-telegram-bot` · Twilio ou Meta Cloud API · stockage MinIO.

### 3.7 agent overlay `@Vitruve` (exploration)
Agent de démarrage projet spécifique BTP.
- Analyse programme client → surfaces, usages, relations fonctionnelles.
- Étude sol G1/G2 → portance, fondations, nappe.
- Relevé topo → pente, orientation, NGF, voisinage.
- PLU → emprise, hauteur, prospect.
- Secteur ABF, zones à risque (inondation, sismique, archéo).
- Cohérence programme/budget MOA.
- **Sortie** : fiche synthèse contraintes avant ESQ.

---

## 4. Roadmap V3 — ouverture et généralisation

### 4.1 Nouveaux overlays métier
- `domains/legal/` — scoring juridique, analyse normative, registre pièces.
- `domains/medical/` — cotation, protocoles, dossier patient.
- `domains/audit/`, `domains/consulting/`, `domains/it/`.
- Chacun : prompts + skills + workflows + policies propres ; core inchangé.

### 4.2 Plugin system skills
API stable pour qu'un domaine déclare ses skills sans toucher au core —
calcul structurel, analyse normative, scoring juridique, cotation médicale,
etc.

### 4.3 Abstraction LLM
Provider‑agnostic (Ollama, OpenAI, Anthropic, Mistral) — hot‑swap via
`settings.yaml`, fallback configuré, routing par coût/latence.

### 4.4 Versioning SemVer
Par agent, skill, workflow, overlay — déploiement versionné selon métier,
compat matricielle documentée.

### 4.5 Portabilité des mémoires
Export / import **@Hestia** (projet) et **@Mnemosyne** (agence) — backups,
migrations inter‑serveurs sans perte.

### 4.6 Voix
Transcription (NoobScribe) + synthèse TTS dans OpenWebUI et webhooks.

### 4.7 Explorations
- **Hindsight / TEMPR** (vectorize‑io) — mémoire agentique
  sémantique + BM25 + graphe + temporel. Évaluation sur affaire pilote.
- **Neo4j** — graphe de connaissances (décisions ↔ documents ↔ acteurs ↔
  DTU) si la complexité justifie un 6ᵉ store.
- **Hermes‑Agent** — variations sur mesure d'agents existants (ex.
  *Prometheus junior*). Garder garde‑fou : ne pas diluer l'identité du
  panthéon.
- **Micro‑services** — *seulement si* la charge ou l'équipe l'exige.
  L'hexagonal modulaire couvre 90 % du besoin ; pas un objectif en soi.

---

## 5. Garde‑fous — ne rien perdre de l'existant

- **Documenter** chaque agent, skill, workflow, overlay en Markdown de
  référence (objectifs, entrées, sorties, limites).
- **Tests de non‑régression** sur les flux critiques (RAG hybride,
  orchestration multi‑patterns, chaîne veto, mémoire, scoring décisionnel).
- **Migrations Alembic** systématiques pour toute modification de schéma.
- **Helpers stables** conservés (extraction PDF, SSE, `search_hybrid`) tant
  qu'ils fonctionnent.
- **Branches Git** :
  - `main` — production stable ;
  - `develop` — travaux V2 ;
  - `experiment/v3-*` — explorations V3 ;
  - `overlay/{domain}` — développement d'un nouvel overlay métier.

---

## 6. Synthèse des phases

| Phase | Core | Overlay architecture | Livrable clé |
|---|---|---|---|
| **MVP** | Runtime Hermes + 12 agents + RAG hybride | — | API + OpenWebUI + Console |
| **V2** | Registre dynamique, state manager, veto chain, DSPy P1–P2, multimodal, tests | skills `decisions`, `planning`, `chantier`, `finance`, `communications`, `webhooks`, agent `Vitruve` | Console + LangGraph + Redis + overlay BTP complet |
| **V3** | Abstraction LLM, SemVer, export mémoire, voix, plugin system | — | Overlays `legal`, `medical`, `audit`… · plateforme multi‑domaine |

La ligne directrice : **core mince et générique, valeur métier dans les
overlays**. C'est ce qui rend Pantheon OS portable d'un cabinet
d'architecture à un cabinet juridique sans toucher au runtime.
