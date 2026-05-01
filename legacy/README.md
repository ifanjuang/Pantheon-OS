# Legacy

Code et documents issus d'anciens développements, conservés pour référence
historique mais **non maintenus** et **non chargés par le runtime**.

## Convention

- Rien dans `legacy/` n'est importé par le code vivant.
- Pas de tests, pas de migrations, pas d'entrée dans `modules.yaml`.
- Si une fonctionnalité doit être réactivée, elle doit être déplacée hors de
  `legacy/`, alignée sur les patterns courants (manifest, tests, migration),
  et déclarée explicitement dans la config.

## Contenu

| Chemin | Origine | Raison de l'archivage |
|---|---|---|
| `apps/control/` | `platform/api/apps/control/` | Stub sans tests, sans migration, sans modèle ; workflows orphelins. |
| `apps/monitoring/` | `platform/api/apps/monitoring/` | Sans tests, sans migration, sans modèle ; rôle observability flou. |
| `benchmarks/` | `benchmarks/` | Outil interne ClawMark, exclu du linting, plus appelé par la CI. |
| `INSTALL.md` | racine | Procédure d'installation décalée par rapport à `scripts/install/ui/`. |
