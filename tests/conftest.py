"""
Fixtures partagées pour tous les tests ARCEUS.

Stratégie :
- DB réelle PostgreSQL (arceus_test) — test des requêtes SQL/pgvector
- Services externes mockés : MinIO, Ollama/LLM, events PostgreSQL LISTEN/NOTIFY
- Chaque test reçoit une session DB annulée après exécution (rollback)
- Tokens JWT créés directement (sans appel HTTP au login)
"""
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from unittest.mock import AsyncMock, MagicMock

# ── Import de tous les modèles AVANT create_all ──────────────────────────────
from modules.auth.models import AffairePermission, User  # noqa: F401
from modules.affaires.models import Affaire              # noqa: F401
from modules.documents.models import Chunk, Document     # noqa: F401
from modules.agent.models import AgentRun, AgentMemory   # noqa: F401
from modules.orchestra.models import OrchestraRun        # noqa: F401
from modules.capture.models import CaptureSession        # noqa: F401

from core.auth import create_access_token
from core.settings import settings
from database import Base, get_db

# ── URL base de données de test ──────────────────────────────────────────────
# Remplace le nom de la base par arceus_test
# Gère les deux cas : @db: (docker) et @localhost: (local)
TEST_DB_URL = (
    settings.DATABASE_URL
    .replace("/arceus", "/arceus_test")
)


# ── Engine de test (session scope — créé une seule fois) ─────────────────────

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


# ── Session DB par test (rollback automatique) ───────────────────────────────

@pytest.fixture
async def db(test_engine) -> AsyncSession:
    Session = async_sessionmaker(
        bind=test_engine, expire_on_commit=False, autoflush=False
    )
    async with Session() as session:
        yield session
        await session.rollback()


# ── Application FastAPI de test (pas de lifespan) ────────────────────────────

@pytest.fixture
async def client(db, mocker):
    """
    Client HTTP branché sur une app FastAPI minimale :
    - Mêmes routers que la prod (chargés depuis modules.yaml)
    - DB overridée → session de test (rollback)
    - MinIO, LLM, events → mockés
    """
    # Mocker les services externes
    mocker.patch("core.events.init_pool", new_callable=AsyncMock)
    mocker.patch("core.events.close_pool", new_callable=AsyncMock)
    mocker.patch(
        "core.services.storage_service.StorageService._get_client",
        return_value=_mock_minio(),
    )
    mocker.patch(
        "core.services.llm_service.LlmService._get_client",
        return_value=_mock_openai_client(),
    )

    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from slowapi import _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded
    from core.health import router as health_router
    from core.rate_limit import limiter
    from core.registry import ModuleRegistry

    test_app = FastAPI(title="ARCEUS Test")
    test_app.add_middleware(
        CORSMiddleware, allow_origins=["*"],
        allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
    )
    test_app.state.limiter = limiter
    test_app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    test_app.include_router(health_router)

    # Charger les modules (même modules.yaml que la prod)
    reg = ModuleRegistry(test_app)
    reg.load_all("modules.yaml")

    # Override get_db → session de test
    async def _override_db():
        yield db

    test_app.dependency_overrides[get_db] = _override_db

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as c:
        yield c


# ── Helpers utilisateurs ─────────────────────────────────────────────────────

@pytest.fixture
async def admin_user(db) -> User:
    from modules.auth.service import create_user
    user = await create_user(db, "admin@test.fr", "password123", "Admin Test", "admin")
    await db.commit()
    return user


@pytest.fixture
async def moe_user(db) -> User:
    from modules.auth.service import create_user
    user = await create_user(db, "moe@test.fr", "password123", "MOE Test", "moe")
    await db.commit()
    return user


@pytest.fixture
async def lecteur_user(db) -> User:
    from modules.auth.service import create_user
    user = await create_user(db, "lecteur@test.fr", "password123", "Lecteur Test", "lecteur")
    await db.commit()
    return user


# ── Helpers tokens JWT ───────────────────────────────────────────────────────

@pytest.fixture
def admin_token(admin_user) -> str:
    return create_access_token({"sub": str(admin_user.id), "role": "admin"})


@pytest.fixture
def moe_token(moe_user) -> str:
    return create_access_token({"sub": str(moe_user.id), "role": "moe"})


@pytest.fixture
def lecteur_token(lecteur_user) -> str:
    return create_access_token({"sub": str(lecteur_user.id), "role": "lecteur"})


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ── Helpers affaires ─────────────────────────────────────────────────────────

@pytest.fixture
async def affaire(db, admin_user) -> Affaire:
    from modules.affaires.service import create_affaire
    a = await create_affaire(
        db,
        code="TEST-001",
        nom="Résidence Test",
        description="Projet de test",
        statut="actif",
        created_by=admin_user.id,
    )
    await db.commit()
    return a


# ── Mocks services externes ──────────────────────────────────────────────────

def _mock_minio() -> MagicMock:
    client = MagicMock()
    client.bucket_exists.return_value = True
    client.put_object.return_value = None
    client.get_object.return_value = MagicMock(read=lambda: b"fake content", close=lambda: None)
    client.remove_object.return_value = None
    return client


def _mock_openai_client() -> MagicMock:
    """Mock du client OpenAI pour les tests LLM."""
    mock = MagicMock()
    # Mock chat completions
    choice = MagicMock()
    choice.message.content = "Réponse de test de l'agent."
    choice.message.tool_calls = None
    choice.message.model_dump.return_value = {
        "role": "assistant", "content": "Réponse de test."
    }
    mock.chat.completions.create = AsyncMock(
        return_value=MagicMock(choices=[choice], usage=None)
    )
    return mock
