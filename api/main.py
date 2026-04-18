"""
Point d'entrée de l'API OS Projet.
Ne connaît aucun module — tout passe par ModuleRegistry.load_all().
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from core.logging import configure_logging, get_logger
from database import AsyncSessionLocal
from core.settings import settings
from core.rate_limit import limiter
import core.events as events
from database import engine, Base

configure_logging()
log = get_logger("main")


def _check_migrations() -> None:
    """Vérifie que toutes les migrations Alembic sont appliquées (§23.4). Crash explicite sinon."""
    try:
        from alembic.runtime.migration import MigrationContext
        from alembic.script import ScriptDirectory
        from alembic.config import Config
        from sqlalchemy import create_engine as sync_engine

        cfg = Config("alembic.ini")
        script = ScriptDirectory.from_config(cfg)
        head = script.get_current_head()

        eng = sync_engine(settings.DATABASE_URL_SYNC)
        with eng.connect() as conn:
            ctx = MigrationContext.configure(conn)
            current = ctx.get_current_revision()
        eng.dispose()

        if current != head:
            raise RuntimeError(
                f"\n\n  ❌ Base de données non à jour.\n"
                f"  Lancer : alembic upgrade head\n"
                f"  Actuelle : {current}\n"
                f"  Attendue : {head}\n"
            )
        log.info("migrations.ok", revision=current)
    except ImportError:
        log.warning("migrations.alembic_not_found", detail="Vérification ignorée")
    except Exception as e:
        if "non à jour" in str(e):
            raise
        log.warning("migrations.check_failed", error=str(e))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────
    log.info("startup.begin", version="0.1.0", debug=settings.DEBUG)

    # 1. Vérifier les migrations (§23.4)
    if not settings.DEBUG:
        # En dev, on tolère une base non migrée (alembic upgrade head à la main)
        _check_migrations()

    # 2. Créer les tables si nécessaire (dev uniquement — prod = alembic)
    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # 3. Initialiser le bus d'événements PostgreSQL
    await events.init_pool(settings.ASYNCPG_URL)

    # 4. Créer les tables LangGraph (checkpointer HITL)
    from core.checkpointer import setup_checkpointer
    try:
        await setup_checkpointer()
        log.info("checkpointer.ready")
    except Exception as e:
        log.warning("checkpointer.setup_failed", error=str(e))

    # 5. Seed utilisateur admin par défaut
    from modules.auth.service import seed_admin
    async with AsyncSessionLocal() as db:
        await seed_admin(db)

    # 6. Charger les modules
    from core.registry import ModuleRegistry
    reg = ModuleRegistry(app)
    reg.load_all("modules.yaml")

    log.info("startup.complete", modules=reg.loaded_modules)
    yield

    # ── Shutdown ─────────────────────────────────────────────────
    await events.close_pool()
    await engine.dispose()
    log.info("shutdown.complete")


app = FastAPI(
    title="OS Projet API",
    description="Intelligence opérationnelle pour agence MOE",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# ── Middleware ───────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://openwebui:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Routes core (non-modulaires) ─────────────────────────────────
from core.health import router as health_router  # noqa: E402
app.include_router(health_router)
