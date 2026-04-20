-- Initialisation de la base de données OS Projet
-- Ce script est exécuté au premier démarrage du container PostgreSQL

-- Extension pgvector (embeddings sémantiques)
CREATE EXTENSION IF NOT EXISTS vector;

-- Extension uuid-ossp (génération UUID côté DB)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extension pg_trgm (recherche textuelle rapide, optionnel)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Vérification
SELECT extname, extversion FROM pg_extension WHERE extname IN ('vector', 'uuid-ossp', 'pg_trgm');
