---
name: agent-soul
description: Consulter ou modifier le SOUL.md d'un agent du panthéon ARCEUS (themis, argus, hermes, mnemosyne, athena)
allowed-tools: Read, Write
argument-hint: "[nom-agent] [edit|show]"
---

Agent demandé : $ARGUMENTS

## Agents disponibles
⚖️ themis · 👁️ argus · ⚡ hermes · 🏛️ mnemosyne · 🦉 athena

## Comportement

Si l'argument contient "show" ou "read" → lire et afficher le SOUL.md + MEMORY.md de l'agent.

Si l'argument contient "edit" ou "update" → lire d'abord le SOUL.md existant, proposer les modifications,
attendre validation avant d'écrire. Ne jamais écraser un SOUL.md sans confirmation explicite.

Si l'argument contient "memory" → lire et afficher le MEMORY.md de l'agent. Proposer d'ajouter
une entrée si l'utilisateur fournit un retour à capitaliser.

## Règles pour modifier un SOUL.md
- Garder sous 60 lignes
- Conserver la structure : Identité / Rôle / Principes / Relations
- Ne jamais enlever les principes existants sans raison explicite
- Une leçon apprise va dans MEMORY.md, pas dans SOUL.md

## Chemin des fichiers
`agents/{nom}/SOUL.md` · `agents/{nom}/MEMORY.md` · `agents/{nom}/IDENTITY.md`
