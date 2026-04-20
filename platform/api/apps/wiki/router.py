"""
Router wiki — synthesis cache (pages markdown navigables).

POST   /wiki/pages/                      → créer une page manuellement
POST   /wiki/pages/from-decision/{id}    → promouvoir une décision validée
GET    /wiki/pages/                      → lister (filtres scope/affaire/tag)
GET    /wiki/pages/{slug_or_id}          → détail page
PATCH  /wiki/pages/{id}                  → éditer
POST   /wiki/pages/{id}/validate         → marquer comme validée
DELETE /wiki/pages/{id}                  → supprimer
GET    /wiki/pages/{id}/export           → markdown brut (mode AUDIT)

POST   /wiki/search                      → recherche hybride
POST   /wiki/precedents                  → lookup précédents + bonus scoring
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from database import get_db
from apps.wiki.models import WikiPage
from apps.wiki.schemas import (
    PrecedentCheckRequest,
    PrecedentResult,
    PromoteDecisionRequest,
    WikiPageCreateRequest,
    WikiPageResponse,
    WikiPageSummary,
    WikiPageUpdateRequest,
    WikiSearchHit,
    WikiSearchRequest,
)
from apps.wiki.service import WikiService

log = get_logger("wiki.router")


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def _hit_to_schema(hit: dict) -> WikiSearchHit:
    """Convertit un hit raw (dict de find_similar) en WikiSearchHit."""
    return WikiSearchHit(
        page=WikiPageSummary(
            id=hit["id"],
            scope=hit["scope"],
            slug=hit["slug"],
            titre=hit["titre"],
            tags=hit.get("tags") or [],
            criticite=hit.get("criticite"),
            score=hit.get("score"),
            reuse_count=hit.get("reuse_count") or 0,
            updated_at=hit["updated_at"],
        ),
        score=float(hit.get("similarity") or 0.0),
        extrait=hit.get("extrait") or "",
    )


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    # ── Création ────────────────────────────────────────────────────

    @router.post("/pages/", response_model=WikiPageResponse, status_code=201)
    async def create_page(
        payload: WikiPageCreateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        try:
            page = await WikiService.create_page(
                db,
                titre=payload.titre,
                contenu_md=payload.contenu_md,
                scope=payload.scope,
                affaire_id=payload.affaire_id,
                tags=payload.tags,
                criticite=payload.criticite,
                score=payload.score,
                citations=payload.citations,
                validated_by=current_user.id,
                auto_validate=True,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        return page

    @router.post(
        "/pages/from-decision/{decision_id}",
        response_model=WikiPageResponse,
        status_code=201,
    )
    async def promote_decision(
        decision_id: uuid.UUID,
        payload: PromoteDecisionRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe")),
    ):
        """Promeut une project_decision validée en page wiki."""
        try:
            page = await WikiService.promote_from_decision(
                db,
                decision_id=decision_id,
                scope=payload.scope,
                tags=payload.tags,
                contenu_md_override=payload.contenu_md_override,
                validated_by=current_user.id,
            )
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        return page

    # ── Lecture ─────────────────────────────────────────────────────

    @router.get("/pages/", response_model=list[WikiPageSummary])
    async def list_pages(
        scope: Optional[str] = Query(None, pattern="^(projet|agence)$"),
        affaire_id: Optional[uuid.UUID] = None,
        tag: Optional[str] = None,
        criticite: Optional[str] = Query(None, pattern="^C[1-5]$"),
        limit: int = Query(50, ge=1, le=200),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        query = select(WikiPage)
        if scope:
            query = query.where(WikiPage.scope == scope)
        if affaire_id:
            query = query.where(or_(WikiPage.affaire_id == affaire_id, WikiPage.scope == "agence"))
        if criticite:
            query = query.where(WikiPage.criticite == criticite)
        if tag:
            query = query.where(WikiPage.tags.contains([tag]))

        query = query.order_by(WikiPage.updated_at.desc()).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @router.get("/pages/{slug_or_id}", response_model=WikiPageResponse)
    async def get_page(
        slug_or_id: str,
        scope: Optional[str] = Query(None, pattern="^(projet|agence)$"),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """
        Résolution par UUID ou par slug.
        Pour un slug, ?scope=projet|agence est recommandé (sinon renvoie la
        première page trouvée toutes portées confondues).
        """
        if _is_uuid(slug_or_id):
            page = await db.get(WikiPage, uuid.UUID(slug_or_id))
        else:
            query = select(WikiPage).where(WikiPage.slug == slug_or_id)
            if scope:
                query = query.where(WikiPage.scope == scope)
            query = query.limit(1)
            result = await db.execute(query)
            page = result.scalar_one_or_none()

        if not page:
            raise HTTPException(status_code=404, detail="Page introuvable")
        return page

    @router.patch("/pages/{page_id}", response_model=WikiPageResponse)
    async def update_page(
        page_id: uuid.UUID,
        payload: WikiPageUpdateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe")),
    ):
        page = await db.get(WikiPage, page_id)
        if not page:
            raise HTTPException(status_code=404, detail="Page introuvable")

        updates = payload.model_dump(exclude_none=True)
        for field, value in updates.items():
            setattr(page, field, value)

        # Recalcul du sujet_norm si le titre change
        if "titre" in updates:
            page.sujet_norm = WikiService.normalize_sujet(updates["titre"])[:512]

        await db.commit()
        await db.refresh(page)
        return page

    @router.post("/pages/{page_id}/validate", response_model=WikiPageResponse)
    async def validate_page(
        page_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe")),
    ):
        page = await db.get(WikiPage, page_id)
        if not page:
            raise HTTPException(status_code=404, detail="Page introuvable")
        page.validated_by = current_user.id
        page.validated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(page)
        log.info("wiki.page_validated", page_id=str(page.id), slug=page.slug)
        return page

    @router.delete("/pages/{page_id}", status_code=204)
    async def delete_page(
        page_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        page = await db.get(WikiPage, page_id)
        if not page:
            raise HTTPException(status_code=404, detail="Page introuvable")
        await db.delete(page)
        await db.commit()

    @router.get("/pages/{page_id}/export", response_class=PlainTextResponse)
    async def export_page(
        page_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        page = await db.get(WikiPage, page_id)
        if not page:
            raise HTTPException(status_code=404, detail="Page introuvable")
        return WikiService.render_markdown(page)

    # ── Recherche & précédents ─────────────────────────────────────

    @router.post("/search", response_model=list[WikiSearchHit])
    async def search(
        payload: WikiSearchRequest,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        hits = await WikiService.find_similar(
            db,
            query=payload.query,
            affaire_id=payload.affaire_id,
            scope=payload.scope,
            top_k=payload.top_k,
        )
        return [_hit_to_schema(h) for h in hits]

    @router.post("/precedents", response_model=PrecedentResult)
    async def check_precedents(
        payload: PrecedentCheckRequest,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """
        Appelé par le module scoring pour calculer le bonus
        « +5 déjà validé dans projets passés ».
        """
        result = await WikiService.check_precedents(
            db,
            sujet=payload.sujet,
            affaire_id=payload.affaire_id,
            top_k=payload.top_k,
            increment_reuse=payload.increment_reuse,
        )
        return PrecedentResult(
            bonus_applicable=result["bonus_applicable"],
            bonus_points=result["bonus_points"],
            precedents=[_hit_to_schema(h) for h in result["precedents"]],
        )

    return router
