---
name: agent-soul
description: Consulter ou modifier le SOUL.md d'un agent du panthéon Pantheon OS
allowed-tools: Read, Write
argument-hint: "[nom-agent] [edit|show]"
---

Agent demandé : $ARGUMENTS

## Agents disponibles (22)
**Meta** : zeus · athena · themis · hera · apollo
**Analysis** : hermes · argos · prometheus · hecate · demeter · artemis · metis
**Memory** : hestia · hades · mnemosyne
**Output** : kairos · daedalus · iris · aphrodite · hephaestus
**System** : ares · poseidon

## Comportement

Si l'argument contient "show" ou "read" → lire et afficher le SOUL.md de l'agent.

Si l'argument contient "edit" ou "update" → lire d'abord le SOUL.md existant, proposer les modifications,
attendre validation avant d'écrire. Ne jamais écraser un SOUL.md sans confirmation explicite.

## Règles pour modifier un SOUL.md
- Garder sous 60 lignes
- Conserver la structure : Rôle / Règles / Format de sortie
- Ne jamais enlever les règles existantes sans raison explicite
- Écrire en français

## Chemin des fichiers
`modules/agents/{layer}/{myth}_{role}/SOUL.md`

Exemple : zeus → `modules/agents/meta/zeus_orchestrator/SOUL.md`
