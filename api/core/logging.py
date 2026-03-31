"""
Logging structuré JSON via structlog (§23.1).
Chaque appel LLM, RAG, notification produit un log avec duration_ms + contexte métier.

Usage :
    from core.logging import get_logger
    log = get_logger(__name__)
    log.info("rag.search", affaire_id=str(id), query=query[:60], hits=5, duration_ms=120)
"""
import logging
import sys
import structlog
from core.settings import settings


def configure_logging() -> None:
    """À appeler une seule fois dans main.py au démarrage."""
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
    ]

    if settings.DEBUG:
        # Développement : sortie lisible en console
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    else:
        # Production : JSON sur stdout (filtrable Grafana Loki, etc.)
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if settings.DEBUG else logging.INFO
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(sys.stdout),
        cache_logger_on_first_use=True,
    )

    # Rediriger les loggers stdlib vers structlog
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.WARNING)


def get_logger(name: str = "arceus"):
    return structlog.get_logger(name)
