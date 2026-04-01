"""
Outils disponibles pour l'agent copilote MOE.

Chaque outil expose :
  - DEFINITION : dict OpenAI function-calling (schema JSON)
  - execute()   : coroutine async qui reçoit les args et retourne une str

L'agent peut combiner ces outils librement pour répondre à une instruction.
"""
import json
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.rag_service import RagService

log = get_logger("agent.tools")

# ── Définitions OpenAI function-calling ─────────────────────────────────────

DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "rag_search",
            "description": (
                "Recherche sémantique dans les documents du projet. "
                "Utilise pour répondre à des questions sur le contenu des fichiers."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Question ou sujet à rechercher"},
                    "top_k": {"type": "integer", "default": 4, "description": "Nombre de résultats"},
                    "source_type": {
                        "type": "string",
                        "description": "Filtrer par type : cctp, cr, note, email, dtu",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_documents",
            "description": "Liste les documents disponibles dans le projet.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_affaire_info",
            "description": "Retourne les informations générales du projet (nom, code, statut).",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


# ── Exécution des outils ─────────────────────────────────────────────────────

async def execute_tool(
    name: str,
    args: dict,
    affaire_id: UUID,
    db: AsyncSession,
) -> str:
    """Dispatche l'appel d'outil et retourne le résultat sous forme de str."""
    if name == "rag_search":
        return await _rag_search(db, affaire_id, args)
    if name == "list_documents":
        return await _list_documents(db, affaire_id)
    if name == "get_affaire_info":
        return await _get_affaire_info(db, affaire_id)
    return f"[outil inconnu : {name}]"


async def _rag_search(db: AsyncSession, affaire_id: UUID, args: dict) -> str:
    results = await RagService.search(
        db=db,
        query=args["query"],
        affaire_id=affaire_id,
        top_k=args.get("top_k", 4),
        source_type=args.get("source_type"),
    )
    if not results:
        return "Aucun résultat trouvé dans les documents du projet."

    lines = []
    for i, r in enumerate(results, 1):
        score_pct = int(r["score"] * 100)
        lines.append(f"[{i}] (score {score_pct}%) {r['contenu'][:400]}")
    return "\n\n".join(lines)


async def _list_documents(db: AsyncSession, affaire_id: UUID) -> str:
    from modules.documents.models import Document

    result = await db.execute(
        select(Document.id, Document.nom, Document.couche, Document.type_doc, Document.created_at)
        .where(Document.affaire_id == affaire_id)
        .order_by(Document.created_at.desc())
    )
    rows = result.all()
    if not rows:
        return "Aucun document dans ce projet."

    lines = [f"- {r.nom} [{r.couche}/{r.type_doc}] (id: {r.id})" for r in rows]
    return f"{len(rows)} document(s) :\n" + "\n".join(lines)


async def _get_affaire_info(db: AsyncSession, affaire_id: UUID) -> str:
    from modules.affaires.models import Affaire

    affaire = await db.get(Affaire, affaire_id)
    if not affaire:
        return "Projet introuvable."
    return (
        f"Projet : {affaire.nom}\n"
        f"Code   : {affaire.code}\n"
        f"Statut : {affaire.statut}\n"
        f"Description : {affaire.description or '—'}"
    )
