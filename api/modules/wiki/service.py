"""
WikiService — synthesis cache pour ARCEUS.

Pattern inspiré de llm-wiki : chaque décision validée devient une page
markdown navigable, réutilisable comme précédent lors du scoring d'une
nouvelle décision (bonus +5 « déjà validé dans projets passés »).

Responsabilités :
  - slugify / normalize_sujet  : identifiants stables
  - create_page                : création manuelle + embed
  - promote_from_decision      : lit project_decisions, génère markdown
  - find_similar               : recherche hybride (cosine + LIKE sujet_norm)
  - check_precedents           : wrap find_similar + calcul bonus scoring
  - render_markdown            : export pour mode AUDIT
"""
import re
import unicodedata
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.rag_service import RagService
from modules.wiki.models import WikiPage

log = get_logger("wiki.service")

# Bonus scoring aligné sur l'archi scoring décisionnel
PRECEDENT_BONUS_POINTS = 5
PRECEDENT_MIN_SCORE = 0.55  # Similarité cosine minimale pour considérer un précédent


def _now() -> datetime:
    return datetime.now(timezone.utc)


class WikiService:
    # ── Identifiants ────────────────────────────────────────────────

    @staticmethod
    def normalize_sujet(sujet: str) -> str:
        """Lowercase + retrait accents + whitespace collapse pour lookup rapide."""
        nfkd = unicodedata.normalize("NFKD", sujet)
        ascii_str = "".join(c for c in nfkd if not unicodedata.combining(c))
        return re.sub(r"\s+", " ", ascii_str.lower()).strip()

    @staticmethod
    def slugify(titre: str, max_length: int = 80) -> str:
        """Kebab-case URL-safe depuis un titre."""
        norm = WikiService.normalize_sujet(titre)
        slug = re.sub(r"[^a-z0-9]+", "-", norm).strip("-")
        return slug[:max_length] or "page"

    @classmethod
    async def _unique_slug(
        cls, db: AsyncSession, scope: str, base_slug: str
    ) -> str:
        """Ajoute un suffixe -2, -3, ... si (scope, slug) existe déjà."""
        candidate = base_slug
        suffix = 2
        while True:
            result = await db.execute(
                select(WikiPage.id).where(
                    WikiPage.scope == scope, WikiPage.slug == candidate
                )
            )
            if result.scalar_one_or_none() is None:
                return candidate
            candidate = f"{base_slug}-{suffix}"
            suffix += 1

    # ── Création ────────────────────────────────────────────────────

    @classmethod
    async def create_page(
        cls,
        db: AsyncSession,
        *,
        titre: str,
        contenu_md: str,
        scope: str = "projet",
        affaire_id: Optional[UUID] = None,
        tags: Optional[list[str]] = None,
        criticite: Optional[str] = None,
        score: Optional[int] = None,
        decision_id: Optional[UUID] = None,
        source_run_id: Optional[UUID] = None,
        citations: Optional[list[dict]] = None,
        validated_by: Optional[UUID] = None,
        auto_validate: bool = False,
    ) -> WikiPage:
        """
        Crée une page wiki, calcule l'embedding et persiste.
        scope='projet' exige un affaire_id.
        """
        if scope == "projet" and affaire_id is None:
            raise ValueError("scope='projet' requires affaire_id")

        base_slug = cls.slugify(titre)
        slug = await cls._unique_slug(db, scope, base_slug)

        embedding: Optional[list[float]] = None
        try:
            # Embed sur titre + début du contenu (context pertinent)
            embed_input = f"{titre}\n\n{contenu_md[:1500]}"
            embedding = await RagService.embed(embed_input)
        except Exception as exc:
            log.warning("wiki.embed_failed", slug=slug, error=str(exc))

        page = WikiPage(
            affaire_id=affaire_id,
            scope=scope,
            slug=slug,
            titre=titre[:512],
            sujet_norm=cls.normalize_sujet(titre)[:512],
            contenu_md=contenu_md,
            tags=tags or [],
            criticite=criticite,
            score=score,
            decision_id=decision_id,
            source_run_id=source_run_id,
            citations=citations or [],
            validated_by=validated_by if auto_validate else None,
            validated_at=_now() if auto_validate else None,
        )
        # embedding assigné séparément pour éviter l'erreur en dev sans pgvector
        if embedding is not None and hasattr(page, "embedding"):
            page.embedding = embedding

        db.add(page)
        await db.commit()
        await db.refresh(page)
        log.info(
            "wiki.page_created",
            page_id=str(page.id),
            scope=scope,
            slug=slug,
            validated=auto_validate,
        )
        return page

    # ── Promotion depuis une décision ──────────────────────────────

    @classmethod
    async def promote_from_decision(
        cls,
        db: AsyncSession,
        *,
        decision_id: UUID,
        scope: str = "projet",
        tags: Optional[list[str]] = None,
        contenu_md_override: Optional[str] = None,
        validated_by: Optional[UUID] = None,
    ) -> WikiPage:
        """
        Lit une project_decision validée (raw SQL — pas d'ORM model dédié)
        et crée une page wiki correspondante.
        """
        row = (
            await db.execute(
                text(
                    """
                    SELECT id, affaire_id, run_id, objet, contexte, constat,
                           analyse, impacts, options, criticite, dette, statut,
                           agent_source
                    FROM project_decisions
                    WHERE id = :id
                    """
                ),
                {"id": str(decision_id)},
            )
        ).mappings().first()

        if row is None:
            raise ValueError(f"project_decision {decision_id} introuvable")

        if row["statut"] != "validé":
            log.warning(
                "wiki.promote_non_validated",
                decision_id=str(decision_id),
                statut=row["statut"],
            )

        titre = (row["objet"] or "Décision sans objet")[:512]
        contenu = contenu_md_override or cls._render_decision_markdown(dict(row))

        return await cls.create_page(
            db,
            titre=titre,
            contenu_md=contenu,
            scope=scope,
            affaire_id=row["affaire_id"] if scope == "projet" else None,
            tags=tags or [],
            criticite=row["criticite"],
            score=None,  # Le score sera renseigné quand le module scoring sera branché
            decision_id=decision_id,
            source_run_id=row["run_id"],
            citations=[{"agent": row["agent_source"]}] if row["agent_source"] else [],
            validated_by=validated_by,
            auto_validate=row["statut"] == "validé",
        )

    @staticmethod
    def _render_decision_markdown(decision: dict[str, Any]) -> str:
        """
        Génère le markdown d'une page à partir d'une ligne project_decisions.
        Sections alignées sur la sortie structurée de l'interface unique
        (Objet / Contexte / Constat / Analyse / Impacts / Options / Décision).
        """
        lines: list[str] = [
            f"# {decision.get('objet') or 'Décision'}",
            "",
            f"- **Criticité** : {decision.get('criticite') or '—'}",
            f"- **Dette** : {decision.get('dette') or 'D0'}",
            f"- **Statut** : {decision.get('statut') or '—'}",
        ]
        if decision.get("agent_source"):
            lines.append(f"- **Agent source** : {decision['agent_source']}")
        lines.append("")

        def _section(title: str, body: Any) -> None:
            if not body:
                return
            lines.append(f"## {title}")
            lines.append("")
            if isinstance(body, (list, dict)):
                import json as _json
                lines.append("```json")
                lines.append(_json.dumps(body, ensure_ascii=False, indent=2))
                lines.append("```")
            else:
                lines.append(str(body))
            lines.append("")

        _section("Contexte", decision.get("contexte"))
        _section("Constat", decision.get("constat"))
        _section("Analyse", decision.get("analyse"))
        _section("Impacts", decision.get("impacts"))
        _section("Options", decision.get("options"))
        return "\n".join(lines).rstrip() + "\n"

    # ── Recherche ───────────────────────────────────────────────────

    @classmethod
    async def find_similar(
        cls,
        db: AsyncSession,
        *,
        query: str,
        affaire_id: Optional[UUID] = None,
        scope: Optional[str] = None,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Recherche hybride sur wiki_pages :
          1. Cosine similarity sur embedding (si dispo)
          2. Fallback / complément : LIKE sur sujet_norm

        Retourne [{page_id, slug, titre, score, extrait, scope, ...}, ...].
        """
        try:
            query_emb = await RagService.embed(query)
        except Exception as exc:
            log.warning("wiki.search_embed_failed", error=str(exc))
            query_emb = None

        # Filtres optionnels
        where_clauses = ["1 = 1"]
        params: dict[str, Any] = {"top_k": top_k}

        if scope:
            where_clauses.append("scope = :scope")
            params["scope"] = scope
        if affaire_id:
            where_clauses.append("(affaire_id = :affaire_id OR scope = 'agence')")
            params["affaire_id"] = str(affaire_id)

        where_sql = " AND ".join(where_clauses)

        if query_emb is not None:
            params["qvec"] = str(query_emb)
            sql = f"""
                SELECT id, affaire_id, scope, slug, titre, criticite, score,
                       reuse_count, updated_at, tags,
                       LEFT(contenu_md, 400) AS extrait,
                       1 - (embedding <=> :qvec::vector) AS similarity
                FROM wiki_pages
                WHERE {where_sql}
                  AND embedding IS NOT NULL
                ORDER BY embedding <=> :qvec::vector
                LIMIT :top_k
            """
        else:
            # Fallback LIKE si pas d'embedding (dev local)
            params["qnorm"] = f"%{cls.normalize_sujet(query)}%"
            sql = f"""
                SELECT id, affaire_id, scope, slug, titre, criticite, score,
                       reuse_count, updated_at, tags,
                       LEFT(contenu_md, 400) AS extrait,
                       0.0 AS similarity
                FROM wiki_pages
                WHERE {where_sql}
                  AND sujet_norm LIKE :qnorm
                ORDER BY updated_at DESC
                LIMIT :top_k
            """

        rows = (await db.execute(text(sql), params)).mappings().all()
        return [dict(r) for r in rows]

    # ── Précédents & bonus scoring ─────────────────────────────────

    @classmethod
    async def check_precedents(
        cls,
        db: AsyncSession,
        *,
        sujet: str,
        affaire_id: Optional[UUID] = None,
        top_k: int = 3,
        increment_reuse: bool = True,
    ) -> dict:
        """
        Vérifie si le sujet a déjà été traité/validé.
        Retourne le bonus à appliquer au scoring (+5 si précédent validé).

        Pour éviter de "gonfler" le score sur des correspondances faibles,
        PRECEDENT_MIN_SCORE est appliqué comme seuil cosine.
        """
        hits = await cls.find_similar(
            db, query=sujet, affaire_id=affaire_id, top_k=top_k
        )

        # On privilégie les précédents agence (pattern Mnémosyne) au-dessus
        # du seuil minimal et réellement validés (validated_at non null).
        qualifying_ids: list[str] = []
        filtered: list[dict] = []
        for hit in hits:
            similarity = float(hit.get("similarity") or 0.0)
            hit["similarity"] = similarity
            if similarity < PRECEDENT_MIN_SCORE:
                continue
            filtered.append(hit)
            # Seuls les précédents scope=agence déclenchent le bonus
            if hit["scope"] == "agence":
                qualifying_ids.append(hit["id"])

        bonus_applicable = bool(qualifying_ids)
        bonus = PRECEDENT_BONUS_POINTS if bonus_applicable else 0

        if increment_reuse and qualifying_ids:
            await db.execute(
                update(WikiPage)
                .where(WikiPage.id.in_(qualifying_ids))
                .values(reuse_count=WikiPage.reuse_count + 1)
            )
            await db.commit()

        log.info(
            "wiki.precedents_checked",
            sujet=sujet[:60],
            affaire_id=str(affaire_id) if affaire_id else None,
            total_hits=len(hits),
            qualifying=len(qualifying_ids),
            bonus=bonus,
        )

        return {
            "bonus_applicable": bonus_applicable,
            "bonus_points": bonus,
            "precedents": filtered,
        }

    # ── Export ──────────────────────────────────────────────────────

    @staticmethod
    def render_markdown(page: WikiPage) -> str:
        """
        Formate une page pour export (mode AUDIT).
        Ajoute un trailer avec métadonnées (inspiré du git audit trail llm-wiki).
        """
        tags = ", ".join(page.tags) if page.tags else "—"
        lines = [
            page.contenu_md.rstrip(),
            "",
            "---",
            f"*Scope : {page.scope} · Slug : `{page.slug}`*",
            f"*Tags : {tags}*",
        ]
        if page.criticite:
            lines.append(f"*Criticité : {page.criticite}*")
        if page.score is not None:
            lines.append(f"*Score : {page.score}/100*")
        if page.validated_at:
            lines.append(
                f"*Validé le {page.validated_at.strftime('%Y-%m-%d')}*"
            )
        lines.append(f"*Réutilisé : {page.reuse_count}×*")
        return "\n".join(lines) + "\n"
