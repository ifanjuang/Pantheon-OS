# OS Projet — Installation, Configuration & Maintenance

---

## Prérequis

| Outil | Version minimale | Vérifier |
|-------|-----------------|---------|
| Docker | 24+ | `docker --version` |
| Docker Compose | v2+ | `docker compose version` |
| Git | 2.40+ | `git --version` |
| RAM disponible | 8 Go (16 Go recommandé avec Ollama) | `free -h` |
| Espace disque | 20 Go minimum | `df -h` |

> **Mode cloud uniquement (sans Ollama) :** 4 Go RAM suffisent.

---

## Installation initiale

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-org/os-projet.git
cd os-projet
```

### 2. Créer le fichier `.env`

```bash
cp .env.example .env
```

Ouvrir `.env` et remplir les valeurs obligatoires (voir section [Configuration](#configuration) ci-dessous).

### 3. Choisir le mode IA

**Mode local (recommandé — données 100% sur site) :**
```bash
# Dans .env :
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral:7b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

**Mode cloud (performance maximale) :**
```bash
# Dans .env :
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o
```

### 4. Lancer les services

```bash
# Démarrage complet
docker compose up -d

# Avec le bot Telegram (optionnel)
docker compose --profile telegram up -d

# Vérifier que tout est en vie
docker compose ps
```

### 5. Initialiser la base de données

```bash
# Créer les tables (migrations Alembic)
docker compose exec api alembic upgrade head

# Créer le premier compte admin
docker compose exec api python -m scripts.create_admin \
  --email admin@agence.fr \
  --nom "Admin" \
  --password "MotDePasseForte2025!"
```

### 6. Télécharger le modèle IA (mode Ollama uniquement)

```bash
# Télécharger le LLM
docker compose exec ollama ollama pull mistral:7b

# Télécharger le modèle d'embedding
docker compose exec ollama ollama pull nomic-embed-text

# Vérifier les modèles disponibles
docker compose exec ollama ollama list
```

### 7. Vérifier l'installation

```bash
# Health check API
curl http://localhost:8000/health
# → {"status": "ok"}

# Ouvrir l'interface
open http://localhost:3000   # OpenWebUI
open http://localhost:8080   # MinIO console (fichiers)
```

---

## Configuration

### Variables d'environnement (`.env`)

```bash
# ── Base de données ────────────────────────────────────────────────────
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=os_projet
POSTGRES_USER=os_projet
POSTGRES_PASSWORD=changeme_motdepasse_fort

# ── Stockage fichiers (MinIO) ──────────────────────────────────────────
MINIO_HOST=minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=changeme_minio_secret
MINIO_BUCKET=arceag-files

# ── Auth JWT ───────────────────────────────────────────────────────────
JWT_SECRET=changeme_secret_tres_long_et_aleatoire_min_32_chars
JWT_EXPIRE_MINUTES=1440   # 24h

# ── Mode IA ───────────────────────────────────────────────────────────
LLM_PROVIDER=ollama           # ollama | openai | mistral | groq
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=mistral:7b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-...
# LLM_MODEL=gpt-4o
# EMBEDDING_MODEL=text-embedding-3-large

# ── Email (alertes SMTP) ───────────────────────────────────────────────
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=notifications@agence.fr
SMTP_PASSWORD=mot_de_passe_application
SMTP_FROM=OS Projet <notifications@agence.fr>

# ── Optionnel ─────────────────────────────────────────────────────────
TELEGRAM_TOKEN=             # Bot Telegram (laisser vide si non utilisé)
SLACK_WEBHOOK_URL=          # Notifications Slack
SENTRY_DSN=                 # Monitoring erreurs
```

> **Sécurité :** Ne jamais commiter `.env` dans Git. Le fichier est dans `.gitignore`.

---

### Activer / désactiver des modules (`modules.yaml`)

```yaml
# modules.yaml — à la racine
modules:
  - name: chantier
    enabled: true

  - name: budget
    enabled: true

  - name: planning
    enabled: true

  - name: finance
    enabled: true       # ← passer à false pour désactiver

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

Après modification : `docker compose restart api` (en développement, hot-reload via watchfiles).

---

### Modifier le comportement sans toucher au code

Chaque module expose un fichier `config.yaml` modifiable à chaud :

| Ce que je veux changer | Fichier | Clé |
|------------------------|---------|-----|
| Seuil alerte dépassement budget | `api/modules/finance/config.yaml` | `seuil_alerte_pct: 90` |
| Dépendances entre lots (planning) | `api/modules/planning/config.yaml` | `lot_dependencies` |
| Catégories d'emails à classifier | `api/modules/communications/config.yaml` | `categories` |
| Prompt de l'agent réunion | `api/modules/meeting/config.yaml` | `prompt_file` |
| Types de documents générables | `api/modules/documents/config.yaml` | `types` |
| Règles d'alertes automatiques | `api/modules/events_engine/config.yaml` | `rules` |
| Modèle LLM | `.env` | `LLM_MODEL` |
| Modèle Ollama | `.env` | `OLLAMA_MODEL` |

**Rechargement à chaud :** les `config.yaml` sont rechargés par watchfiles sans redémarrage en développement. En production, `docker compose restart api`.

---

### Importer la base normative (Couche 1)

Via l'interface admin ou directement via API :

```bash
# Importer un DTU
curl -X POST http://localhost:8000/rag/import \
  -H "Authorization: Bearer <token_admin>" \
  -F "file=@DTU_20.1.pdf" \
  -F "source_type=general" \
  -F "label=DTU 20.1 — Maçonnerie"

# Importer un Eurocode
curl -X POST http://localhost:8000/rag/import \
  -H "Authorization: Bearer <token_admin>" \
  -F "file=@EC2_NF_EN_1992.pdf" \
  -F "source_type=general" \
  -F "label=Eurocode 2 — Béton armé"
```

---

## Maintenance

### Mises à jour

```bash
# 1. Récupérer les nouvelles versions
git pull origin main

# 2. Reconstruire les images si nécessaire
docker compose build --no-cache api

# 3. Appliquer les migrations de BDD
docker compose exec api alembic upgrade head

# 4. Redémarrer
docker compose up -d

# 5. Vérifier les logs
docker compose logs -f api --tail=50
```

---

### Sauvegardes

#### Sauvegarde complète (BDD + fichiers)

```bash
#!/bin/bash
# scripts/backup.sh — à planifier via cron

DATE=$(date +%Y%m%d_%H%M)
BACKUP_DIR="./backups/$DATE"
mkdir -p "$BACKUP_DIR"

# 1. Dump PostgreSQL
docker compose exec -T postgres pg_dump \
  -U "$POSTGRES_USER" "$POSTGRES_DB" \
  | gzip > "$BACKUP_DIR/postgres.sql.gz"

# 2. Export MinIO (fichiers projets)
docker compose exec -T minio mc mirror \
  /data "$BACKUP_DIR/minio/"

echo "Sauvegarde complète : $BACKUP_DIR"
```

**Planifier via cron (tous les jours à 2h) :**
```bash
0 2 * * * /chemin/vers/os-projet/scripts/backup.sh >> /var/log/os-projet-backup.log 2>&1
```

#### Restauration

```bash
# Restaurer la BDD
gunzip -c backups/20250601_0200/postgres.sql.gz \
  | docker compose exec -T postgres psql -U "$POSTGRES_USER" "$POSTGRES_DB"

# Restaurer les fichiers MinIO
docker compose exec minio mc mirror \
  backups/20250601_0200/minio/ /data/
```

---

### Logs & monitoring

```bash
# Logs de l'API en temps réel
docker compose logs -f api

# Logs d'un module spécifique
docker compose logs -f api | grep "\[planning\]"

# Logs de tous les services
docker compose logs -f

# Espace disque utilisé par les volumes Docker
docker system df -v

# Santé de chaque service
docker compose ps
curl http://localhost:8000/health
```

---

### Gestion des migrations de base de données

```bash
# Voir l'état actuel des migrations
docker compose exec api alembic current

# Appliquer toutes les migrations en attente
docker compose exec api alembic upgrade head

# Revenir à la migration précédente (si problème)
docker compose exec api alembic downgrade -1

# Créer une nouvelle migration (développeurs)
docker compose exec api alembic revision --autogenerate -m "description_courte"
```

---

### Gestion des modèles Ollama

```bash
# Lister les modèles installés
docker compose exec ollama ollama list

# Télécharger un nouveau modèle
docker compose exec ollama ollama pull llama3.2:3b

# Changer de modèle sans redémarrer
# → modifier .env : OLLAMA_MODEL=llama3.2:3b
# → docker compose restart api

# Supprimer un modèle (libérer de l'espace)
docker compose exec ollama ollama rm mistral:7b

# Tester un modèle directement
docker compose exec ollama ollama run mistral:7b "Qu'est-ce qu'un DTU ?"
```

---

### Gestion des utilisateurs

```bash
# Créer un utilisateur
docker compose exec api python -m scripts.create_user \
  --email collaborateur@agence.fr \
  --nom "Marie Dupont" \
  --role collaborateur

# Lister les utilisateurs
docker compose exec api python -m scripts.list_users

# Réinitialiser un mot de passe
docker compose exec api python -m scripts.reset_password \
  --email collaborateur@agence.fr \
  --password "NouveauMotDePasse2025!"

# Désactiver un compte (départ d'un collaborateur)
docker compose exec api python -m scripts.deactivate_user \
  --email ancien@agence.fr
```

---

### Arrêt et redémarrage propre

```bash
# Redémarrer l'API uniquement (sans couper la BDD)
docker compose restart api

# Arrêt complet (données préservées dans les volumes)
docker compose down

# Arrêt + suppression des données (ATTENTION — irréversible)
docker compose down -v

# Démarrage en mode dev (logs en direct)
docker compose up
```

---

## Déploiement en production (serveur OVH / Hetzner)

### Configuration HTTPS avec Traefik

```yaml
# docker-compose.prod.yml — ajout à docker-compose.yml de base
services:
  traefik:
    image: traefik:v3
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik/acme.json:/acme.json      # certificats Let's Encrypt
    command:
      - --providers.docker=true
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
      - --certificatesresolvers.letsencrypt.acme.httpchallenge=true
      - --certificatesresolvers.letsencrypt.acme.email=admin@agence.fr

  api:
    labels:
      - traefik.http.routers.api.rule=Host(`api.os-projet.agence.fr`)
      - traefik.http.routers.api.tls.certresolver=letsencrypt

  openwebui:
    labels:
      - traefik.http.routers.ui.rule=Host(`os-projet.agence.fr`)
      - traefik.http.routers.ui.tls.certresolver=letsencrypt
```

```bash
# Créer le fichier acme.json avec les bonnes permissions
touch traefik/acme.json && chmod 600 traefik/acme.json

# Lancer en production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

### Variables de production à changer obligatoirement

```bash
# !! Toutes ces valeurs DOIVENT être changées en production !!
POSTGRES_PASSWORD=<générer avec : openssl rand -base64 32>
JWT_SECRET=<générer avec : openssl rand -base64 64>
MINIO_SECRET_KEY=<générer avec : openssl rand -base64 32>
```

---

## Résolution de problèmes courants

| Symptôme | Cause probable | Solution |
|----------|---------------|---------|
| `curl /health` → connexion refusée | API pas encore démarrée | `docker compose logs api` — attendre ou vérifier erreur |
| Migrations échouent | BDD pas prête | `docker compose restart api` (la BDD démarre plus lentement) |
| Ollama lent (>30s) | Pas assez de RAM | Réduire le modèle : `OLLAMA_MODEL=tinyllama:1b` |
| MinIO inaccessible | Port 9000 bloqué | Vérifier le firewall : `ufw allow 9000` |
| JWT expiré | Token trop court | Augmenter `JWT_EXPIRE_MINUTES=1440` dans `.env` |
| `alembic upgrade` échoue | Migration conflit | `docker compose exec api alembic stamp head` (forcer l'état) |
| Emails non envoyés | SMTP mal configuré | Vérifier `SMTP_*` dans `.env`, utiliser un mot de passe d'application Gmail |
| Embedding très lent | CPU overload | Passer à `EMBEDDING_PROVIDER=openai` temporairement |

---

## Checklist de mise en production

```
□ .env créé avec toutes les valeurs de production (pas les valeurs par défaut)
□ POSTGRES_PASSWORD, JWT_SECRET, MINIO_SECRET_KEY générés aléatoirement
□ Certificat HTTPS configuré (Traefik + Let's Encrypt)
□ Sauvegarde automatique planifiée (cron)
□ Premier compte admin créé
□ Modèles Ollama téléchargés (si mode local)
□ Base normative Couche 1 importée (DTU, Eurocodes, RE2020)
□ Test de l'interface OpenWebUI accessible depuis l'extérieur
□ Test d'une question RAG sur la base normative
□ Notification SMTP testée (envoi d'une alerte test)
```
