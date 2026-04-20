from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession


class BaseEngine(ABC):
    """Contrat minimal pour tout engine métier."""

    def __init__(self, db: AsyncSession, config: dict):
        self.db = db
        self.config = config  # issu du config.yaml du module

    @classmethod
    def name(cls) -> str:
        """Nom du module propriétaire."""
        raise NotImplementedError
