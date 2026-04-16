import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

# Ajouter api/ au path pour importer les modèles
sys.path.insert(0, str(Path(__file__).parent.parent / "api"))

from core.settings import settings
from database import Base

# Importer tous les modèles pour que Base.metadata les connaisse
from modules.auth.models import User, AffairePermission  # noqa: F401
from modules.affaires.models import Affaire              # noqa: F401
from modules.documents.models import Document, Chunk     # noqa: F401
from modules.agent.models import AgentRun, AgentMemory   # noqa: F401
from modules.orchestra.models import OrchestraRun        # noqa: F401
from modules.meeting.models import MeetingCR, MeetingAction, MeetingAgenda  # noqa: F401
from modules.webhooks.models import WebhookSession                           # noqa: F401
from modules.capture.models import CaptureSession                            # noqa: F401
from modules.wiki.models import WikiPage                                     # noqa: F401
from modules.scoring.models import DecisionScore                             # noqa: F401
from modules.decisions.models import ProjectDecision, ProjectTask, ProjectObservation  # noqa: F401
from modules.planning.models import Lot, Tache, Jalon, LienDependance                # noqa: F401
from modules.chantier.models import ObservationChantier, NonConformite               # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override URL depuis les settings (prend la priorité sur alembic.ini)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_SYNC)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
