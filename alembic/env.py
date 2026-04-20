import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add platform/api/ to path so model imports resolve correctly
sys.path.insert(0, str(Path(__file__).parent.parent / "platform" / "api"))

from core.settings import settings
from database import Base

# Import all models so Base.metadata knows about them
from apps.auth.models import User, AffairePermission  # noqa: F401
from apps.affaires.models import Affaire              # noqa: F401
from apps.documents.models import Document, Chunk     # noqa: F401
from apps.agent.models import AgentRun, AgentMemory   # noqa: F401
from apps.orchestra.models import OrchestraRun        # noqa: F401
from apps.meeting.models import MeetingCR, MeetingAction, MeetingAgenda  # noqa: F401
from apps.webhooks.models import WebhookSession                           # noqa: F401
from apps.capture.models import CaptureSession                            # noqa: F401
from apps.wiki.models import WikiPage                                     # noqa: F401
from apps.scoring.models import DecisionScore                             # noqa: F401
from apps.decisions.models import ProjectDecision, ProjectTask, ProjectObservation  # noqa: F401
from apps.planning.models import Lot, Tache, Jalon, LienDependance                # noqa: F401
from apps.chantier.models import ObservationChantier, NonConformite               # noqa: F401
from apps.communications.models import Courrier                                    # noqa: F401
from apps.finance.models import Avenant, SituationTravaux                         # noqa: F401
from apps.flowmanager.models import WorkflowDefinition                             # noqa: F401

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
