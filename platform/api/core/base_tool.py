from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Wrapper OpenWebUI — appelle l'API REST interne avec le JWT de l'utilisateur.
    Aucune logique métier ici : uniquement des appels HTTP.
    """

    api_base: str = "http://api:8000"

    @abstractmethod
    def get_tools(self) -> list[dict]:
        """Retourne la liste des tools au format OpenWebUI."""
        ...
