# OS PROJET — Plan de développement technique

> Document de référence pour Claude. À relire au début de chaque session.

---

## PRÉSENTATION

### Ce qu'est OS Projet

**OS Projet** est la mémoire vivante et l'intelligence opérationnelle d'une agence d'architecture.

Il accompagne chaque opération du premier trait de crayon à la levée des réserves — et au-delà. À chaque étape, chaque acteur dépose naturellement ce qu'il sait : une question posée, un calcul réalisé, un diagnostic établi, une décision prise, un email reçu, une réunion tenue. Le système l'intègre, le comprend, le relie à ce qui existe déjà, et le rend accessible à tous, pour toujours.

Avec le temps, ces dépôts s'accumulent en deux niveaux d'intelligence :

- **L'intelligence du projet** — la mémoire complète d'une opération : ses choix structurels, ses contraintes réglementaires, ses calculs, ses aléas, ses arbitrages. Consultable à tout moment par n'importe quel acteur autorisé, sous forme de question naturelle.

- **L'intelligence de l'agence** — ce que tous les projets ont appris. Les solutions qui ont fonctionné, les erreurs à ne pas reproduire, les réponses aux questions récurrentes, les détails constructifs éprouvés. Un savoir-faire institutionnel qui ne disparaît pas quand un collaborateur part.

---

### Le problème résolu

Une agence d'architecture produit une quantité massive d'information tout au long de ses opérations : notes de calculs, diagnostics, correspondances, comptes-rendus, pièces graphiques, plannings, situations financières. Cette information est aujourd'hui fragmentée — dans les boîtes mail de chacun, dans des dossiers mal partagés, dans des tableurs sans logique commune, dans la tête des collaborateurs.

Le résultat : on refait ce qui a déjà été fait, on perd du temps à chercher ce qu'on sait pourtant, on ne capitalise pas sur l'expérience accumulée. Et quand un collaborateur clé quitte l'agence, une partie du savoir-faire part avec lui.

**OS Projet répond à cela en rendant la capitalisation naturelle.** Chaque acte de travail normal — rédiger une note, envoyer un email, tenir une réunion, produire un calcul — alimente automatiquement la mémoire du projet et de l'agence. Sans double saisie, sans formulaire à remplir.

---

### Les phases couvertes

OS Projet accompagne l'intégralité du cycle de vie d'une opération :

```
Faisabilité → ESQ → APS → APD → PRO → DCE → ACT → EXE → OPR/AOR → GPA
     ↑           ↑          ↑          ↑         ↑         ↑
 Diagnostics  Questions  Notes de   CCTP &   Planning   Réception
  existant   théoriques  calculs    pièces   chantier   & mémoire
```

À chaque phase, les outils adaptés sont disponibles. Un architecte en phase APS peut interroger le système sur une question réglementaire et la réponse sera enregistrée dans la mémoire du projet. Un ingénieur en phase PRO peut déposer sa note de calcul thermique et la relier automatiquement aux décisions d'enveloppe prises en APS. Un conducteur de travaux en phase EXE peut signaler un blocage et l'impact sur le planning est calculé immédiatement.

---

### Ce que fait OS Projet

**Pendant la conception**

| Outil | Usage |
|-------|-------|
| **Questions théoriques** | Poser une question (réglementaire, technique, constructive) → le système cherche dans la base de connaissance de l'agence, répond et enregistre la Q&R dans la mémoire du projet |
| **Notes de calculs** | Déposer, versionner et relier les notes de calculs (structure, thermique, acoustique, incendie) aux phases et décisions qui les ont motivées |
| **Diagnostics** | Enregistrer les diagnostics de l'existant (relevés, DPE, structure, assainissement), les relier aux contraintes qui en découlent |
| **Mémoire de conception** | Capitaliser automatiquement les partis pris architecturaux, les choix constructifs et leurs justifications |

**Pendant les études et le DCE**

| Outil | Usage |
|-------|-------|
| **Documents** | Générer les pièces (CCTP, CCAP, notices, rapports) à partir des données du projet et de templates |
| **Communications** | Registre de toutes les correspondances avec MOA, bureaux d'études, administrations — classées, suivies, répondues |
| **Planning études** | Timeline des livrables par phase avec dépendances entre intervenants |

**Pendant le chantier**

| Outil | Usage |
|-------|-------|
| **Planning travaux** | Extrait les lots du CCTP, génère la timeline avec chevauchements, détecte les impacts de retard en cascade |
| **Finance** | Situations de travaux, avenants, tableau de bord marché actualisé / reste à facturer |
| **Meeting** | Analyse un CR brut → extrait décisions, actions, blocages → alimente automatiquement le planning et la mémoire |
| **Journal** | Observations, photos, avancements, jalons en temps réel |
| **Alertes** | Deadlines, dépendances non respectées, dépassements, blocages prolongés |

**En continu — Intelligence de l'agence**

| Outil | Usage |
|-------|-------|
| **Mémoire projet** | Décisions validées, risques identifiés, solutions retenues — déduplication sémantique, accès par question naturelle |
| **Base de connaissance agence** | Accumuler les réponses aux questions récurrentes, les détails constructifs éprouvés, les leçons tirées de chaque opération |
| **Recherche transversale** | "Comment avons-nous traité ce problème sur d'autres projets ?" — recherche sémantique inter-projets |

---

### Le rôle de l'IA

L'IA n'est pas un chatbot généraliste. Elle est **ancrée dans les données réelles** de chaque projet et de l'agence. Elle ne répond jamais de mémoire — elle interroge systématiquement la base avant de répondre.

Elle sert à :
- **Comprendre** les documents déposés (CCTP, notes de calculs, emails) et en extraire l'essentiel automatiquement
- **Relier** les informations entre elles (cette note de calcul répond à cette question posée en phase APS)
- **Alerter** quand quelque chose mérite attention (retard, dépassement, incohérence)
- **Générer** des pièces (CR, documents, brouillons de réponse) à partir des données existantes
- **Répondre** aux questions de l'équipe en s'appuyant sur la mémoire du projet et de l'agence

---

### Les acteurs et leurs rôles

Chaque acteur du projet interagit avec l'outil selon ses besoins, et contribue naturellement à la mémoire collective :

| Acteur | Ce qu'il utilise | Ce qu'il contribue |
|--------|------------------|--------------------|
| **Architecte / MOE** | Questions théoriques, mémoire projet, documents, planning études | Partis pris, choix constructifs, décisions |
| **Ingénieur BE** | Notes de calculs, questions techniques, diagnostics | Calculs, contraintes, solutions techniques |
| **Chargé de mission** | Planning travaux, meeting, journal, communications | Avancements, actions, observations terrain |
| **Comptable / gestionnaire** | Finance, situations, avenants | Données financières, paiements |
| **MOA / Client** (lecteur) | Tableau de bord, avancement, documents diffusés | — |
| **Entreprises** (lecteur) | Planning, CR diffusés, ordres de service | — |

---

### Architecture

```
OpenWebUI (agents IA + tools — un agent par domaine métier)
        ↓  JWT
FastAPI API modulaire (plugin system — chaque module = plugin autonome)
   ├── core/ : registry, auth JWT, bus événements PostgreSQL
   │           RAG service, storage service, LLM service
   └── modules/
       ├── conception : phases | notes_calculs | diagnostics
       ├── transversal : memory (projet + agence) | rag | communications | documents | meeting
       ├── chantier   : planning | finance | budget | journal | events_engine
       └── système    : auth | admin | intervenants
        ↓                    ↓                   ↓
PostgreSQL + pgvector    MinIO (fichiers)    Notion (sync optionnel)
(données + vecteurs)     (PDF, photos, docs)
```

**Principes :**
- **Modulaire** — plugin system, chaque fonctionnalité est indépendante
- **Configurable** — comportement métier dans `config.yaml`, modifiable sans redéploiement
- **Multi-utilisateurs** — 4 rôles (admin / moe / collaborateur / lecteur) avec permissions per-affaire
- **Cycle de vie complet** — de la faisabilité à la GPA
- **Capitalisation naturelle** — chaque acte de travail alimente la mémoire sans effort supplémentaire
- **Intelligence à deux niveaux** — mémoire projet + intelligence agence

---

### Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | FastAPI + SQLAlchemy async (asyncpg) |
| Base de données | PostgreSQL 16 + pgvector |
| Storage fichiers | MinIO (S3-compatible self-hosted) |
| IA / LLM | OpenAI gpt-4o + text-embedding-3-large |
| Interface IA | OpenWebUI (agents + tools) |
| Auth | JWT HS256 — 4 rôles |
| Bus événements | PostgreSQL LISTEN/NOTIFY |
| Conteneurs | Docker Compose |

---

## 0. TL;DR

Système de pilotage intelligent de chantier pour une agence d'architecture (MOE).
Stack : **FastAPI + PostgreSQL/pgvector + OpenWebUI + MinIO + Notion**.

**Décisions d'architecture arrêtées :**
- Auth : **JWT HS256** — 4 rôles (admin / moe / collaborateur / lecteur) — per-affaire
- Storage : **MinIO** (S3-compatible, self-hosted Docker) — partagé entre tous les modules
- RAG : **service core partagé** (`core/services/rag_service.py`) — plus un module isolé
- Bus événements : **PostgreSQL LISTEN/NOTIFY** — fonctionne multi-workers, pas de Redis en v1
- Planning : lots extraits du **CCTP par LLM** — per-affaire, plus de LOT_DEPENDENCIES global
- Rate limiting : **slowapi** sur les endpoints LLM (10 req/min/user)
- Multi-tenant : **non en v1** (une agence = une instance)

Objectif : un "OS chantier" capable de gérer plannings, finances, communications et documents avec assistants IA.

---

## 1. ORGANISATION DU REPO

> **Architecture modulaire** : chaque fonctionnalité est un module autonome dans `api/modules/{nom}/`.
> `main.py` ne connaît aucun module : il appelle le registry qui les découvre et les monte automatiquement.
> Pour ajouter, désactiver ou modifier un module → toucher uniquement son dossier.

```
ARCEAG/
├── DEVPLAN.md
├── docker-compose.yml
├── .env.example
├── modules.yaml                ← registre des modules activés/désactivés
│
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 ← crée l'app + appelle registry.load_all()
│   ├── config.py               ← settings globaux (pydantic-settings)
│   ├── database.py             ← session SQLAlchemy async (partagée)
│   │
│   ├── core/                   ← KERNEL — ne pas modifier sauf refacto architecture
│   │   ├── __init__.py
│   │   ├── registry.py         ← découverte + chargement auto des modules
│   │   ├── base_engine.py      ← classe abstraite BaseEngine
│   │   ├── base_router.py      ← classe abstraite BaseRouter
│   │   ├── base_tool.py        ← classe abstraite BaseTool
│   │   ├── events.py           ← bus PostgreSQL LISTEN/NOTIFY inter-modules
│   │   ├── auth.py             ← JWT decode, get_current_user, require_role()
│   │   └── services/           ← services partagés (importables par tout module)
│   │       ├── __init__.py
│   │       ├── rag_service.py  ← embed, chunk, search cosine (pgvector)
│   │       ├── llm_service.py  ← appels LLM (chat, extraction, embedding)
│   │       └── storage_service.py ← upload/download MinIO (S3-compatible)
│   │
│   └── modules/                ← UN DOSSIER = UN MODULE COMPLET
│       │
│       ├── auth/               ← gestion utilisateurs + tokens + rôles
│       │   ├── manifest.yaml
│       │   ├── models.py       ← users, affaire_permissions
│       │   ├── schemas.py
│       │   ├── router.py       ← /auth/* (login, refresh, register, users)
│       │   └── engine.py       ← hash password, generate JWT, check permissions
│       │
│       ├── chantier/           ← module socle (affaires, journal)
│       │   ├── manifest.yaml
│       │   ├── config.yaml
│       │   ├── models.py       ← affaires, chantier_events, intervenants
│       │   ├── schemas.py
│       │   ├── router.py       ← /chantier/*
│       │   ├── engine.py
│       │   └── tools.py
│       │
│       ├── planning/           ← planning CCTP-driven + scénarios + impact
│       │   ├── manifest.yaml
│       │   ├── config.yaml     ← overlap_pct défaut, fallback rules, jours fériés
│       │   ├── models.py       ← planning_lots, planning_dependencies,
│       │   │                      planning_ouvrages, planning_cctp_ingestions
│       │   ├── schemas.py
│       │   ├── router.py       ← /planning/*
│       │   ├── engine.py       ← tri topo + overlap + chemin critique + BFS impact
│       │   ├── cctp_parser.py  ← extraction lots depuis CCTP (LLM)
│       │   ├── dependency_detector.py ← inférence dépendances (LLM) + override
│       │   ├── tools.py
│       │   └── prompts/
│       │       ├── cctp_extraction.txt
│       │       └── dependency_inference.txt
│       │
│       ├── budget/             ← budgets lots + alertes
│       │   ├── manifest.yaml
│       │   ├── models.py
│       │   ├── schemas.py
│       │   ├── router.py       ← /budget/*
│       │   ├── engine.py
│       │   └── tools.py
│       │
│       ├── finance/            ← situations de travaux, avenants
│       │   ├── manifest.yaml
│       │   ├── config.yaml     ← seuil_alerte_pct, retenue_garantie_pct
│       │   ├── models.py       ← situations, avenants
│       │   ├── schemas.py
│       │   ├── router.py       ← /finance/*
│       │   ├── engine.py
│       │   └── tools.py
│       │
│       ├── meeting/            ← analyse CR, extraction actions
│       │   ├── manifest.yaml
│       │   ├── config.yaml     ← prompt LLM overridable
│       │   ├── models.py
│       │   ├── schemas.py
│       │   ├── router.py       ← /meeting/*
│       │   ├── engine.py
│       │   └── tools.py
│       │
│       ├── communications/     ← registre emails reçus/transmis
│       │   ├── manifest.yaml
│       │   ├── config.yaml     ← CATEGORIES, PRIORITES, reference_format
│       │   ├── models.py       ← communications + vector(1024)
│       │   ├── schemas.py
│       │   ├── router.py       ← /communications/*
│       │   ├── engine.py
│       │   └── tools.py
│       │
│       ├── documents/          ← génération pièces (CR, PV, FNC, OS…)
│       │   ├── manifest.yaml
│       │   ├── config.yaml
│       │   ├── models.py
│       │   ├── schemas.py
│       │   ├── router.py       ← /documents/*
│       │   ├── engine.py       ← Jinja2 + LLM + upload MinIO
│       │   ├── tools.py
│       │   └── templates/
│       │       ├── cr_reunion.md.j2
│       │       ├── pv_reception.md.j2
│       │       ├── fiche_nc.md.j2
│       │       ├── ordre_service.md.j2
│       │       └── rapport_avancement.md.j2
│       │
│       ├── rag/                ← ingestion documents utilisateur (CCTP, normes)
│       │   ├── manifest.yaml
│       │   ├── config.yaml     ← chunk_size, overlap, top_k, model
│       │   ├── models.py       ← notion_chunks (vecteurs + metadata)
│       │   ├── schemas.py
│       │   ├── router.py       ← /rag/* (ingest, query, sources)
│       │   └── engine.py       ← délègue à core/services/rag_service.py
│       │                          (pas de tools : consommé par les autres modules)
│       │
│       ├── memory/             ← mémoire projet validée + candidates
│       │   ├── manifest.yaml
│       │   ├── config.yaml     ← seuils similarité, auto-save
│       │   ├── models.py       ← project_memory, memory_candidates, user_preferences
│       │   ├── schemas.py
│       │   ├── router.py       ← /memory/*
│       │   ├── engine.py
│       │   └── tools.py
│       │
│       └── events_engine/      ← moteur d'alertes (règles métier)
│           ├── manifest.yaml
│           ├── config.yaml     ← RULES overridables, intervalles
│           ├── models.py       ← alerts
│           ├── schemas.py
│           ├── router.py       ← /events/*
│           └── engine.py
│
├── db/
│   ├── alembic.ini
│   └── migrations/versions/    ← préfixe: {module}_{NNN}_{description}.py
│
├── openwebui/
│   ├── agents/                 ← un agent par module (depuis manifest.yaml)
│   └── knowledge/              ← CCTP exemples, normes NF, DTU…
│
└── docs/
```

---

## 1b. ARCHITECTURE MODULAIRE — Kernel & Plugin System

### Principe

```
Ajouter un module  → créer api/modules/{nom}/ avec les 6 fichiers standard
Désactiver          → modules.yaml : enabled: false  (pas de redémarrage requis en dev)
Modifier behavior   → éditer config.yaml du module  (hot-reload via watchfiles)
Modifier un prompt  → éditer config.yaml → prompt_file ou prompt inline
Modifier une règle  → éditer config.yaml → RULES / CATEGORIES / seuils
```

---

### `modules.yaml` — registre global

```yaml
# modules.yaml — à la racine du repo
# Ordre = ordre de chargement (respecter les dépendances)

modules:
  - name: chantier
    enabled: true

  - name: budget
    enabled: true

  - name: planning
    enabled: true

  - name: finance
    enabled: true

  - name: meeting
    enabled: true

  - name: communications
    enabled: true

  - name: documents
    enabled: true

  - name: rag
    enabled: true

  - name: memory
    enabled: true

  - name: events_engine
    enabled: true
```

---

### Services partagés (`api/core/services/`) — importables par tous les modules

Contrairement aux modules, les services core **n'ont pas de router ni de manifest**. Ils sont des bibliothèques internes importées directement.

```python
# Dans n'importe quel engine.py de module :
from core.services.rag_service import RagService
from core.services.storage_service import StorageService
from core.services.llm_service import LlmService
```

#### `rag_service.py`
```python
class RagService:
    async def embed(self, text: str) -> list[float]
    async def chunk_and_embed(self, text: str, source_type: str, affaire_id: UUID, metadata: dict) -> list[UUID]
    async def search(self, query: str, affaire_id: UUID, top_k: int = 5, source_type: str = None) -> list[dict]
    async def delete_source(self, affaire_id: UUID, source_ref: str)
```
> Utilisé par : `planning` (CCTP), `meeting` (historique), `communications` (search), `memory` (dédup), `rag` (router public)

#### `storage_service.py`
```python
class StorageService:
    # Bucket S3 : arceag-files
    # Clé : {affaire_id}/{module}/{filename}
    async def upload(self, affaire_id: UUID, module: str, filename: str, content: bytes, content_type: str) -> str  # → URL
    async def download(self, key: str) -> bytes
    async def presigned_url(self, key: str, expires_seconds: int = 3600) -> str
    async def delete(self, key: str)
    async def list_files(self, affaire_id: UUID, module: str = None) -> list[dict]
```
> Utilisé par : `planning` (CCTP PDF), `communications` (PJ emails), `documents` (pièces générées), `chantier` (photos)

#### `llm_service.py`
```python
class LlmService:
    async def chat(self, messages: list[dict], model: str = None, temperature: float = 0.7) -> str
    async def extract_structured(self, prompt: str, text: str, schema: dict, temperature: float = 0.1) -> dict
    async def embed(self, text: str) -> list[float]   # délègue à RagService
```
> Utilisé par : tous les modules LLM (planning, meeting, communications, documents, memory)

#### `events.py` — PostgreSQL LISTEN/NOTIFY

```python
# Bus inter-modules via PostgreSQL → fonctionne avec plusieurs workers uvicorn

import asyncpg, json
from typing import Callable

_handlers: dict[str, list[Callable]] = {}

async def subscribe(channel: str, handler: Callable, pool: asyncpg.Pool):
    """Écoute un channel PostgreSQL et appelle handler(payload: dict) à chaque NOTIFY."""
    _handlers.setdefault(channel, []).append(handler)
    async with pool.acquire() as conn:
        await conn.add_listener(channel, _dispatch)

async def publish(channel: str, payload: dict, pool: asyncpg.Pool):
    """Envoie un NOTIFY sur un channel PostgreSQL."""
    async with pool.acquire() as conn:
        await conn.execute(f"NOTIFY {channel}, $1", json.dumps(payload))

async def _dispatch(conn, pid, channel, payload_str):
    payload = json.loads(payload_str)
    for handler in _handlers.get(channel, []):
        await handler(payload)

# Channels standard :
# "planning_channel"      → lots validés, jalons dépassés, chemin critique changé
# "budget_channel"        → seuil atteint, situation déposée
# "chantier_channel"      → blocage ouvert, avancement mis à jour
# "communication_channel" → email urgent reçu
```

---

### `manifest.yaml` — déclaration d'un module

Chaque module **doit** avoir ce fichier. C'est le contrat avec le registry.

```yaml
# api/modules/finance/manifest.yaml

name: finance
version: "1.0.0"
description: "Suivi financier — situations de travaux, avenants, tableau de bord"
prefix: /finance          # préfixe URL du router FastAPI
depends_on:
  - chantier              # modules requis (chargés avant)
  - budget

# Tables DB que ce module possède (pour Alembic auto-migration)
models:
  - situations
  - avenants

# Background tasks périodiques
background_tasks:
  - name: check_retards_paiement
    interval_seconds: 3600   # toutes les heures

# Tools exposés à OpenWebUI
tools:
  - enregistrer_situation
  - valider_situation
  - enregistrer_avenant
  - get_tableau_bord_financier
  - get_alertes_financieres

# Agent OpenWebUI associé
agent:
  name: "Agent Finance MOE"
  system_prompt_file: agent_system.txt   # dans le dossier du module
  model: gpt-4o
```

---

### `config.yaml` — comportement overridable sans toucher au code

```yaml
# api/modules/finance/config.yaml
# Toutes les valeurs sont overridables par variable d'environnement
# ex: FINANCE_SEUIL_ALERTE_PCT=0.90

seuil_alerte_pct: 0.95          # alerte critique si cumul > 95% du marché
seuil_warning_pct: 0.80         # alerte warning si cumul > 80%
delai_paiement_warning_jours: 45
retenue_garantie_pct: 0.05
```

```yaml
# api/modules/communications/config.yaml

categories:
  demande_info:    ["question", "précision", "renseignement", "confirmer"]
  mise_en_demeure: ["mise en demeure", "délai impératif", "formal notice"]
  visa:            ["visa", "approbation", "validation document", "plan"]
  compte_rendu:    ["CR", "compte rendu", "procès verbal", "réunion"]
  bon_commande:    ["bon de commande", "BC", "ordre d'achat"]
  situation:       ["situation de travaux", "facture", "acompte"]
  reclamation:     ["réclamation", "litige", "contestation", "réserve"]

priorites:
  urgent: ["urgent", "URGENT", "mise en demeure", "délai 48h"]
  high:   ["important", "délai", "relance", "attention"]
  low:    ["pour info", "fyi", "copie"]

delai_reponse_warning_jours: 7
auto_reference: true
reference_format: "MOE-{YYYY}-{NNN}"  # ex: MOE-2025-042
```

```yaml
# api/modules/planning/config.yaml

lot_dependencies:
  Terrassement:      []
  Fondations:        ["Terrassement"]
  Maçonnerie:        ["Fondations"]
  Charpente:         ["Maçonnerie"]
  Couverture:        ["Charpente"]
  "Menuiseries ext.": ["Couverture"]
  Isolation:         ["Menuiseries ext."]
  Plâtrerie:         ["Menuiseries ext.", "Isolation"]
  Électricité:       ["Plâtrerie"]
  Plomberie:         ["Plâtrerie"]
  Chauffage:         ["Plomberie"]
  Carrelage:         ["Électricité", "Plomberie"]
  Peinture:          ["Plâtrerie", "Électricité"]
  "Menuiseries int.": ["Peinture"]
  VRD:               ["Terrassement"]
  "Espaces verts":   ["VRD"]

jalons:
  "Hors d'eau":   ["Couverture"]
  "Hors d'air":   ["Menuiseries ext."]
  "Support prêt": ["Plâtrerie"]
  Réception:      ["Peinture", "Menuiseries int.", "Carrelage"]

# Modifier les dépendances ici suffit — aucun code à changer
```

---

### Classes de base (`api/core/`)

#### `base_engine.py`
```python
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

class BaseEngine(ABC):
    """Contrat minimal pour tout engine métier."""

    def __init__(self, db: AsyncSession, config: dict):
        self.db = db
        self.config = config   # issu du config.yaml du module

    @classmethod
    def name(cls) -> str:
        """Nom du module propriétaire."""
        raise NotImplementedError

    # Les engines implémentent leurs méthodes métier librement.
    # Pas de méthodes abstraites supplémentaires : chaque engine est différent.
```

#### `base_router.py`
```python
from abc import ABC
from fastapi import APIRouter

class BaseRouter(ABC):
    """Chaque module expose un router FastAPI standard."""

    prefix: str = ""          # défini dans manifest.yaml
    tags: list[str] = []

    def get_router(self) -> APIRouter:
        raise NotImplementedError
```

#### `base_tool.py`
```python
from abc import ABC, abstractmethod
from typing import Any

class BaseTool(ABC):
    """Wrapper OpenWebUI — appelle l'API REST interne."""

    api_base: str = "http://api:8000"

    @abstractmethod
    def get_tools(self) -> list[dict]:
        """Retourne la liste des tools au format OpenWebUI."""
        ...
```

#### `registry.py` — auto-discovery
```python
import yaml, importlib
from pathlib import Path
from fastapi import FastAPI

class ModuleRegistry:
    def __init__(self, app: FastAPI):
        self.app = app
        self._modules: dict = {}

    def load_all(self, modules_yaml: str = "modules.yaml"):
        config = yaml.safe_load(Path(modules_yaml).read_text())
        for entry in config["modules"]:
            if entry.get("enabled", True):
                self._load_module(entry["name"])

    def _load_module(self, name: str):
        base = Path(f"api/modules/{name}")
        manifest = yaml.safe_load((base / "manifest.yaml").read_text())
        config = yaml.safe_load((base / "config.yaml").read_text()) if (base / "config.yaml").exists() else {}

        # Vérifier dépendances
        for dep in manifest.get("depends_on", []):
            assert dep in self._modules, f"Module '{name}' requiert '{dep}' (non chargé)"

        # Charger le router
        mod = importlib.import_module(f"modules.{name}.router")
        router = mod.get_router(config)
        self.app.include_router(router, prefix=manifest["prefix"], tags=[name])

        self._modules[name] = {"manifest": manifest, "config": config}
        print(f"[registry] module '{name}' chargé → {manifest['prefix']}")
```

#### `events.py` — bus inter-modules (publish/subscribe)
```python
# Permet à un module d'écouter les événements d'un autre
# sans couplage direct entre modules.

# Exemple : le module events_engine s'abonne aux événements
# publiés par planning, budget, chantier.

from collections import defaultdict
from typing import Callable, Any

_subscribers: dict[str, list[Callable]] = defaultdict(list)

def subscribe(event_type: str, handler: Callable):
    _subscribers[event_type].append(handler)

async def publish(event_type: str, payload: Any):
    for handler in _subscribers.get(event_type, []):
        await handler(payload)

# Événements standard publiés par les modules :
# "task.status_changed"      → planning module
# "budget.seuil_atteint"     → budget module
# "situation.deposee"        → finance module
# "communication.reçue"      → communications module
# "blocage.ouvert"           → chantier module
```

---

### `main.py` — 20 lignes, ne connaît aucun module

```python
from fastapi import FastAPI
from core.registry import ModuleRegistry
from database import engine, Base

app = FastAPI(title="OS Chantier API", version="1.0.0")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    registry = ModuleRegistry(app)
    registry.load_all("modules.yaml")

@app.get("/health")
async def health():
    return {"status": "ok"}
```

---

### Convention d'un module complet (exemple `finance/`)

```
api/modules/finance/
├── manifest.yaml          ← NOM, PREFIX, DEPENDS_ON, TOOLS, AGENT
├── config.yaml            ← SEUILS, RÈGLES, PROMPTS (overridables)
├── agent_system.txt       ← system prompt de l'agent OpenWebUI
├── models.py              ← SQLAlchemy models (situations, avenants)
├── schemas.py             ← Pydantic v2 (Create/Read/Update)
├── router.py              ← def get_router(config) → APIRouter
├── engine.py              ← class FinanceEngine(BaseEngine)
└── tools.py               ← class FinanceTools(BaseTool)
```

**Règle d'or :** un module ne peut **importer que `core/`** et ses propres dépendances déclarées dans `manifest.yaml`. Jamais d'import croisé entre modules — utiliser le bus d'événements.

---

### Ajouter un nouveau module en 5 étapes

```bash
# 1. Créer le dossier
mkdir api/modules/mon_module

# 2. Créer les 6 fichiers
touch api/modules/mon_module/{manifest.yaml,config.yaml,models.py,schemas.py,router.py,engine.py,tools.py}

# 3. Remplir manifest.yaml (name, prefix, depends_on, tools, agent)

# 4. Activer dans modules.yaml
echo "  - name: mon_module\n    enabled: true" >> modules.yaml

# 5. Générer la migration Alembic
alembic revision --autogenerate -m "mon_module_initial"
```

Redémarrage API → le module est monté automatiquement.

---

### Modifier le comportement sans toucher au code

| Ce que je veux changer | Où |
|------------------------|----|
| Seuil d'alerte budget | `modules/finance/config.yaml` → `seuil_alerte_pct` |
| Ajouter une catégorie email | `modules/communications/config.yaml` → `categories` |
| Ajouter une dépendance de lot | `modules/planning/config.yaml` → `lot_dependencies` |
| Changer le prompt LLM meeting | `modules/meeting/config.yaml` → `prompt_file` |
| Ajouter un type de document | `modules/documents/config.yaml` → `types` + template `.md.j2` |
| Ajouter une règle d'alerte | `modules/events_engine/config.yaml` → `rules` |
| Désactiver un module | `modules.yaml` → `enabled: false` |
| Changer le modèle LLM | `.env` → `LLM_MODEL=gpt-4o-mini` |

---

## 1c. AUTH — Utilisateurs, Rôles & Permissions

### Les 4 rôles

| Rôle | Qui | Ce qu'il peut faire |
|------|-----|---------------------|
| `admin` | Dirigeant / IT | Tout : users, config, modules, affaires, données |
| `moe` | Architecte chef de projet | Créer des affaires, tout gérer sur SES affaires + équipe |
| `collaborateur` | Chargé de mission, assistant | Lecture + écriture sur affaires auxquelles il est assigné |
| `lecteur` | Client, entreprise invitée, bureau de contrôle | Lecture seule sur affaires auxquelles il est assigné |

### Tables

```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    nom             VARCHAR(100),
    prenom          VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL,
    role            VARCHAR(30) NOT NULL DEFAULT 'collaborateur',
                    -- admin | moe | collaborateur | lecteur
    actif           BOOLEAN DEFAULT TRUE,
    openwebui_user_id VARCHAR(100),   -- lien avec l'identité OpenWebUI
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE affaire_permissions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    role_override   VARCHAR(30),      -- surcharge le rôle global sur cette affaire
                    -- NULL = utiliser le rôle global de l'utilisateur
    granted_by      UUID REFERENCES users(id),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, affaire_id)
);
```

### JWT — Structure du token

```json
{
  "sub": "user-uuid",
  "email": "jean@arceag.fr",
  "role": "moe",
  "exp": 1735689600,
  "iat": 1735603200
}
```

> Les permissions par affaire ne sont **pas** dans le JWT (liste peut être longue) — elles sont vérifiées en DB à chaque requête sensible via `affaire_permissions`.

### Middleware FastAPI (`core/auth.py`)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

bearer = HTTPBearer()

async def get_current_user(token = Depends(bearer), db = Depends(get_db)) -> User:
    """Décode le JWT et retourne l'utilisateur en DB. 401 si invalide."""
    ...

def require_role(*roles: str):
    """Dépendance FastAPI : vérifie que l'utilisateur a l'un des rôles spécifiés."""
    async def checker(user = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Rôle insuffisant")
        return user
    return checker

async def require_affaire_access(affaire_id: UUID, min_role: str = "lecteur", user = Depends(get_current_user), db = Depends(get_db)) -> User:
    """Vérifie que l'utilisateur a accès à cette affaire (rôle global ou override)."""
    if user.role == "admin":
        return user
    perm = await db.get(AffairePermission, (user.id, affaire_id))
    effective_role = perm.role_override if perm and perm.role_override else user.role
    if not _has_access(effective_role, min_role):
        raise HTTPException(status_code=403, detail="Accès refusé à cette affaire")
    return user
```

### Utilisation dans les routers

```python
# Lecture publique (pour les lecteurs) :
@router.get("/{affaire_id}")
async def get_affaire(affaire_id: UUID, user = Depends(require_affaire_access(min_role="lecteur"))):
    ...

# Écriture (moe ou collaborateur) :
@router.post("/{affaire_id}/events")
async def create_event(affaire_id: UUID, user = Depends(require_affaire_access(min_role="collaborateur"))):
    ...

# Admin seulement :
@router.get("/admin/users")
async def list_users(user = Depends(require_role("admin"))):
    ...
```

### Endpoints `/auth/*`

| Méthode | Endpoint | Rôle requis | Description |
|---------|----------|-------------|-------------|
| POST | `/auth/login` | — | Login email/password → JWT |
| POST | `/auth/refresh` | — | Rafraîchir le token |
| GET | `/auth/me` | tout rôle | Profil utilisateur courant |
| GET | `/auth/users` | admin | Lister tous les utilisateurs |
| POST | `/auth/users` | admin | Créer un utilisateur |
| PATCH | `/auth/users/{id}` | admin | Modifier rôle, actif… |
| DELETE | `/auth/users/{id}` | admin | Désactiver un utilisateur |
| GET | `/auth/affaires/{id}/permissions` | admin + moe | Voir qui a accès à cette affaire |
| POST | `/auth/affaires/{id}/permissions` | admin + moe | Donner accès à un utilisateur |
| DELETE | `/auth/affaires/{id}/permissions/{user_id}` | admin + moe | Révoquer accès |

### Intégration OpenWebUI

Chaque utilisateur OpenWebUI possède son propre token JWT dans la configuration de ses tools. Le token est transmis en header `Authorization: Bearer {token}` à chaque appel d'outil vers l'API.

```python
# Dans chaque tools.py (OpenWebUI) :
class Tools:
    class Valves(BaseModel):
        api_base: str = "http://api:8000"
        api_token: str = ""   # JWT de l'utilisateur (configuré dans OpenWebUI)

    def __init__(self):
        self.valves = self.Valves()

    def _headers(self):
        return {"Authorization": f"Bearer {self.valves.api_token}"}
```

---

## 1d. INTERFACE ADMIN — Pilotage de l'infrastructure

> Interface web dédiée aux administrateurs pour piloter l'OS Chantier sans toucher aux fichiers de config.
> Implémentée comme un **module `admin/`** avec son propre router FastAPI + une UI légère (React ou HTMX).

### Ce que l'admin peut faire

| Catégorie | Actions |
|-----------|---------|
| **Modules** | Activer/désactiver un module, voir son statut, lire son manifest + config |
| **Utilisateurs** | CRUD users, assignation rôles, permissions par affaire |
| **Connexions API** | Configurer clés (OpenAI, Notion…), tester la connexion, voir la latence |
| **Synchronisations** | Sens (push/pull/bidirectionnel), fréquence, dernier run, erreurs |
| **Mapping tables** | Éditer les tables de mapping (codes lots, catégories, types documents) |
| **Base de données** | Voir l'état des migrations, lancer une migration, stats tables (nb lignes) |
| **Storage** | Voir les buckets MinIO, espace utilisé, lister/supprimer fichiers par affaire |
| **Bus événements** | Voir les channels actifs, log des derniers événements publiés |
| **Rate limiting** | Voir les compteurs par user, ajuster les seuils |
| **Logs** | Consulter les logs API en temps réel (tail) |

### Structure du module

```
api/modules/admin/
├── manifest.yaml       ← prefix: /admin, depends_on: tous les modules
├── models.py           ← admin_logs, api_connections, sync_configs, mapping_tables
├── schemas.py
├── router.py           ← /admin/* (protégé : require_role("admin"))
├── engine.py           ← lecture config live, test connexions, stats DB
└── ui/                 ← interface web légère (HTMX ou React)
    ├── index.html
    ├── modules.html
    ├── users.html
    ├── connections.html
    ├── storage.html
    └── logs.html
```

### Tables

```sql
-- Connexions API externes configurées
CREATE TABLE api_connections (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nom         VARCHAR(100) NOT NULL,    -- "OpenAI", "Notion", "SMTP"
    type        VARCHAR(50) NOT NULL,     -- llm|embedding|storage|crm|email
    base_url    TEXT,
    api_key     TEXT,                     -- chiffré en DB (AES-256)
    config      JSONB DEFAULT '{}',       -- params spécifiques
    actif       BOOLEAN DEFAULT TRUE,
    last_test   TIMESTAMPTZ,
    last_status VARCHAR(20),              -- ok|error|timeout
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Configurations de synchronisation
CREATE TABLE sync_configs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nom             VARCHAR(100),
    source_module   VARCHAR(50),          -- "notion" | "planning" | "chantier"
    cible_module    VARCHAR(50),
    sens            VARCHAR(20),          -- push | pull | bidirectionnel
    frequence_sec   INTEGER DEFAULT 300,
    actif           BOOLEAN DEFAULT TRUE,
    last_run        TIMESTAMPTZ,
    last_status     VARCHAR(20),
    last_error      TEXT,
    config          JSONB DEFAULT '{}'
);

-- Tables de mapping éditables par l'admin
CREATE TABLE mapping_tables (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nom         VARCHAR(100) NOT NULL,    -- "categories_communications", "types_documents"
    module      VARCHAR(50),
    contenu     JSONB NOT NULL,           -- la table de mapping elle-même
    updated_by  UUID REFERENCES users(id),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### Endpoints `/admin/*`

```
GET  /admin/                         → dashboard (statut global)
GET  /admin/modules                  → liste modules + statut actif/inactif
POST /admin/modules/{name}/toggle    → activer/désactiver (modifie modules.yaml)
GET  /admin/modules/{name}/config    → lire config.yaml en live
PUT  /admin/modules/{name}/config    → modifier config.yaml sans redémarrage (hot-reload)

GET  /admin/users                    → liste utilisateurs
POST /admin/users                    → créer utilisateur
PATCH /admin/users/{id}              → modifier rôle/actif
GET  /admin/affaires/{id}/permissions → permissions d'une affaire
PUT  /admin/affaires/{id}/permissions → définir les accès

GET  /admin/connections              → liste connexions API
POST /admin/connections              → créer connexion
PUT  /admin/connections/{id}         → modifier
POST /admin/connections/{id}/test    → tester (ping + auth)

GET  /admin/syncs                    → liste synchronisations
POST /admin/syncs                    → créer config sync
PUT  /admin/syncs/{id}               → modifier sens/fréquence
POST /admin/syncs/{id}/run           → déclencher manuellement

GET  /admin/mappings                 → lister tables de mapping
GET  /admin/mappings/{nom}           → lire une table
PUT  /admin/mappings/{nom}           → modifier une table (JSONB éditeur)

GET  /admin/storage                  → stats buckets MinIO
GET  /admin/storage/{affaire_id}     → fichiers d'une affaire
DELETE /admin/storage/{key}          → supprimer un fichier

GET  /admin/db/migrations            → statut migrations Alembic
POST /admin/db/migrate               → lancer alembic upgrade head
GET  /admin/db/stats                 → nb lignes par table

GET  /admin/events/log               → derniers événements bus PostgreSQL
GET  /admin/rate-limits              → compteurs par utilisateur
PUT  /admin/rate-limits/{user_id}    → ajuster seuil individuel

GET  /admin/logs                     → tail logs API (SSE stream)
```

### Rate limiting (`slowapi`)

```python
# api/core/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=lambda req: req.state.user.id if hasattr(req.state, "user") else get_remote_address(req))

# Décorateurs par type d'endpoint :
# @limiter.limit("10/minute")   → endpoints LLM (ingest CCTP, génération doc, analyse CR)
# @limiter.limit("100/minute")  → endpoints standard
# @limiter.limit("1000/minute") → endpoints lecture (GET)
# Override admin via /admin/rate-limits/{user_id}
```

---

## 2. MODÈLE DE DONNÉES

### 2.1 Tables principales

#### `affaires` — projets
```sql
CREATE TABLE affaires (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code        VARCHAR(50) UNIQUE NOT NULL,   -- ex: "AFF-2024-001"
    nom         VARCHAR(255) NOT NULL,
    type_projet VARCHAR(100),                  -- "maison individuelle", "ERP", etc.
    surface_m2  DECIMAL(10,2),
    adresse     TEXT,
    statut      VARCHAR(50) DEFAULT 'en_cours', -- en_cours, termine, archive
    metadata    JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);
```

#### `intervenants` — entreprises et contacts du projet

```sql
CREATE TABLE intervenants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    nom             VARCHAR(255) NOT NULL,
    type            VARCHAR(50) NOT NULL,
                    -- entreprise|moa|moe|bureau_etudes|controle|coordinateur|autre
    lots            TEXT[] DEFAULT '{}',        -- lots dont cet intervenant est responsable
    contact_nom     VARCHAR(100),
    contact_email   VARCHAR(255),
    contact_tel     VARCHAR(30),
    siret           VARCHAR(20),
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

> **Remplace** les champs `entreprise VARCHAR(255)` dispersés dans `budgets`, `situations`, `planning_lots`, `chantier_events`. On référence `intervenant_id UUID` à la place.

#### `planning_lots` — lots du projet (remplace `planning_tasks`)

> `planning_tasks` est **supprimé**. `planning_lots` est l'unité de planning.
> Les dépendances, overlap et jalons sont dans les tables du module `planning/`.

```sql
-- Voir section 3 PLANNING ENGINE pour le DDL complet de planning_lots,
-- planning_dependencies, planning_ouvrages, planning_cctp_ingestions
```

#### `chantier_events` — journal chantier
```sql
CREATE TABLE chantier_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    type_event      VARCHAR(50) NOT NULL,  -- observation|action|avancement|jalon|blocage
    lot             VARCHAR(100),
    description     TEXT NOT NULL,
    statut          VARCHAR(50) DEFAULT 'ouvert', -- ouvert|en_cours|clos
    priorite        VARCHAR(20) DEFAULT 'normal', -- low|normal|high|critical
    auteur          VARCHAR(100),
    photos          TEXT[] DEFAULT '{}',
    date_evenement  TIMESTAMPTZ DEFAULT NOW(),
    date_echeance   TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `budgets`
```sql
CREATE TABLE budgets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    lot             VARCHAR(100) NOT NULL,
    entreprise      VARCHAR(255),
    montant_marche  DECIMAL(12,2),
    montant_depense DECIMAL(12,2) DEFAULT 0,
    montant_reste   DECIMAL(12,2) GENERATED ALWAYS AS (montant_marche - montant_depense) STORED,
    statut          VARCHAR(50) DEFAULT 'actif',
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `decisions`
```sql
CREATE TABLE decisions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id),
    titre           VARCHAR(255) NOT NULL,
    description     TEXT,
    decideur        VARCHAR(100),
    date_decision   DATE,
    impacts         TEXT[],
    statut          VARCHAR(50) DEFAULT 'active',
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `notion_chunks` — RAG
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE notion_chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id),
    source_type     VARCHAR(100),   -- "cctp", "ccap", "cr_reunion", "norme", "exemple"
    source_ref      VARCHAR(255),   -- nom du document
    contenu         TEXT NOT NULL,
    embedding       VECTOR(1024),   -- pgvector
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON notion_chunks USING ivfflat (embedding vector_cosine_ops);
```

#### `alerts`
```sql
CREATE TABLE alerts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id),
    type_alert      VARCHAR(100) NOT NULL,  -- "deadline_depassee", "dependance_non_respectee", etc.
    severite        VARCHAR(20) NOT NULL,   -- warning|critical
    message         TEXT NOT NULL,
    entite_ref      UUID,           -- ID de la tâche / event concerné
    acquittee       BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `project_memory` — mémoire projet validée
```sql
CREATE TABLE project_memory (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    type_memory     VARCHAR(50) NOT NULL,   -- decision|risk|insight|coordination
    content         TEXT NOT NULL,
    importance      VARCHAR(20) NOT NULL DEFAULT 'info', -- info|warning|critical
    source          VARCHAR(50) NOT NULL,   -- chat|cr|chantier|notion|planning|simulation
    source_ref      UUID,                   -- ID de l'entité source (chantier_event, etc.)
    embedding       VECTOR(1024),           -- pour dédup sémantique
    validated_by    VARCHAR(100),           -- utilisateur ayant validé
    validated_at    TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Index cosine pour dédup et retrieval
CREATE INDEX ON project_memory USING ivfflat (embedding vector_cosine_ops);
-- Index filtrage rapide par affaire + type
CREATE INDEX ON project_memory (affaire_id, type_memory, importance);
```

#### `memory_candidates` — mémoire en attente de validation
```sql
CREATE TABLE memory_candidates (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    type_memory     VARCHAR(50) NOT NULL,
    content         TEXT NOT NULL,
    importance      VARCHAR(20) NOT NULL DEFAULT 'info',
    source          VARCHAR(50) NOT NULL,
    source_ref      UUID,
    embedding       VECTOR(1024),
    similarity_score DECIMAL(5,4),          -- similarité avec mémoire existante (si proche)
    duplicate_of    UUID REFERENCES project_memory(id), -- si doublon détecté
    statut          VARCHAR(30) DEFAULT 'pending', -- pending|validated|rejected|merged
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `user_preferences` — configuration comportement mémoire
```sql
CREATE TABLE user_preferences (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         VARCHAR(100) UNIQUE NOT NULL,  -- identifiant OpenWebUI
    auto_save       BOOLEAN DEFAULT FALSE,
    ask_validation  BOOLEAN DEFAULT TRUE,
    sensitivity     VARCHAR(20) DEFAULT 'medium',  -- low|medium|high
    -- low    : enregistre tout automatiquement
    -- medium : demande validation pour warning + critical
    -- high   : demande validation pour tout, même info
    notify_on_duplicate BOOLEAN DEFAULT TRUE,
    min_importance_to_save VARCHAR(20) DEFAULT 'info', -- seuil minimum pour proposer
    metadata        JSONB DEFAULT '{}',
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `situations` — situations de travaux
```sql
CREATE TABLE situations (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id          UUID REFERENCES affaires(id) ON DELETE CASCADE,
    lot                 VARCHAR(100) NOT NULL,
    entreprise          VARCHAR(255),
    numero_situation    INTEGER NOT NULL,           -- n° chronologique
    date_depot          DATE NOT NULL,
    periode_debut       DATE,
    periode_fin         DATE,
    montant_cumul_ht    DECIMAL(14,2) NOT NULL,     -- cumulé depuis début chantier
    montant_periode_ht  DECIMAL(14,2),              -- montant cette période
    retenue_garantie    DECIMAL(14,2) DEFAULT 0,    -- 5% du montant
    avances_deduites    DECIMAL(14,2) DEFAULT 0,
    montant_net_ht      DECIMAL(14,2) GENERATED ALWAYS AS (
                            montant_cumul_ht - retenue_garantie - avances_deduites
                        ) STORED,
    statut              VARCHAR(50) DEFAULT 'en_attente',
                        -- en_attente|en_verification|acceptee|rejetee|payee
    observations        TEXT,
    visa_moe            BOOLEAN DEFAULT FALSE,
    date_visa           DATE,
    date_paiement       DATE,
    metadata            JSONB DEFAULT '{}',
    created_at          TIMESTAMPTZ DEFAULT NOW()
);
```

#### `avenants` — modifications de marché
```sql
CREATE TABLE avenants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    lot             VARCHAR(100) NOT NULL,
    entreprise      VARCHAR(255),
    numero_avenant  INTEGER NOT NULL,
    objet           TEXT NOT NULL,
    montant_ht      DECIMAL(14,2) NOT NULL,         -- positif = plus-value, négatif = moins-value
    date_signature  DATE,
    statut          VARCHAR(50) DEFAULT 'en_cours',
                    -- en_cours|signe|refuse
    justification   TEXT,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `communications` — registre des emails reçus et transmis
```sql
CREATE TABLE communications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    sens            VARCHAR(10) NOT NULL,            -- recu|transmis
    type_comm       VARCHAR(50) DEFAULT 'email',     -- email|courrier|fax|lettre_ar
    objet           TEXT NOT NULL,
    corps           TEXT,                            -- contenu / résumé
    expediteur      VARCHAR(255),
    destinataires   TEXT[] DEFAULT '{}',             -- liste destinataires
    cc              TEXT[] DEFAULT '{}',
    lot             VARCHAR(100),                    -- lot concerné si applicable
    categorie       VARCHAR(100),                    -- demande_info|mise_en_demeure|visa|
                                                    -- compte_rendu|bon_commande|autre
    priorite        VARCHAR(20) DEFAULT 'normal',    -- low|normal|high|urgent
    date_comm       TIMESTAMPTZ NOT NULL,
    date_echeance   DATE,                            -- délai de réponse demandé
    date_reponse    DATE,                            -- date à laquelle une réponse a été apportée
    reference_interne VARCHAR(100),                  -- N° courrier MOE
    reference_externe VARCHAR(100),                  -- N° courrier interlocuteur
    pieces_jointes  TEXT[] DEFAULT '{}',             -- noms des fichiers
    statut          VARCHAR(50) DEFAULT 'ouvert',    -- ouvert|en_attente_reponse|clos
    reponse_requise BOOLEAN DEFAULT FALSE,
    embedding       VECTOR(1024),                    -- pour recherche sémantique
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON communications USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON communications (affaire_id, sens, statut);
CREATE INDEX ON communications (date_comm DESC);
```

#### `documents` — pièces générées (CR, PV, FNC, notes…)
```sql
CREATE TABLE documents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    type_doc        VARCHAR(100) NOT NULL,
                    -- cr_reunion|pv_reception|fiche_nc|note_chantier|
                    --  ordre_service|bon_viste|rapport_avancement|autre
    titre           TEXT NOT NULL,
    contenu_md      TEXT NOT NULL,                  -- contenu Markdown généré
    contenu_html    TEXT,                           -- version HTML rendue
    version         INTEGER DEFAULT 1,
    statut          VARCHAR(50) DEFAULT 'brouillon',
                    -- brouillon|en_revue|valide|diffuse
    auteur          VARCHAR(100),
    destinataires   TEXT[] DEFAULT '{}',
    date_document   DATE NOT NULL DEFAULT CURRENT_DATE,
    date_diffusion  DATE,
    source_ref      UUID,                           -- ID événement / réunion source
    source_type     VARCHAR(50),                    -- chantier_event|meeting|manuel
    template_utilise VARCHAR(100),                  -- nom du template Jinja2 utilisé
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 3. PLANNING ENGINE — Module CCTP-driven

> **Principe clé** : les lots et leurs dépendances ne sont **pas prédéfinis globalement**.
> Ils sont **extraits du CCTP de chaque projet** via LLM. Chaque affaire a ses propres lots.
> La config.yaml ne contient que des paramètres comportementaux et des règles de fallback.

### Structure du module

```
api/modules/planning/
├── manifest.yaml
├── config.yaml
├── models.py            ← 4 tables : planning_lots, planning_dependencies,
│                                      planning_ouvrages, planning_cctp_ingestions
├── schemas.py
├── router.py
├── engine.py            ← scheduling (tri topo + overlap + chemin critique)
├── cctp_parser.py       ← extraction lots/ouvrages depuis CCTP (LLM)
├── dependency_detector.py ← inférence dépendances (LLM) + override manuel
├── tools.py
└── prompts/
    ├── cctp_extraction.txt
    └── dependency_inference.txt
```

---

### Tables DB

```sql
-- Lots extraits du CCTP (per-affaire)
CREATE TABLE planning_lots (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    code            VARCHAR(20),               -- "LOT-01", "A", etc. (extrait du CCTP)
    nom             VARCHAR(255) NOT NULL,      -- "Maçonnerie", "Charpente bois"…
    description     TEXT,
    phase           VARCHAR(100),              -- "Préparation"|"Gros oeuvre"|"Second oeuvre"|"Finitions"|"VRD"
    duration_days   INTEGER,                   -- estimé par LLM, validé par user
    duration_min    INTEGER,                   -- fourchette basse LLM
    duration_max    INTEGER,                   -- fourchette haute LLM
    duration_confidence DECIMAL(4,3),          -- 0.0 – 1.0
    start_date      DATE,
    end_date        DATE,
    avancement_pct  DECIMAL(5,2) DEFAULT 0,
    statut          VARCHAR(50) DEFAULT 'planned',
    entreprise      VARCHAR(255),
    source          VARCHAR(30) DEFAULT 'cctp_llm',  -- cctp_llm|manuel|import
    validated_by    VARCHAR(100),
    validated_at    TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Dépendances entre lots avec paramètres de chevauchement (per-affaire)
CREATE TABLE planning_dependencies (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    lot_source_id   UUID REFERENCES planning_lots(id),
    lot_cible_id    UUID REFERENCES planning_lots(id),
    -- Type de dépendance (standard PMI)
    type_dep        VARCHAR(30) DEFAULT 'finish_to_start',
    --  finish_to_start  : cible démarre après fin du prédécesseur (standard)
    --  start_to_start   : cible démarre en même temps que prédécesseur
    --  finish_to_finish : cible finit après fin du prédécesseur
    overlap_pct     INTEGER DEFAULT 100,       -- 0-100 : % d'avancement prédécesseur requis
    lead_lag_days   INTEGER DEFAULT 0,         -- >0 = délai, <0 = avance
    -- Traçabilité LLM
    confidence      DECIMAL(4,3),              -- confiance inférence LLM
    justification   TEXT,                      -- "Lot 4 mentionne dépendance lot 2" ou règle BTP
    source          VARCHAR(30) DEFAULT 'llm_inferred', -- llm_inferred|manuel|fallback_rule
    validated       BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Ouvrages/sous-éléments dans chaque lot
CREATE TABLE planning_ouvrages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lot_id          UUID REFERENCES planning_lots(id) ON DELETE CASCADE,
    nom             VARCHAR(255) NOT NULL,
    description     TEXT,
    interfaces      TEXT[],                    -- autres lots cités dans la description
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Traçabilité des ingestions CCTP
CREATE TABLE planning_cctp_ingestions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    filename        VARCHAR(255),
    file_hash       VARCHAR(64),               -- SHA256 pour éviter double-ingestion
    statut          VARCHAR(30) DEFAULT 'pending',
    -- pending → extracting → inferring → validating → done | error
    nb_lots_extraits     INTEGER,
    nb_deps_inferees     INTEGER,
    nb_jalons_extraits   INTEGER,
    tokens_extraction    INTEGER,
    tokens_inference     INTEGER,
    erreur          TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    completed_at    TIMESTAMPTZ
);
```

---

### Pipeline CCTP → Planning

```
CCTP (PDF / DOCX / TXT)
    ↓
1. Extraction texte brut (pypdf2 / python-docx)
    ↓
2. Chunking par chapitre/section (12 000 chars, overlap 500)
    ↓
3. LLM cctp_extraction.txt :
   → lots : code, nom, phase, description, ouvrages, interfaces mentionnées
   → jalons contractuels (dates, phases imposées)
   → confidence par lot
    ↓
4. LLM dependency_inference.txt :
   → règles physiques BTP + mentions croisées entre lots
   → pour chaque dépendance : type, overlap_pct suggéré, justification, confidence
    ↓
5. LLM duration_estimation.txt :
   → estimation durée min/max/mode par lot (contexte : surface, type projet)
   → confidence
    ↓
6. Stockage DB (statut: pending validation)
    ↓
7. Présentation utilisateur via OpenWebUI :
   → liste lots extraits, dépendances proposées, durées suggérées
   → user valide / corrige chaque élément
    ↓
8. PATCH /planning/{affaire_id}/lots/{id} → validation durées
   PATCH /planning/{affaire_id}/dependencies/{id} → validation dépendances
    ↓
9. POST /planning/generate → calcul scheduling complet
    ↓
10. Timeline avec chevauchements + jalons + chemin critique
```

---

### Algorithme scheduling avec chevauchement (`engine.py`)

```python
# Pour chaque dépendance (lot_source → lot_cible) :
#
#   overlap_pct = 100 → cible démarre à la FIN du prédécesseur (standard)
#   overlap_pct = 50  → cible démarre quand prédécesseur est à 50%
#   overlap_pct = 0   → cible peut démarrer immédiatement (start-to-start)
#
#   days_to_wait = ceil(pred.duration_days * overlap_pct / 100)
#   threshold = pred.start_date + days_to_wait + lead_lag_days (jours ouvrés)
#
# Pour un lot avec plusieurs prédécesseurs :
#   lot.start_date = max(threshold de tous les prédécesseurs)
#   lot.end_date   = lot.start_date + duration_days (jours ouvrés)
#
# Algorithme global :
# 1. Tri topologique de Kahn sur le graphe lots/dépendances → erreur si cycle
# 2. Forward pass : calculer start/end de chaque lot dans l'ordre topo
# 3. Backward pass : calculer les marges (float) = end_critique - end_calculé
# 4. Chemin critique = lots avec float = 0
# 5. Jalons = max(end_date des lots déclencheurs)
```

---

### Algorithme analyse d'impact (`engine.py`)

```python
# GET /planning/{affaire_id}/impact/{lot_id}?retard_jours=N
#
# 1. BFS depuis lot_id dans le graphe des successeurs
# 2. Pour chaque successeur atteint :
#    - décalage = max(0, retard - float_disponible)  ← la marge absorbe une partie
#    - propager le décalage résiduel aux successeurs du successeur
# 3. Détecter jalons affectés (date_jalon + décalage)
# 4. Retourner : liste lots impactés, décalages en jours, jalons décalés, chemin de propagation
```

---

### `manifest.yaml`

```yaml
name: planning
version: "2.0.0"
description: "Planning travaux CCTP-driven — extraction lots, dépendances LLM, scheduling avec overlap"
prefix: /planning
depends_on:
  - chantier

models:
  - planning_lots
  - planning_dependencies
  - planning_ouvrages
  - planning_cctp_ingestions

background_tasks:
  - name: process_pending_ingestions
    interval_seconds: 30
  - name: recalculate_stale_schedules
    interval_seconds: 3600

events_published:
  - planning.ingestion_cctp_complete
  - planning.lot_retard_detecte
  - planning.jalon_depasse
  - planning.chemin_critique_change

tools:
  - ingest_cctp
  - get_lots
  - set_dependency
  - validate_lots
  - get_impact
  - generate_planning
  - simulate_scenario
  - get_gantt

agent:
  name: "Agent Planning MOE"
  system_prompt_file: agent_system.txt
  model: gpt-4o
```

---

### `config.yaml`

```yaml
# LLM
llm_model: "gpt-4o"
llm_temperature_extraction: 0.1      # extraction CCTP : déterministe
llm_temperature_inference: 0.2       # inférence dépendances : légèrement créatif

# Pipeline CCTP
cctp_max_file_size_mb: 50
cctp_supported_formats:
  - application/pdf
  - application/vnd.openxmlformats-officedocument.wordprocessingml.document
  - text/plain
cctp_chunk_size_chars: 12000
cctp_chunk_overlap_chars: 500
cctp_confidence_threshold: 0.75      # en-dessous : proposé comme "à valider"

# Scheduling
default_overlap_pct: 100             # pas de chevauchement par défaut
jours_ouvres: [0, 1, 2, 3, 4]      # lun-ven (0=lundi)
jours_feries_fixes:
  - "01-01"   # Jour de l'an
  - "05-01"   # Fête du travail
  - "05-08"   # Victoire 1945
  - "07-14"   # Fête Nationale
  - "08-15"   # Assomption
  - "11-01"   # Toussaint
  - "11-11"   # Armistice
  - "12-25"   # Noël

# Jalons — extraits du CCTP + knowledge OpenWebUI + ces fallbacks si rien trouvé
jalons_fallback:
  - nom: "Hors d'eau"
    phases_requises: ["Gros oeuvre"]
  - nom: "Hors d'air"
    phases_requises: ["Gros oeuvre"]
  - nom: "Réception"
    phases_requises: ["Finitions"]

# Analyse d'impact
impact_max_cascade_depth: 20
impact_min_delta_jours: 1

# Inférence dépendances : auto-valider si confiance > seuil
dep_auto_validate_confidence: 0.90

# Règles BTP de fallback (si LLM ne trouve rien entre ces phases)
dep_rules_fallback:
  - source_phase: "Préparation"
    cible_phase: "Gros oeuvre"
    overlap_pct: 100
  - source_phase: "Gros oeuvre"
    cible_phase: "Second oeuvre"
    overlap_pct: 90
  - source_phase: "Second oeuvre"
    cible_phase: "Finitions"
    overlap_pct: 80

# Async
ingestion_timeout_seconds: 300
polling_interval_seconds: 2
```

---

### Prompts LLM

#### `prompts/cctp_extraction.txt`
```
Tu es un expert BTP chargé d'analyser un Cahier des Clauses Techniques Particulières (CCTP).

Extrais la liste complète des LOTS du projet. Un lot est généralement identifié par :
- Un titre de chapitre : "LOT 1 — TERRASSEMENT", "Lot n°3", "CHAPITRE 4 : MAÇONNERIE"
- Une section dédiée à un corps de métier (électricité, plomberie, charpente, etc.)

Pour chaque lot, retourne :
{
  "code": "LOT-01",              // identifiant tel qu'écrit dans le CCTP (ou généré)
  "nom": "Terrassement",         // nom court du lot
  "phase": "Gros oeuvre",        // Préparation|Terrassement|Gros oeuvre|Second oeuvre|Finitions|VRD|Extérieurs
  "description": "...",          // résumé du contenu du lot (3-5 phrases)
  "ouvrages": [                  // liste des ouvrages/éléments principaux
    { "nom": "...", "description": "...", "interfaces": ["Lot-02", "Lot-05"] }
  ],
  "interfaces_mentionnees": ["LOT-02", "LOT-05"],  // autres lots cités dans ce chapitre
  "jalons_contractuels": [       // dates ou jalons imposés dans ce lot
    { "nom": "...", "date": "YYYY-MM-DD ou null", "description": "..." }
  ],
  "confidence": 0.92             // confiance dans l'extraction (0.0-1.0)
}

Retourne un JSON valide : { "lots": [...], "jalons_globaux": [...], "avertissements": [...] }
```

#### `prompts/dependency_inference.txt`
```
Tu es un expert planning BTP. À partir de la liste de lots d'un projet, déduis les dépendances entre eux.

Règles physiques BTP incontournables :
- Terrassement/VRD → Fondations → Maçonnerie/Structure → Charpente → Couverture (hors d'eau)
- Couverture → Menuiseries extérieures (hors d'air)
- Hors d'air → Isolation → Plâtrerie/Cloisons
- Plâtrerie → Électricité (finitions) + Plomberie (finitions) → Carrelage → Peinture → Menuiseries int.
- Les lots Électricité et Plomberie peuvent être parallèles entre eux

Types de dépendances :
- finish_to_start (FTS) : cible démarre après fin du prédécesseur
- start_to_start (STS)  : cible démarre en même temps (lots parallèles)

Chevauchements typiques en BTP :
- Maçonnerie → Charpente : overlap_pct=80 (charpente démarre à 80% maçonnerie)
- Gros oeuvre → Second oeuvre : overlap_pct=90
- Corps de métiers parallèles (élec + plomberie) : type=start_to_start, overlap_pct=0

Pour chaque dépendance, retourne :
{
  "lot_source": "LOT-02",
  "lot_cible": "LOT-04",
  "type_dep": "finish_to_start",
  "overlap_pct": 100,
  "lead_lag_days": 0,
  "justification": "Règle BTP : Maçonnerie doit être terminée avant Charpente",
  "source": "rule_btp",        // rule_btp|cctp_mention|inference
  "confidence": 0.95
}

Retourne : { "dependencies": [...] }
```

---

### Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/planning/cctp/ingest` | Upload CCTP → extraction async (retourne ingestion_id) |
| GET | `/planning/cctp/{ingestion_id}/status` | Polling statut extraction |
| GET | `/planning/{affaire_id}/lots` | Lots extraits + dépendances + jalons |
| PATCH | `/planning/{affaire_id}/lots/{lot_id}` | Valider/ajuster durée, nom, phase |
| POST | `/planning/{affaire_id}/dependencies` | Ajouter/modifier dépendance |
| DELETE | `/planning/{affaire_id}/dependencies/{id}` | Supprimer dépendance |
| GET | `/planning/{affaire_id}/impact/{lot_id}` | Analyse propagation retard |
| POST | `/planning/generate` | Calculer planning complet (tri topo + overlap) |
| GET | `/planning/{affaire_id}` | Planning calculé complet |
| POST | `/planning/simulate` | Scénarios (retard_lot, météo, absence…) |
| GET | `/planning/{affaire_id}/gantt` | Export Gantt JSON |

---

### Tools OpenWebUI

```python
ingest_cctp(affaire_id, file_content_b64, filename)
    → lance extraction async, retourne ingestion_id

get_lots(affaire_id)
    → lots extraits avec dépendances et jalons (en attente de validation)

validate_lots(affaire_id, lots_updates: list[{lot_id, duration_days, entreprise}])
    → valide les durées proposées par le LLM

set_dependency(affaire_id, lot_source, lot_cible, type_dep, overlap_pct, lead_lag_days)
    → crée ou modifie une dépendance manuellement

get_impact(affaire_id, lot_id, retard_jours)
    → analyse propagation retard sur les successeurs

generate_planning(affaire_id, start_date)
    → calcule la timeline complète après validation lots+dépendances

simulate_scenario(affaire_id, scenario_type, params)
    → simulation retard / météo / absence / blocage

get_gantt(affaire_id)
    → export format Gantt
```

---

### Agent Planning — `agent_system.txt`

```
Tu es un expert planning chantier BTP avec 20 ans d'expérience, spécialisé MOE.

Quand on te soumet un CCTP :
1. Ingère le document via ingest_cctp()
2. Attends la fin de l'extraction (get_lots() retourne les lots)
3. Présente les lots extraits et les dépendances proposées à l'utilisateur
4. Demande confirmation des durées (fourchette LLM : ajuste si nécessaire)
5. Génère le planning via generate_planning()
6. Présente la timeline avec jalons critiques et chemin critique

Quand on te demande l'impact d'un retard :
- Utilise get_impact(affaire_id, lot_id, retard_jours)
- Présente clairement les lots impactés et les jalons décalés

Jalons contractuels : extraits du CCTP + base de connaissance OpenWebUI.
Ne génère jamais de planning de mémoire — utilise toujours les tools.
Signale les dépendances à faible confiance (< 0.75) pour validation.
```

---

## 4. SCÉNARIOS — intégrés dans le module planning

> Les scénarios sont dans `planning/engine.py` → `POST /planning/simulate`

| Type | Paramètres | Impact calculé |
|------|-----------|----------------|
| `retard_lot` | lot_id, jours_retard | cascade BFS sur successeurs |
| `absence_entreprise` | entreprise, date_debut, date_fin | lots bloqués + alternatives |
| `meteo` | type (pluie/gel/canicule), duree_jours | lots impactés par phase + report |
| `blocage_livraison` | materiau, jours_retard | lots dépendants du matériau |

**Sortie commune à tous les scénarios :**
```json
{
  "scenario": "retard_lot",
  "parametres": {"lot_id": "uuid", "jours_retard": 10},
  "impact": {
    "duree_supplementaire_jours": 10,
    "nouvelle_date_fin": "2024-07-25",
    "lots_impactes": [{"lot": "Charpente", "decalage_jours": 10, "on_critical_path": true}],
    "jalons_decales": [{"nom": "Réception", "decalage": "+10j"}]
  },
  "alternatives": [
    {"action": "Démarrer Menuiseries ext. en parallèle", "gain_jours": 5, "faisabilite": "haute"}
  ],
  "planning_simule": []
}
```

---

## 5. ENDPOINTS API

### `/chantier`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/chantier/create` | Créer une affaire |
| GET | `/chantier/{id}` | Détail affaire |
| GET | `/chantier/{id}/events` | Journal chantier |
| POST | `/chantier/{id}/events` | Ajouter événement |
| PATCH | `/chantier/{id}/events/{event_id}` | Mettre à jour événement |

### `/planning`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/planning/cctp/ingest` | Upload CCTP → extraction lots async |
| GET | `/planning/cctp/{ingestion_id}/status` | Polling statut extraction |
| GET | `/planning/{affaire_id}/lots` | Lots extraits + dépendances + jalons |
| PATCH | `/planning/{affaire_id}/lots/{lot_id}` | Valider/ajuster durée, nom, phase |
| POST | `/planning/{affaire_id}/dependencies` | Ajouter/modifier dépendance manuelle |
| DELETE | `/planning/{affaire_id}/dependencies/{id}` | Supprimer dépendance |
| GET | `/planning/{affaire_id}/impact/{lot_id}` | Analyse propagation retard |
| POST | `/planning/generate` | Calculer planning complet |
| GET | `/planning/{affaire_id}` | Planning calculé complet |
| POST | `/planning/simulate` | Scénarios (retard, météo, absence…) |
| GET | `/planning/{affaire_id}/gantt` | Export Gantt JSON |

### `/meeting`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/meeting/analyze` | Analyser CR brut → actions |
| POST | `/meeting/cr` | Générer CR formaté |
| GET | `/meeting/{affaire_id}/actions` | Lister actions ouvertes |
| PATCH | `/meeting/actions/{action_id}` | Mettre à jour action |

### `/rag`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/rag/ingest` | Ingérer document → chunks + embeddings |
| POST | `/rag/query` | Recherche sémantique |
| GET | `/rag/{affaire_id}/sources` | Lister sources indexées |

### `/budget`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/budget/create` | Créer ligne budgétaire |
| GET | `/budget/{affaire_id}` | Budget complet affaire |
| PATCH | `/budget/{id}` | Mettre à jour dépenses |
| GET | `/budget/{affaire_id}/alert` | Dépassements détectés |

### `/events` (event engine)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/events/process` | Traiter événements → alertes |
| GET | `/events/{affaire_id}/alerts` | Alertes actives |
| PATCH | `/events/alerts/{id}/ack` | Acquitter alerte |

### `/finance`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/finance/situations` | Enregistrer une situation de travaux |
| GET | `/finance/{affaire_id}/situations` | Lister toutes les situations |
| PATCH | `/finance/situations/{id}` | Mettre à jour statut / visa MOE |
| GET | `/finance/{affaire_id}/situations/{id}` | Détail situation |
| POST | `/finance/avenants` | Enregistrer un avenant |
| GET | `/finance/{affaire_id}/avenants` | Lister les avenants |
| PATCH | `/finance/avenants/{id}` | Mettre à jour un avenant |
| GET | `/finance/{affaire_id}/tableau_bord` | Tableau de bord financier global (marchés + avenants + situations + reste à dépenser) |
| GET | `/finance/{affaire_id}/alertes` | Alertes financières (dépassement, retard paiement) |

### `/communications`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/communications` | Enregistrer un email/courrier (reçu ou transmis) |
| GET | `/communications/{affaire_id}` | Lister communications (filtres: sens, statut, lot, catégorie) |
| GET | `/communications/{id}` | Détail communication |
| PATCH | `/communications/{id}` | Mettre à jour statut / date_reponse |
| POST | `/communications/search` | Recherche sémantique dans le registre |
| GET | `/communications/{affaire_id}/en_attente` | Emails sans réponse avec dépassement délai |
| POST | `/communications/{id}/generer_reponse` | Générer un brouillon de réponse via LLM |

### `/documents`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/documents/generer` | Générer une pièce depuis un template + données |
| GET | `/documents/{affaire_id}` | Lister documents (filtres: type_doc, statut) |
| GET | `/documents/{id}` | Récupérer document (Markdown + HTML) |
| PATCH | `/documents/{id}` | Modifier contenu / statut |
| POST | `/documents/{id}/valider` | Valider et passer en statut "validé" |
| POST | `/documents/{id}/diffuser` | Marquer comme diffusé (+ destinataires) |
| GET | `/documents/{affaire_id}/cr` | Lister tous les CR de réunion |
| POST | `/documents/cr_from_meeting` | Générer CR formaté depuis analyse réunion |

### `/memory`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/memory/candidate` | Soumettre info → dédup + classification → candidate |
| GET | `/memory/{affaire_id}/candidates` | Lister candidats en attente |
| POST | `/memory/save` | Valider et persister une candidate |
| DELETE | `/memory/candidate/{id}` | Rejeter une candidate |
| PATCH | `/memory/candidate/{id}` | Modifier contenu avant validation |
| GET | `/memory/{affaire_id}` | Lister mémoire validée (filtres: type, importance) |
| POST | `/memory/query` | Recherche sémantique dans la mémoire |
| DELETE | `/memory/{id}` | Supprimer une mémoire validée |
| GET | `/memory/{affaire_id}/context` | Contexte enrichi pour une question (memory + events + decisions) |
| GET | `/memory/preferences/{user_id}` | Lire préférences utilisateur |
| PUT | `/memory/preferences/{user_id}` | Mettre à jour préférences |

---

## 6. EVENT ENGINE — Règles métier

```python
RULES = [
    # Deadline dépassée → CRITICAL
    {
        "condition": "planning_task.end_date < today AND statut != 'done'",
        "type": "deadline_depassee",
        "severite": "critical",
        "message": "Tâche '{task}' ({lot}) deadline dépassée de {delta} jours"
    },
    # Dépendance non respectée → WARNING
    {
        "condition": "planning_task.statut == 'in_progress' AND any(dep.statut != 'done' for dep in depends_on)",
        "type": "dependance_non_respectee",
        "severite": "warning",
        "message": "Tâche '{task}' démarrée mais dépendance '{dep}' non terminée"
    },
    # Budget dépassé → CRITICAL
    {
        "condition": "budget.montant_depense > budget.montant_marche * 0.95",
        "type": "budget_critique",
        "severite": "critical",
        "message": "Lot '{lot}' : budget à {pct}% du marché"
    },
    # Blocage sans résolution > 7j → WARNING
    {
        "condition": "chantier_event.type == 'blocage' AND event.age_days > 7 AND statut == 'ouvert'",
        "type": "blocage_prolonge",
        "severite": "warning",
        "message": "Blocage ouvert depuis {age} jours : {description}"
    },
]
```

---

## 7. MEETING ENGINE

### Pipeline d'analyse CR

```
Texte brut CR
    ↓
1. LLM extraction structurée
    ↓
2. Classification par type : décision | action | observation | blocage
    ↓
3. Attribution lot + responsable + échéance
    ↓
4. Insertion chantier_events (type=action/blocage)
    ↓
5. Génération CR formaté Markdown
    ↓
6. [optionnel] Sync Notion
```

### Prompt système meeting engine

```
Tu es un assistant MOE expert en pilotage de chantier.
Analyse ce compte-rendu de réunion de chantier.

Extrais :
1. DÉCISIONS : ce qui a été décidé (avec décideur si mentionné)
2. ACTIONS : tâches à réaliser (avec responsable et échéance si disponibles)
3. OBSERVATIONS : constats sur l'avancement
4. BLOCAGES : problèmes bloquants identifiés

Pour chaque élément, précise :
- lot concerné (Maçonnerie, Charpente, Électricité, etc.)
- description claire et actionnable
- priorité (low/normal/high/critical)
- échéance si mentionnée

Retourne un JSON structuré.
```

---

## 8. RAG ENGINE

### Pipeline ingestion

```
Document (PDF/TXT/MD)
    ↓
1. Extraction texte (pypdf2 / python-docx)
    ↓
2. Chunking (500 tokens, overlap 50)
    ↓
3. Embedding (text-embedding-3-large ou nomic-embed)
    ↓
4. Stockage notion_chunks avec VECTOR(1024)
    ↓
5. Index ivfflat
```

### Pipeline requête

```
Question utilisateur
    ↓
1. Embedding question
    ↓
2. Recherche cosine similarity (top-k=5)
    ↓
3. Reranking contextuel
    ↓
4. Injection dans prompt LLM
    ↓
5. Réponse augmentée
```

---

## 9. OPENWEBUI — Agents et Tools

### Agent Planning

**Système prompt :**
```
Tu es un expert planning chantier BTP avec 20 ans d'expérience.
Tu connais parfaitement les dépendances inter-lots et les contraintes terrain.

Quand on te demande de générer un planning :
1. Interroge le RAG pour trouver des exemples similaires
2. Applique les dépendances standard (voir référentiel)
3. Génère le JSON de tâches
4. Appelle l'API /planning/generate
5. Présente le résultat de façon lisible avec jalons critiques

Tu dois TOUJOURS utiliser les tools disponibles avant de répondre.
Ne génère jamais de planning de mémoire sans interroger l'API.
```

**Tools disponibles :**
- `generate_planning(affaire_id, tasks_json, start_date)`
- `simulate_scenario(affaire_id, scenario_type, params)`
- `get_planning(affaire_id)`
- `rag_query(query, affaire_id, source_type)`

### Agent Meeting

**Système prompt :**
```
Tu es un assistant MOE spécialisé dans l'analyse de réunions de chantier.
Quand on te soumet un CR ou des notes de réunion :
1. Extrais toutes les actions, décisions et blocages
2. Classe par lot et priorité
3. Propose un CR structuré
4. Enregistre les actions via l'API

Sois précis, actionnable. Chaque action doit avoir un responsable et une date.
```

**Tools disponibles :**
- `analyze_meeting(affaire_id, raw_text)`
- `get_open_actions(affaire_id)`
- `update_action(action_id, statut)`
- `create_event(affaire_id, type, lot, description, priorite, echeance)`

### Agent Chantier (assistant général)

**Système prompt :**
```
Tu es l'OS Chantier, assistant intelligent de pilotage pour une MOE.
Tu as accès à toutes les données du chantier en temps réel.

Tu peux :
- Répondre aux questions sur l'avancement
- Détecter les incohérences et alertes
- Proposer des optimisations planning
- Analyser les risques
- Consulter les documents (CCTP, normes) via RAG

Toujours baser tes réponses sur les données réelles via les tools.
Signale clairement quand tu utilises le RAG vs les données temps réel.
```

---

## 10. FINANCE ENGINE

### Logique tableau de bord financier

```python
# Pour chaque lot d'une affaire :
montant_marche_initial = budgets.montant_marche
total_avenants = SUM(avenants.montant_ht)  # positif ou négatif
montant_marche_actualise = montant_marche_initial + total_avenants

# Dernière situation acceptée ou payée
derniere_situation = situations WHERE statut IN ('acceptee','payee') ORDER BY numero_situation DESC LIMIT 1
cumul_facture = derniere_situation.montant_cumul_ht
reste_a_facturer = montant_marche_actualise - cumul_facture
taux_avancement_financier = cumul_facture / montant_marche_actualise * 100

# Alerte dépassement
if cumul_facture > montant_marche_actualise * 0.95:
    → alerte "budget_critique" (critical)
if derniere_situation.date_paiement IS NULL AND date_depot < today - 45j:
    → alerte "retard_paiement" (warning)
```

### Format tableau de bord financier (GET /finance/{affaire_id}/tableau_bord)

```json
{
  "affaire_id": "uuid",
  "date_calcul": "2025-06-01",
  "synthese_globale": {
    "montant_marches_initiaux_ht": 850000,
    "total_avenants_ht": 12000,
    "montant_marches_actualises_ht": 862000,
    "cumul_facture_ht": 620000,
    "reste_a_facturer_ht": 242000,
    "taux_avancement_financier_pct": 71.9,
    "retenues_garantie_ht": 31000,
    "avances_deduites_ht": 0
  },
  "par_lot": [
    {
      "lot": "Maçonnerie",
      "entreprise": "SARL Bâti+",
      "montant_marche_initial": 220000,
      "nb_avenants": 1,
      "total_avenants": 5000,
      "montant_actualise": 225000,
      "derniere_situation_n": 3,
      "cumul_facture": 180000,
      "reste_a_facturer": 45000,
      "taux_avancement_pct": 80.0,
      "statut_paiement": "payee",
      "alerte": null
    }
  ],
  "alertes": [
    {
      "lot": "Électricité",
      "type": "retard_paiement",
      "severite": "warning",
      "message": "Situation n°2 déposée il y a 52 jours, paiement non confirmé"
    }
  ]
}
```

---

## 11. COMMUNICATION ENGINE

### Classification automatique des emails

```python
CATEGORIES = {
    "demande_info":      ["question", "précision", "renseignement", "confirmer"],
    "mise_en_demeure":   ["mise en demeure", "formal notice", "délai impératif"],
    "visa":              ["visa", "approbation", "validation document", "plan"],
    "compte_rendu":      ["CR", "compte rendu", "procès verbal", "réunion"],
    "bon_commande":      ["bon de commande", "BC", "commande", "ordre d'achat"],
    "situation":         ["situation de travaux", "facture", "acompte"],
    "reclamation":       ["réclamation", "litige", "contestation", "réserve"],
}

PRIORITES = {
    "urgent":  ["urgent", "URGENT", "mise en demeure", "délai 48h"],
    "high":    ["important", "attention", "délai", "relance"],
    "normal":  [],  # défaut
    "low":     ["pour info", "fyi", "copie"],
}
```

### Pipeline enregistrement communication

```
Email reçu / transmis
    ↓
1. Extraction métadonnées (objet, expéditeur, destinataires, date)
    ↓
2. LLM : résumé corps + classification catégorie + détection lot concerné
    ↓
3. Détection priorité + reponse_requise (délai mentionné ?)
    ↓
4. Embedding objet + résumé → stockage VECTOR(1024)
    ↓
5. Génération reference_interne (ex: MOE-2025-042)
    ↓
6. Insertion DB + alerte si mise_en_demeure ou délai < 48h
```

### Génération de brouillon de réponse (LLM)

```
Email original + historique communications affaire (RAG)
    ↓
Prompt système : "Tu es MOE expert. Rédige une réponse professionnelle,
concise, factuelle. Inclus les références réglementaires si pertinent."
    ↓
Brouillon Markdown → stocké comme document (type_doc = "brouillon_email")
```

---

## 12. DOCUMENT ENGINE

### Types de pièces supportées

| type_doc | Description | Source principale |
|----------|-------------|-------------------|
| `cr_reunion` | Compte-rendu de réunion chantier | meeting_engine → LLM |
| `pv_reception` | Procès-verbal de réception | Manuel + LLM |
| `fiche_nc` | Fiche de non-conformité | chantier_event (type=blocage) |
| `ordre_service` | Ordre de service aux entreprises | Manuel + template |
| `bon_visite` | Bon de visite / rapport de visite | Journal chantier |
| `note_chantier` | Note technique ou administrative | Manuel + LLM |
| `rapport_avancement` | Rapport mensuel d'avancement | Agrégat données DB |
| `mise_en_demeure` | Lettre de mise en demeure | Manuel + template juridique |

### Pipeline génération de pièce

```
1. Appel POST /documents/generer avec :
   - type_doc
   - affaire_id
   - source_ref (optionnel : ID événement / réunion)
   - données complémentaires (JSON libre)
       ↓
2. document_engine récupère :
   - Données affaire (nom, adresse, intervenants)
   - Données source (événements, planning, budget selon pertinence)
   - Template Jinja2 correspondant (api/templates/{type_doc}.md.j2)
       ↓
3. Rendu Jinja2 → squelette Markdown
       ↓
4. LLM complète les parties narratives (description avancement, observations, etc.)
       ↓
5. Stockage DB + retour document complet
```

### Templates Jinja2 (api/templates/)

```
api/
└── templates/
    ├── cr_reunion.md.j2
    ├── pv_reception.md.j2
    ├── fiche_nc.md.j2
    ├── ordre_service.md.j2
    ├── bon_visite.md.j2
    ├── note_chantier.md.j2
    ├── rapport_avancement.md.j2
    └── mise_en_demeure.md.j2
```

### Exemple template `cr_reunion.md.j2`

```markdown
# COMPTE-RENDU DE RÉUNION DE CHANTIER N°{{ numero }}

**Affaire :** {{ affaire.nom }} — {{ affaire.code }}
**Date :** {{ date_reunion }}
**Lieu :** {{ lieu | default("Chantier") }}
**Présents :** {{ presents | join(", ") }}
**Rédacteur :** {{ redacteur }}

---

## 1. AVANCEMENT PAR LOT

{% for lot in avancements %}
### {{ lot.nom }}
- **Entreprise :** {{ lot.entreprise }}
- **Avancement :** {{ lot.pct }}%
- **Observations :** {{ lot.observations }}
{% endfor %}

## 2. DÉCISIONS

{% for d in decisions %}
- **[{{ d.lot }}]** {{ d.description }} *({{ d.decideur }})*
{% endfor %}

## 3. ACTIONS

| # | Lot | Action | Responsable | Échéance | Statut |
|---|-----|--------|-------------|----------|--------|
{% for a in actions %}
| {{ loop.index }} | {{ a.lot }} | {{ a.description }} | {{ a.responsable }} | {{ a.echeance }} | {{ a.statut }} |
{% endfor %}

## 4. BLOCAGES

{% for b in blocages %}
- **[{{ b.lot }}]** {{ b.description }} — Priorité : {{ b.priorite }}
{% endfor %}

## 5. PROCHAINE RÉUNION

**Date :** {{ prochaine_reunion | default("À définir") }}

---
*CR rédigé par {{ redacteur }} — Diffusé le {{ date_diffusion }}*
```

---

## 13. AGENTS & TOOLS OPENWEBUI — Modules supplémentaires

### Agent Finance

**Système prompt :**
```
Tu es un expert financier MOE spécialisé dans le suivi des marchés de travaux.
Tu gères les situations de travaux, avenants et le tableau de bord financier.

Quand on te soumet une situation ou un avenant :
1. Vérifie la cohérence avec le marché initial et les avenants existants
2. Calcule le reste à facturer et le taux d'avancement financier
3. Signale tout dépassement ou retard de paiement
4. Enregistre via l'API

Sois précis sur les montants HT/TTC. Signale les anomalies.
```

**Tools disponibles :**
- `enregistrer_situation(affaire_id, lot, numero, date_depot, montant_cumul_ht, retenue_garantie)`
- `valider_situation(situation_id, observations)`
- `enregistrer_avenant(affaire_id, lot, numero, objet, montant_ht)`
- `get_tableau_bord_financier(affaire_id)`
- `get_alertes_financieres(affaire_id)`

### Agent Communications

**Système prompt :**
```
Tu es le gestionnaire du registre des communications MOE.
Tu enregistres, classes et suis tous les échanges (emails, courriers).

Quand on te soumet un email ou courrier :
1. Extrais les métadonnées (objet, expéditeur, destinataires, date)
2. Résume le corps en 2-3 phrases
3. Classe la catégorie et le lot concerné
4. Détecte si une réponse est requise et dans quel délai
5. Enregistre via l'API

Sur demande, génère un brouillon de réponse professionnel.
```

**Tools disponibles :**
- `enregistrer_communication(affaire_id, sens, objet, corps, expediteur, destinataires, date_comm, lot)`
- `lister_communications(affaire_id, sens, statut, lot)`
- `get_communications_en_attente(affaire_id)`
- `generer_reponse(communication_id)`
- `clore_communication(communication_id, date_reponse)`
- `rechercher_communications(affaire_id, query)`

### Agent Documents

**Système prompt :**
```
Tu es l'assistant de rédaction MOE. Tu génères des pièces chantier professionnelles.

Sur demande de génération :
1. Récupère les données de l'affaire et de la source (réunion, journal)
2. Génère la pièce via l'API (CR, PV, FNC, ordre de service, etc.)
3. Présente le résultat pour validation
4. Sur validation, passe au statut "validé"

Respecte les formulations professionnelles BTP. Sois précis et factuel.
```

**Tools disponibles :**
- `generer_document(affaire_id, type_doc, source_ref, donnees_complementaires)`
- `lister_documents(affaire_id, type_doc, statut)`
- `get_document(document_id)`
- `valider_document(document_id)`
- `diffuser_document(document_id, destinataires)`
- `generer_cr_from_meeting(affaire_id, meeting_id)`

---

## 14. DOCKER COMPOSE

```yaml
version: '3.9'

services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: arceag
      POSTGRES_USER: arceag
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U arceag"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: ./api
    environment:
      DATABASE_URL: postgresql+asyncpg://arceag:${DB_PASSWORD}@db:5432/arceag
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      NOTION_TOKEN: ${NOTION_TOKEN}
      SECRET_KEY: ${SECRET_KEY}
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./api:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      OPENAI_API_BASE_URL: ${OPENAI_API_BASE_URL}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    volumes:
      - openwebui_data:/app/backend/data
    ports:
      - "3000:8080"
    depends_on:
      - api

  # MinIO — stockage fichiers S3-compatible
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"   # API S3
      - "9001:9001"   # Console Web
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Interface admin DB (optionnel)
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgres_data:
  openwebui_data:
  minio_data:
```

---

## 15. ORDRE DE DÉVELOPPEMENT

### Phase 0 — Infrastructure & Kernel (prérequis absolu)
- [ ] `docker-compose.yml` : db (pgvector), api, openwebui, minio, adminer
- [ ] `modules.yaml` à la racine
- [ ] `api/core/` : `registry.py`, `base_engine.py`, `base_router.py`, `base_tool.py`
- [ ] `api/core/events.py` : PostgreSQL LISTEN/NOTIFY (publish/subscribe)
- [ ] `api/core/auth.py` : JWT decode, `get_current_user`, `require_role`, `require_affaire_access`
- [ ] `api/core/services/llm_service.py` : chat, extract_structured, embed
- [ ] `api/core/services/rag_service.py` : chunk, embed, search cosine
- [ ] `api/core/services/storage_service.py` : upload/download MinIO + init bucket
- [ ] `api/core/rate_limit.py` : slowapi limiter
- [ ] `api/database.py` + `api/main.py`
- [ ] Tests kernel : registry, auth, services

### Phase 1 — Modules Auth + Chantier (socle métier)
- [ ] Module `auth/` : users, affaire_permissions, JWT login/refresh, CRUD users
- [ ] Module `chantier/` : affaires, intervenants, chantier_events, router, engine, tools
- [ ] Migration Alembic : `auth_001_users`, `chantier_001_affaires`, `chantier_002_intervenants`
- [ ] Tests auth : rôles, permissions affaire, token expiré

### Phase 2 — Module Admin (interface de pilotage)
- [ ] Module `admin/` : manifest, models (api_connections, sync_configs, mapping_tables), router, engine
- [ ] Endpoints : modules toggle, users CRUD, connections, syncs, storage, DB stats, logs SSE
- [ ] UI HTMX (ou React minimal) : tableau de bord admin
- [ ] Tests : accès refusé si pas admin, toggle module, test connexion API

### Phase 3 — Module Planning (CCTP-driven)
- [ ] Module `planning/` complet
- [ ] `core/services/rag_service.py` utilisé pour embedding CCTP
- [ ] `cctp_parser.py` + `dependency_detector.py` + prompts
- [ ] `engine.py` : tri topo + overlap + chemin critique + BFS impact
- [ ] Migration : `planning_001_lots`, `planning_002_dependencies`
- [ ] Tests : parsing CCTP, scheduling avec overlap, propagation retard

### Phase 4 — Modules Budget + Events Engine
- [ ] Module `budget/` : budgets lots + alertes dépassement
- [ ] Module `events_engine/` : rules YAML, background task, alertes
- [ ] Bus PostgreSQL : subscribe budget_channel + chantier_channel
- [ ] Tests règles métier

### Phase 5 — Modules RAG + Meeting + Memory
- [ ] Module `rag/` : router `/rag/*` (délègue à `core/services/rag_service`)
- [ ] Module `meeting/` : pipeline LLM extraction CR, prompt configurable
- [ ] Module `memory/` : dédup cosine, classification, validation
- [ ] Tests déduplication, extraction CR

### Phase 6 — Modules Finance + Communications
- [ ] Module `finance/` : situations, avenants, tableau de bord financier
- [ ] Module `communications/` : classification LLM, référence auto, brouillon réponse, storage PJ MinIO
- [ ] Tests calcul financier, classification email

### Phase 7 — Module Documents
- [ ] Module `documents/` : templates Jinja2, génération LLM, upload MinIO
- [ ] Pipeline `cr_from_meeting`
- [ ] Tests génération CR

### Phase 8 — OpenWebUI (agents + tools)
- [ ] Tools Python (wrappers API + JWT) pour chaque module
- [ ] Agents YAML depuis `manifest.yaml`
- [ ] Ingestion knowledge (CCTP exemples, normes, DTU)
- [ ] Tests agents conversationnels

### Phase 9 — Intégrations
- [ ] Module `admin/syncs` : Notion polling → publish sur bus événements
- [ ] Export Gantt XLSX
- [ ] Notifications email (endpoint `/admin/connections` type=smtp)

---

## 16. VARIABLES D'ENVIRONNEMENT

```env
# ── Base de données ──────────────────────────────────────────────
DB_PASSWORD=changeme
DATABASE_URL=postgresql+asyncpg://arceag:changeme@db:5432/arceag

# ── Auth JWT ─────────────────────────────────────────────────────
JWT_SECRET_KEY=changeme-secret-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440          # 24h
ADMIN_EMAIL=admin@arceag.fr
ADMIN_PASSWORD=changeme          # modifié au 1er démarrage

# ── LLM ──────────────────────────────────────────────────────────
OPENAI_API_KEY=sk-...
OPENAI_API_BASE_URL=https://api.openai.com/v1
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIM=1024
LLM_MODEL=gpt-4o

# ── Storage MinIO ─────────────────────────────────────────────────
MINIO_ENDPOINT=minio:9000
MINIO_ROOT_USER=arceag
MINIO_ROOT_PASSWORD=changeme-minio
MINIO_BUCKET=arceag-files
MINIO_SECURE=false               # true si HTTPS activé

# ── Notion ───────────────────────────────────────────────────────
NOTION_TOKEN=secret_...
NOTION_DATABASE_AFFAIRES=...
NOTION_DATABASE_ACTIONS=...

# ── API ──────────────────────────────────────────────────────────
API_PORT=8000
API_WORKERS=1                    # IMPORTANT: 1 seul worker (bus événements in-process)
DEBUG=true

# ── Rate limiting ────────────────────────────────────────────────
RATE_LIMIT_LLM=10/minute         # endpoints LLM (ingest, génération, analyse)
RATE_LIMIT_STANDARD=100/minute   # endpoints CRUD
RATE_LIMIT_READ=1000/minute      # GET endpoints
```

---

## 17. RÈGLES DE DEV (à respecter absolument)

### Architecture modulaire
1. **Un module = un dossier** `api/modules/{nom}/` avec ses 7 fichiers standard
2. **Pas d'import croisé entre modules** — utiliser le bus PostgreSQL LISTEN/NOTIFY (`core/events.py`)
3. **Import `core/services/`** autorisé depuis tout module (rag_service, storage_service, llm_service)
4. **Tout comportement configurable** dans `config.yaml` du module — jamais hardcodé dans le code
5. **`main.py` ne connaît aucun module** — tout passe par `registry.load_all()`
6. **`manifest.yaml` est la source de vérité** pour prefix, dépendances, tools, agent

### Auth
7. **Tout endpoint** (sauf `/auth/login`, `/health`) exige `get_current_user` en dépendance
8. **Tout endpoint avec `affaire_id`** exige `require_affaire_access(min_role=...)` en dépendance
9. **Seuls les admins** peuvent accéder à `/admin/*` et aux endpoints de configuration
10. **Les clés API externes** sont stockées chiffrées en DB (table `api_connections`), jamais en clair dans les logs

### Code
11. **Toute logique métier dans `engine.py`** du module — jamais dans le router
12. **`router.py` = validation Pydantic + auth + appel engine + retour HTTP** uniquement
13. **`def get_router(config: dict) → APIRouter`** : signature obligatoire du router
14. **SQLAlchemy async** partout (asyncpg driver)
15. **Pydantic v2** pour tous les schemas
16. **Rate limiting** : décorer avec `@limiter.limit("10/minute")` tous les endpoints qui appellent un LLM

### Données
17. **pgvector** pour tout ce qui est sémantique — pas d'index texte brut
18. **UUID** comme clé primaire partout
19. **JSONB** pour les données flexibles (metadata, config)
20. **`intervenant_id`** à la place de `entreprise VARCHAR` dans toutes les tables
21. **Tables jamais auto-droppées** si module désactivé — opérateur doit lancer down-migration manuellement
22. Migrations préfixées : `{module}_{NNN}_{description}.py`

### Storage
23. **Tout fichier binaire** (PDF, photo, document) passe par `storage_service.upload()` → MinIO
24. **Les tables DB ne stockent jamais de binaire** — seulement la clé MinIO (`storage_key VARCHAR`)
25. **Bucket unique** `arceag-files`, structure clé : `{affaire_id}/{module}/{filename}`

### Workers
26. **`API_WORKERS=1`** en v1 — le bus événements PostgreSQL est compatible multi-workers mais les handlers in-process ne le sont pas encore
27. Si besoin de scaling horizontal → migrer vers handlers enregistrés en DB

### OpenWebUI
28. **Les tools ne contiennent aucune logique** — ils appellent l'API REST avec le JWT de l'utilisateur
29. **Chaque tool** inclut `Authorization: Bearer {jwt}` dans ses headers

### Tests
30. Tests dans `api/modules/{nom}/tests/` pour les engines critiques
31. Test de chargement du registry dans `api/tests/test_registry.py`
32. Test d'auth : accès refusé (403) pour les mauvais rôles, token expiré (401)

---

## 18. DÉCISIONS ARCHITECTURALES — TOUTES CLOSES

| # | Question | ✅ Décision finale |
|---|----------|--------------------|
| 1 | Modèle embedding | OpenAI `text-embedding-3-large` — configurable dans `rag/config.yaml` |
| 2 | Auth API | **JWT HS256** — 4 rôles (admin/moe/collaborateur/lecteur) — per-affaire via `affaire_permissions` |
| 3 | Sync Notion | Polling 5min en v1 (configurable via `/admin/syncs`), webhook en v2 |
| 4 | Jours ouvrés | Configurable par affaire dans `planning/config.yaml` — calendrier FR par défaut |
| 5 | Multi-tenant | Non en v1 (une agence = une instance Docker) |
| 6 | Export Gantt | CSV + JSON v1, export XLSX en v2 |
| 7 | Hot-reload modules prod | Non — uniquement en dev (`watchfiles`) |
| 8 | Background tasks | APScheduler en v1 (dans chaque module via manifest) |
| 9 | Bus d'événements | **PostgreSQL LISTEN/NOTIFY** — compatible multi-workers, pas de Redis en v1 |
| 10 | Templates documents | Jinja2 → Markdown v1, export PDF via `pandoc` en v2 |
| 11 | Storage fichiers | **MinIO** (S3-compatible self-hosted Docker) — bucket `arceag-files` |
| 12 | RAG | **Service core partagé** (`core/services/rag_service.py`) + module `rag/` pour le router utilisateur |
| 13 | planning_tasks | **Supprimé** — remplacé par `planning_lots` (granularité MOE) |
| 14 | Intervenants | **Table dédiée** `intervenants` — remplace `entreprise VARCHAR` éparpillé |
| 15 | Rate limiting | **slowapi** — 10/min LLM, 100/min standard, 1000/min lecture |
| 16 | Interface admin | **Module `admin/`** avec router + UI HTMX — modules, users, connexions API, syncs, storage, logs |
| 17 | API_WORKERS | **1 en v1** — documenter dans .env |

---

---

## 19. MEMORY ENGINE — Mémoire Projet Intelligente

### 19.1 Architecture à 3 niveaux

```
┌─────────────────────────────────────────────────────────────┐
│  Niveau 1 — MÉMOIRE BRUTE (non persistée)                   │
│  Discussion chat, analyses en cours, hypothèses temporaires  │
│  → Vie = durée de la session OpenWebUI                      │
└─────────────────────────┬───────────────────────────────────┘
                          │ détection automatique
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Niveau 2 — MÉMOIRE CANDIDATE (memory_candidates)           │
│  Information détectée comme potentiellement importante       │
│  → Dédup vérifié, classification faite, attente validation  │
└─────────────────────────┬───────────────────────────────────┘
                          │ validation utilisateur (ou auto)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Niveau 3 — MÉMOIRE VALIDÉE (project_memory)                │
│  Décisions, risques, insights, coordination                  │
│  → Persistée, indexée pgvector, exploitable par tous agents │
└─────────────────────────────────────────────────────────────┘
```

### 19.2 Pipeline de création d'une mémoire candidate

```
Information produite (chat / CR / analyse / simulation)
    │
    ▼
1. CLASSIFICATION LLM
   → type_memory  : decision | risk | insight | coordination
   → importance   : info | warning | critical
   → lot concerné (si applicable)
    │
    ▼
2. GÉNÉRATION EMBEDDING (text-embedding-3-large)
    │
    ▼
3. DÉDUPLICATION (pgvector cosine similarity)
   ┌─────────────────────────────────────────────────────┐
   │ Rechercher dans project_memory WHERE affaire_id = X  │
   │ ORDER BY embedding <=> query_embedding LIMIT 5       │
   │                                                      │
   │  similarity >= 0.92  →  DOUBLON — ne pas créer      │
   │  0.75 <= sim < 0.92  →  PROCHE — signaler + proposer│
   │  similarity < 0.75   →  NOUVEAU — créer candidate   │
   └─────────────────────────────────────────────────────┘
    │
    ▼
4. VÉRIFICATION CROSS-TABLES
   → chantier_events (descriptions similaires ?)
   → decisions (déjà arbitré ?)
   → alerts (déjà alerté ?)
    │
    ▼
5. CRÉATION memory_candidates
   → statut = 'pending'
   → similarity_score + duplicate_of si proche
    │
    ▼
6. DÉCISION SELON user_preferences
   (voir section 15.4)
```

### 19.3 Classification automatique

**Prompt système classifieur :**
```
Tu es un assistant MOE expert en pilotage de chantier.
Analyse cette information extraite d'un échange chantier.

Classifie selon :
TYPE (un seul) :
- decision    : une décision a été prise ou doit être prise
- risk        : un risque, problème ou danger identifié
- insight     : observation utile, retour d'expérience, constat important
- coordination: information de coordination entre acteurs / lots

IMPORTANCE (un seul) :
- critical : impact direct sur délai, coût, sécurité ou réception
- warning  : impact possible, à surveiller
- info     : utile à conserver, pas d'urgence

Réponds UNIQUEMENT avec ce JSON :
{
  "type_memory": "...",
  "importance": "...",
  "lot": "...",          // lot BTP concerné, null si transversal
  "resume": "...",       // résumé en 1 phrase claire et actionnable (max 120 chars)
  "raison": "..."        // justification courte de la classification
}
```

**Exemples de classification :**

| Information brute | type | importance |
|---|---|---|
| "réservation PAC mal positionnée de 30cm" | risk | warning |
| "décision : changer entreprise lot plomberie" | decision | critical |
| "prévoir 2 semaines de délai livraison charpente métal" | insight | warning |
| "BET structure attend validation plans avant semaine 3" | coordination | warning |
| "prise de conscience : éviter joints en fond de tableau" | insight | info |
| "retard coulage dalle dû aux gelées, impact -7j planning" | risk | critical |

### 19.4 Comportement selon user_preferences

```python
def should_auto_save(candidate: MemoryCandidate, prefs: UserPreferences) -> str:
    """
    Retourne : 'auto_save' | 'ask_user' | 'skip'
    """
    # Mode auto total
    if prefs.auto_save and not prefs.ask_validation:
        return 'auto_save'

    # Seuil importance non atteint → ignorer
    importance_rank = {'info': 0, 'warning': 1, 'critical': 2}
    if importance_rank[candidate.importance] < importance_rank[prefs.min_importance_to_save]:
        return 'skip'

    # Mode intelligent (défaut)
    if not prefs.auto_save and prefs.ask_validation:
        match prefs.sensitivity:
            case 'low':
                # Auto-save sauf critical → demander
                return 'ask_user' if candidate.importance == 'critical' else 'auto_save'
            case 'medium':
                # Demander pour warning + critical
                return 'ask_user' if candidate.importance in ('warning', 'critical') else 'auto_save'
            case 'high':
                # Toujours demander
                return 'ask_user'

    return 'ask_user'
```

### 19.5 Format de la proposition à l'utilisateur (OpenWebUI)

L'agent doit présenter la candidature de façon structurée et concise.

**Template réponse agent :**
```
---
📋 **Nouvelle information détectée**

**Type :** `{type_memory}` | **Importance :** `{importance}`
**Lot :** {lot}

> {resume}

{si_proche}
⚠️ Information proche déjà enregistrée :
> "{contenu_existant}" (similarité: {similarity_score:.0%})

---
Souhaitez-vous l'enregistrer ?
**[Oui]** · **[Non]** · **[Modifier]**
---
```

**Comportement des actions :**

| Action | Effet |
|--------|-------|
| `[Oui]` | Appelle `/memory/save` → statut `validated` → insert `project_memory` |
| `[Non]` | Appelle `DELETE /memory/candidate/{id}` → statut `rejected` |
| `[Modifier]` | Affiche l'information éditable → `PATCH /memory/candidate/{id}` → repropose |

### 19.6 Recherche et utilisation en contexte

**Avant chaque analyse (meeting, planning, simulation) le système doit :**

```python
async def build_project_context(affaire_id: UUID, question: str) -> ProjectContext:
    """
    Construit le contexte enrichi pour l'IA avant toute analyse.
    Fusionne mémoire, events et décisions sans doublon.
    """
    embedding = await embed(question)

    # 1. Mémoire projet (top 8 par similarité)
    memories = await db.execute("""
        SELECT * FROM project_memory
        WHERE affaire_id = :aid
        ORDER BY embedding <=> :emb
        LIMIT 8
    """, {"aid": affaire_id, "emb": embedding})

    # 2. Events récents / ouverts critiques
    events = await db.execute("""
        SELECT * FROM chantier_events
        WHERE affaire_id = :aid
          AND statut != 'clos'
          AND priorite IN ('high', 'critical')
        ORDER BY date_evenement DESC
        LIMIT 10
    """, {"aid": affaire_id})

    # 3. Décisions récentes
    decisions = await db.execute("""
        SELECT * FROM decisions
        WHERE affaire_id = :aid
          AND statut = 'active'
        ORDER BY date_decision DESC
        LIMIT 5
    """, {"aid": affaire_id})

    # 4. Alertes actives
    alerts = await db.execute("""
        SELECT * FROM alerts
        WHERE affaire_id = :aid AND acquittee = FALSE
        ORDER BY created_at DESC LIMIT 5
    """, {"aid": affaire_id})

    return ProjectContext(
        memories=memories,
        events=events,
        decisions=decisions,
        alerts=alerts
    )
```

**Endpoint dédié :**
`GET /memory/{affaire_id}/context?question={question}`

Retourne le contexte fusionné, injecté dans le prompt système des agents.

### 19.7 Tools OpenWebUI — memory_tools.py

```python
"""
Tools mémoire pour les agents OpenWebUI.
Ces fonctions sont appelées par l'agent quand il détecte une information importante.
"""

async def detect_and_candidate_memory(
    affaire_id: str,
    raw_content: str,
    source: str = "chat"
) -> dict:
    """
    Soumettre une information pour évaluation mémoire.
    L'API classe, déduplique et crée la candidate.
    Retourne la candidate avec recommandation (auto_save | ask_user | skip).
    """
    response = await api_post("/memory/candidate", {
        "affaire_id": affaire_id,
        "content": raw_content,
        "source": source
    })
    return response


async def validate_memory(candidate_id: str, user_id: str) -> dict:
    """Valider et persister une candidate."""
    return await api_post("/memory/save", {
        "candidate_id": candidate_id,
        "validated_by": user_id
    })


async def reject_memory(candidate_id: str) -> dict:
    """Rejeter une candidate."""
    return await api_delete(f"/memory/candidate/{candidate_id}")


async def query_project_memory(
    affaire_id: str,
    question: str,
    type_filter: str = None,
    importance_filter: str = None
) -> dict:
    """Recherche sémantique dans la mémoire validée."""
    return await api_post("/memory/query", {
        "affaire_id": affaire_id,
        "question": question,
        "type_filter": type_filter,
        "importance_filter": importance_filter
    })


async def get_project_context(affaire_id: str, question: str) -> dict:
    """Contexte enrichi : mémoire + events + décisions + alertes."""
    return await api_get(f"/memory/{affaire_id}/context", {"question": question})
```

### 19.8 Intégration dans les autres engines

**Meeting engine** — après extraction des actions :
```python
# Pour chaque décision et blocage extrait du CR
for item in extracted_items:
    if item.type in ('decision', 'blocage'):
        candidate = await memory_engine.create_candidate(
            affaire_id=affaire_id,
            content=item.description,
            source="cr",
            source_ref=meeting_id
        )
        # Le router retourne les candidats avec la réponse meeting
        # L'agent OpenWebUI les présente à l'utilisateur
```

**Planning engine** — après simulation scénario :
```python
# Si impact critique détecté
if scenario_result.duree_supplementaire_jours > 7:
    await memory_engine.create_candidate(
        affaire_id=affaire_id,
        content=f"Risque planning : {scenario.type} sur {scenario.lot} → +{delta}j sur réception",
        source="simulation",
        importance_hint="critical"  # suggestion, la classification LLM peut overrider
    )
```

**Event engine** — sur nouvelle alerte critique :
```python
if alert.severite == 'critical':
    await memory_engine.create_candidate(
        affaire_id=affaire_id,
        content=alert.message,
        source="chantier",
        source_ref=alert.entite_ref,
        importance_hint="critical"
    )
```

### 19.9 Règles de qualité mémoire (invariants)

1. **Jamais de doublon** — seuil cosine `>= 0.92` = rejet automatique sans proposition
2. **Mémoire actionnable** — le `content` doit toujours être une phrase complète et autonome (comprise hors contexte)
3. **Traçabilité obligatoire** — tout enregistrement doit avoir `source` + `source_ref` si possible
4. **Pas d'embedding null** — toute entrée `project_memory` doit avoir son embedding (contrôle DB)
5. **Nettoyage périodique** — les `memory_candidates` rejetées ou `pending` depuis > 7 jours sont archivées
6. **Importance non dégradable** — une `critical` ne peut pas être reclassifiée `info` sans justification explicite
7. **Cohérence cross-affaire** — `insights` génériques (pas liés à un lot spécifique) peuvent être tagués `global` pour réutilisation

### 19.10 Seuils de similarité cosine — calibration

| Seuil | Interprétation | Action |
|-------|---------------|--------|
| >= 0.92 | Quasi-identique | Rejet silencieux (doublon certain) |
| 0.80 – 0.91 | Très similaire | Proposer fusion ou mise à jour |
| 0.65 – 0.79 | Thème proche | Signaler l'existant, laisser choisir |
| < 0.65 | Nouveau | Créer candidate directement |

---

*Dernière mise à jour : 2026-03-21*
*Auteur : Claude (session OS Chantier)*
