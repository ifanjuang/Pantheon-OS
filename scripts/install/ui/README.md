# Pantheon OS Installer UI

Installer local autonome pour déployer Pantheon OS sur un NAS avec Ollama lancé sur un PC du réseau local.

Cette UI est volontairement indépendante du runtime Pantheon principal. Elle doit fonctionner avant que Pantheon OS soit installé.

## Lancement

Depuis la racine du dépôt :

```bash
python scripts/install/ui/installer_api.py
```

Puis ouvrir :

```text
http://NAS_IP:8090
```

Exemple local :

```text
http://localhost:8090
```

## Configuration

Champs attendus :

- IP ou URL Ollama : `192.168.50.14` ou `http://192.168.50.14:11434`
- Modèle chat : `qwen2.5:7b`
- Modèle embeddings : `nomic-embed-text`
- URL API Pantheon : `http://localhost:8000` depuis le NAS

## Étapes exécutables

L’UI peut lancer :

- check Docker ;
- check Docker Compose ;
- check Ollama ;
- préparation `.env` ;
- `docker compose up -d --build` ;
- `alembic upgrade head` ;
- tests ciblés ;
- `/health` ;
- `/debug/runtime-registry`.

## Fichier de suivi

L’état est écrit dans :

```text
install_status.json
```

Statuts possibles :

- `pending`
- `running`
- `ok`
- `warning`
- `error`

Statut global :

- `pending`
- `running`
- `ready`
- `degraded`
- `blocked`

## Sécurité

Ne pas exposer cette UI sur Internet.

Elle exécute des commandes locales Docker et Alembic. Elle doit rester accessible uniquement depuis le réseau local administrateur.

## Commandes utiles

```bash
python scripts/install/ui/installer_api.py
```

```bash
cat install_status.json
```

```bash
docker compose logs -f api
```

## Garde-fou Alembic

Si la migration Approval Gate contient :

```python
down_revision = None
```

vérifier localement :

```bash
alembic heads
```

Puis corriger `down_revision` si une tête Alembic existe déjà.
