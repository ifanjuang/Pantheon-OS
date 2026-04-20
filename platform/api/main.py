"""
Pantheon OS — FastAPI entry point.
Loads modules dynamically via ModuleRegistry.
MVP: no LangGraph checkpointer, no Redis/ARQ queue.
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
from database import engine, Base

configure_logging()
log = get_logger("main")


def _check_migrations() -> None:
    """Crash explicitly if Alembic migrations are not up to date."""
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
                f"\n\n  ❌ Database not up to date.\n"
                f"  Run: alembic upgrade head\n"
                f"  Current: {current}\n"
                f"  Expected: {head}\n"
            )
        log.info("migrations.ok", revision=current)
    except ImportError:
        log.warning("migrations.alembic_not_found")
    except Exception as e:
        if "not up to date" in str(e) or "non à jour" in str(e):
            raise
        log.warning("migrations.check_failed", error=str(e))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────
    log.info("startup.begin", version="1.0.0", debug=settings.DEBUG)

    # 1. Check migrations (prod only)
    if not settings.DEBUG:
        _check_migrations()

    # 2. Create tables in dev (prod = alembic upgrade head)
    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # 3. Load Hermes Runtime registries (auto-discovery via manifest.yaml files)
    from core.registries.loader import ManifestLoader
    from pathlib import Path
    loader = ManifestLoader(Path("/modules"))
    agents = loader.load_agents()
    skills = loader.load_skills()
    workflows = loader.load_workflows()
    log.info("hermes.registries_loaded", agents=len(agents), skills=len(skills), workflows=len(workflows))

    # 4. Seed default admin user
    from apps.auth.service import seed_admin
    async with AsyncSessionLocal() as db:
        await seed_admin(db)

    # 5. Load API apps
    from core.registry import ModuleRegistry
    reg = ModuleRegistry(app)
    reg.load_all("modules.yaml")

    log.info("startup.complete", modules=reg.loaded_modules)
    yield

    # ── Shutdown ─────────────────────────────────────────────────
    await engine.dispose()
    log.info("shutdown.complete")


app = FastAPI(
    title="Pantheon OS API",
    description="Hermes Runtime — multi-agent intelligence platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# ── Middleware ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://openwebui:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Core routes (non-module) ────────────────────────────────────────
from core.health import router as health_router  # noqa: E402

app.include_router(health_router)
