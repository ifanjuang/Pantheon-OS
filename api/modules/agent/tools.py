"""
Outils disponibles pour l'agent copilote MOE.

Chaque outil expose :
  - DEFINITION : dict OpenAI function-calling (schema JSON)
  - execute()   : coroutine async qui reçoit les args et retourne (str, list[SourceCitation])

L'agent peut combiner ces outils librement pour répondre à une instruction.

SourceCitation = {chunk_id, document_name, score, excerpt}
Les sources collectées sont agrégées dans agent_runs.sources pour traçabilité.

Outils disponibles :
  rag_search          → recherche sémantique dans les documents uploadés
  list_documents      → liste les fichiers du projet
  get_affaire_info    → infos générales du projet
  web_search          → recherche web (DuckDuckGo, optionnel : sites de confiance)
  fetch_url           → extrait le texte d'une URL ou d'un PDF en ligne
"""
import json
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.rag_service import RagService

log = get_logger("agent.tools")

# Sites de confiance MOE — utilisés par web_search(restrict_to_trusted=True)
TRUSTED_SITES = [
    "legifrance.gouv.fr",
    "boamp.fr",
    "rt-batiment.fr",
    "cstb.fr",
    "afnor.org",
    "oppbtp.fr",
    "qualibat.fr",
    "cohesion-territoires.gouv.fr",
    "construction.gouv.fr",
    "service-public.fr",
]

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
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Recherche sur le web. Utilise pour trouver des normes, DTU, réglementations "
                "(RE2020, loi MOP, CCAG...), jurisprudence, ou toute information externe au projet. "
                "Préfère restrict_to_trusted=true pour les sources officielles MOE/BTP."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Requête de recherche précise",
                    },
                    "num_results": {
                        "type": "integer",
                        "default": 5,
                        "description": "Nombre de résultats (max 10)",
                    },
                    "restrict_to_trusted": {
                        "type": "boolean",
                        "default": True,
                        "description": "Restreindre aux sites de confiance MOE (legifrance, cstb, afnor...)",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_url",
            "description": (
                "Récupère et extrait le contenu textuel complet d'une URL (page web ou PDF en ligne). "
                "Utilise après web_search pour lire le contenu d'une source prometteuse. "
                "Ne cite jamais un snippet de recherche sans avoir lu la source."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL à récupérer",
                    },
                    "max_chars": {
                        "type": "integer",
                        "default": 4000,
                        "description": "Nombre maximum de caractères à retourner",
                    },
                },
                "required": ["url"],
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
) -> tuple[str, list[dict]]:  # (output_text, web_sources)
    """
    Dispatche l'appel d'outil.
    Retourne (output_text, sources) où sources est la liste des citations RAG.
    Pour les outils non-RAG, sources est toujours [].
    """
    if name == "rag_search":
        return await _rag_search(db, affaire_id, args)
    if name == "list_documents":
        return await _list_documents(db, affaire_id), []
    if name == "get_affaire_info":
        return await _get_affaire_info(db, affaire_id), []
    if name == "web_search":
        return await _web_search(args)
    if name == "fetch_url":
        return await _fetch_url(args)
    return f"[outil inconnu : {name}]", []


async def _rag_search(db: AsyncSession, affaire_id: UUID, args: dict) -> tuple[str, list[dict]]:
    results = await RagService.search(
        db=db,
        query=args["query"],
        affaire_id=affaire_id,
        top_k=args.get("top_k", 4),
        source_type=args.get("source_type"),
    )
    if not results:
        return "Aucun résultat trouvé dans les documents du projet.", []

    lines = []
    sources = []

    for i, r in enumerate(results, 1):
        score_pct = int(r["score"] * 100)
        meta = r.get("meta") or {}
        doc_name = meta.get("filename") or f"document_{r['document_id'][:8]}"
        excerpt = r["contenu"][:300]

        # Format lisible pour le LLM — facilite les citations dans la réponse finale
        lines.append(
            f"[SOURCE {i}] 📄 {doc_name} (score {score_pct}%)\n"
            f"{excerpt}"
        )

        sources.append({
            "chunk_id": r["chunk_id"],
            "document_id": r["document_id"],
            "document_name": doc_name,
            "score": r["score"],
            "excerpt": excerpt[:150],
        })

    output = (
        f"Résultats pour : « {args['query']} »\n\n"
        + "\n\n".join(lines)
        + "\n\n— Pour citer une source dans ta réponse, utilise [SOURCE N]."
    )
    return output, sources


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


async def _web_search(args: dict) -> tuple[str, list[dict]]:
    """
    Recherche web via DuckDuckGo.
    Si restrict_to_trusted=True, limite aux sites de confiance MOE.
    """
    query = args["query"]
    num_results = min(args.get("num_results", 5), 10)
    restrict = args.get("restrict_to_trusted", True)

    # Construire la requête avec filtres sites si demandé
    search_query = query
    if restrict and TRUSTED_SITES:
        site_filter = " OR ".join(f"site:{s}" for s in TRUSTED_SITES)
        search_query = f"({query}) ({site_filter})"

    try:
        from duckduckgo_search import DDGS
        import asyncio

        def _search():
            with DDGS() as ddgs:
                return list(ddgs.text(search_query, max_results=num_results))

        results = await asyncio.get_event_loop().run_in_executor(None, _search)
    except ImportError:
        return "[web_search indisponible — installer duckduckgo-search]", []
    except Exception as exc:
        log.warning("tool.web_search_failed", error=str(exc))
        return f"Recherche web échouée : {exc}", []

    if not results:
        if restrict:
            return (
                f"Aucun résultat sur les sites de confiance pour : « {query} »\n"
                "Relance avec restrict_to_trusted=false pour élargir la recherche.",
                [],
            )
        return f"Aucun résultat trouvé pour : « {query} »", []

    sources = []
    lines = [f"Résultats web pour : « {query} »" + (" (sites de confiance)" if restrict else "") + "\n"]

    for i, r in enumerate(results, 1):
        title = r.get("title", "Sans titre")
        url = r.get("href", "")
        snippet = r.get("body", "")[:300]

        # Badge confiance
        is_trusted = any(site in url for site in TRUSTED_SITES)
        badge = "✅" if is_trusted else "🌐"

        lines.append(f"[RÉSULTAT {i}] {badge} {title}\n🔗 {url}\n{snippet}\n")
        sources.append({
            "chunk_id": f"web_{i}",
            "document_name": title,
            "document_id": url,
            "score": 1.0 if is_trusted else 0.7,
            "excerpt": snippet[:150],
            "url": url,
            "trusted": is_trusted,
        })

    lines.append("— Utilise fetch_url(url) pour lire le contenu complet d'une source.")
    return "\n".join(lines), sources


async def _fetch_url(args: dict) -> tuple[str, list[dict]]:
    """
    Récupère et extrait le texte propre d'une URL.
    Supporte HTML (via trafilatura) et PDF (via pypdf).
    """
    url = args["url"]
    max_chars = min(args.get("max_chars", 4000), 8000)

    try:
        import httpx
        async with httpx.AsyncClient(
            timeout=15,
            follow_redirects=True,
            headers={"User-Agent": "ARCEUS-Apollon/1.0 (MOE research bot)"},
        ) as client:
            response = await client.get(url)
            response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        raw = response.content

        # PDF
        if "pdf" in content_type or url.lower().endswith(".pdf"):
            try:
                import io
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(raw))
                text = "\n".join(p.extract_text() or "" for p in reader.pages)
                source_type = "PDF"
            except Exception:
                text = raw.decode("utf-8", errors="replace")
                source_type = "PDF (extraction basique)"

        # HTML → trafilatura pour extraction propre
        else:
            try:
                import trafilatura
                text = trafilatura.extract(
                    raw,
                    include_tables=True,
                    include_links=False,
                    no_fallback=False,
                ) or ""
                source_type = "HTML"
            except ImportError:
                # Fallback : supprimer les balises basiquement
                import re
                text = re.sub(r"<[^>]+>", " ", raw.decode("utf-8", errors="replace"))
                source_type = "HTML (extraction basique)"

        text = text.strip()
        if not text:
            return f"[fetch_url] Aucun contenu extractible depuis {url}", []

        truncated = len(text) > max_chars
        excerpt = text[:max_chars]
        suffix = f"\n\n[... contenu tronqué à {max_chars} caractères sur {len(text)}]" if truncated else ""

        output = (
            f"[CONTENU] {source_type} — {url}\n"
            f"{'─' * 60}\n"
            f"{excerpt}{suffix}"
        )

        is_trusted = any(site in url for site in TRUSTED_SITES)
        source = {
            "chunk_id": f"fetch_{hash(url) % 100000}",
            "document_name": url.split("/")[-1] or url,
            "document_id": url,
            "score": 1.0 if is_trusted else 0.8,
            "excerpt": excerpt[:200],
            "url": url,
            "trusted": is_trusted,
        }
        log.info("tool.fetch_url", url=url, chars=len(text), trusted=is_trusted)
        return output, [source]

    except httpx.HTTPStatusError as exc:
        return f"[fetch_url] Erreur HTTP {exc.response.status_code} : {url}", []
    except Exception as exc:
        log.warning("tool.fetch_url_failed", url=url, error=str(exc))
        return f"[fetch_url] Impossible de récupérer {url} : {exc}", []
