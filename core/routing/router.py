"""HermesRouter — maps user intent to a workflow + agent set."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class RouteResult:
    workflow: str
    agents: list[str]
    pattern: str


class HermesRouter:
    """Lightweight intent → workflow router. Extend with ML scoring for V2."""

    _PATTERNS: list[tuple[list[str], RouteResult]] = [
        (["recherche", "search", "find", "trouvez"],
         RouteResult("research", ["HERMES", "ARGOS", "PROMETHEUS", "KAIROS", "IRIS"], "research")),
        (["dossier", "rapport", "report", "document"],
         RouteResult("dossier_build", ["ATHENA", "HERMES", "ARGOS", "KAIROS", "DAEDALUS", "IRIS"], "document")),
        (["clarif", "précis", "unclear", "ambig"],
         RouteResult("clarification", ["HECATE", "IRIS"], "clarification")),
    ]
    _DEFAULT = RouteResult("simple_answer", ["KAIROS", "IRIS"], "simple")

    def route(self, intent: str, context: dict | None = None) -> RouteResult:
        lowered = intent.lower()
        for keywords, result in self._PATTERNS:
            if any(k in lowered for k in keywords):
                return result
        return self._DEFAULT
