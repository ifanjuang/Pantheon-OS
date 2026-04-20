"""
Veto patterns — couche 0 déterministe du structured_veto.

Avant tout appel LLM, on passe la sortie de l'agent dans un filtre
regex. Si un pattern critique est détecté, on retourne immédiatement
un VetoDecision bloquant sans consommer de token.

Couverture :
  - Patterns génériques (tout agent) : formulations explicites de refus
  - Thémis : hors mission, responsabilité MOE, contentieux, litige
  - Héphaïstos : non-conformité DTU, infaisabilité technique, sécurité
  - Apollon : contradiction normative confirmée

Règle de calibrage :
  - On cherche des formulations explicites, pas des mots isolés
  - Les faux positifs sont plus coûteux que les faux négatifs ici :
    un vrai veto manqué → le LLM le détecte en couche 1
    un faux positif → interrompt l'orchestration inutilement
  - Chaque pattern doit correspondre à une phrase d'opposition réelle,
    pas à une simple mention du concept
"""

import functools
import re
from pathlib import Path
from typing import Optional

from modules.guards.schemas import VetoDecision


# ── Patterns par agent ────────────────────────────────────────────────
# Chaque entrée : (pattern, condition_levee)
# Le pattern est compilé une fois au chargement du module (performance).

_GENERIC = [
    # Formulations explicites d'opposition / blocage
    (r"je\s+m['']oppose\b", "Lever le point de blocage identifié par l'agent"),
    (r"\bveto\s+formel\b", "Résoudre la réserve formelle avant de continuer"),
    (r"\brefus\s+(catégorique|formel|explicite)\b", "Traiter le motif de refus signalé"),
    (r"\bbloqu(ant|e|er)\s+(la\s+)?déci(sion|sion)", "Identifier et lever la condition bloquante"),
    (
        r"\brisque\s+majeur\s+non\s+(assumé|couvert|pris\s+en\s+compte)\b",
        "Formaliser la prise en charge du risque ou escalader à un expert",
    ),
    (
        r"\bexpert\s+externe\s+(requis|nécessaire|obligatoire)\b",
        "Mandater l'expert externe mentionné avant de poursuivre",
    ),
]

_THEMIS = [
    # Hors périmètre mission
    (
        r"\bhors\s+(de\s+la\s+)?mission\s+(MOE|architecte|maître\s+d'œuvre)?\b",
        "Vérifier le périmètre contractuel, éventuellement établir un avenant",
    ),
    (
        r"\bresponsabilit[eé]\s+(de\s+la\s+)?MOE\s+(est\s+)?engag[eé]e\b",
        "Valider avec le client/assureur avant toute action",
    ),
    (r"\bnon\s+couvert[e]?\s+(par\s+)?(le\s+)?contrat\b", "Établir un avenant ou rediriger vers le maître d'ouvrage"),
    (
        r"\bavenant\s+(contractuel\s+)?(obligatoire|requis|nécessaire)\b",
        "Établir et faire signer l'avenant avant de continuer",
    ),
    (
        r"\blitige\s+(potentiel|imminent|en\s+cours|probable)\b",
        "Saisir le service juridique, suspendre toute action unilatérale",
    ),
    (r"\bmise\s+en\s+demeure\b", "Transmettre au juriste, répondre dans les délais légaux"),
    (
        r"\bcontentieux\s+(juridique|contractuel|probable|imminent)\b",
        "Consulter le service juridique avant toute décision",
    ),
    (
        r"\binfraction\s+(au\s+)?(contrat|cahier\s+des\s+charges|marché)\b",
        "Documenter l'infraction et notifier formellement les parties",
    ),
    (r"\bhors\s+(p[eé]rim[eè]tre|scope)\s+(mission|contractuel)\b", "Redéfinir le périmètre ou établir un avenant"),
]

_HEPHAISTOS = [
    # Héphaïstos est diagram_builder — pas de veto technique propre
    # Les patterns DTU/sécurité sont portés par Arès (security_guard)
]

_ARES = [
    # Non-conformité technique / DTU — sécurité chantier
    (
        r"\bnon[- ]conforme\s+(au[x]?\s+)?DTU\b",
        "Obtenir un avis technique ou une dérogation auprès du bureau de contrôle",
    ),
    (
        r"\binterdit\s+(par\s+)?(le\s+)?(DTU|RE2020|ERP|règl[e]?ment)\b",
        "Consulter un BE spécialisé pour solution alternative conforme",
    ),
    (r"\binfaisabl[e]\b", "Proposer une alternative technique faisable, consulter un spécialiste"),
    (
        r"\bimpossibl[e]\s+(techniquement|structurellement|sur\s+le\s+plan\s+technique)\b",
        "Mandater une étude de faisabilité par un bureau d'études",
    ),
    (
        r"\bdanger\s+(structurel|de\s+stabilité|pour\s+la\s+structure)\b",
        "Suspendre les travaux, mandater un bureau de contrôle structure",
    ),
    (
        r"\brisque\s+(structurel|d'effondrement|de\s+ruine)\b",
        "Arrêt de chantier immédiat, expertise structure obligatoire",
    ),
    (
        r"\bs[eé]curit[eé]\s+(des\s+personnes\s+)?(en\s+)?(danger|menac[eé]e|compromise)\b",
        "Mesures conservatoires immédiates, déclaration à l'inspection du travail",
    ),
]

_APOLLON = [
    # Contradiction normative confirmée
    (
        r"\bcontradiction\s+(normative|r[eè]glementaire)\s+(confirm[eé]e|av[eé]r[eé]e|établie)\b",
        "Arbitrage normatif par le CSTB ou bureau de contrôle",
    ),
    (
        r"\bincoh[eé]rence\s+(majeure\s+)?(r[eè]glementaire|normative)\s+(confirm[eé]e|établie)\b",
        "Demander une interprétation officielle à l'organisme normalisateur",
    ),
    (
        r"\bcontradiction\s+(entre|avec)\s+(l[''])?article\s+\d",
        "Clarifier l'interprétation réglementaire applicable avec un expert",
    ),
]

# Compilation au chargement (LRU natif Python pour modules)
_COMPILED: dict[str, list[tuple[re.Pattern, str]]] = {
    "_generic": [(re.compile(p, re.IGNORECASE), cond) for p, cond in _GENERIC],
    "themis": [(re.compile(p, re.IGNORECASE), cond) for p, cond in _THEMIS],
    "hephaistos": [(re.compile(p, re.IGNORECASE), cond) for p, cond in _HEPHAISTOS],
    "ares": [(re.compile(p, re.IGNORECASE), cond) for p, cond in _ARES],
    "apollon": [(re.compile(p, re.IGNORECASE), cond) for p, cond in _APOLLON],
}


@functools.lru_cache(maxsize=1)
def _load_domain_compiled() -> dict[str, list[tuple[re.Pattern, str]]]:
    """Charge et compile les veto_patterns du domaine actif depuis agents/domains/{DOMAIN}.yaml."""
    try:
        import yaml  # type: ignore[import]
    except ImportError:
        return {}
    try:
        from core.settings import settings

        domain = getattr(settings, "DOMAIN", "btp")
    except Exception:
        domain = "btp"

    agents_dir = Path(__file__).parent.parent.parent.parent / "agents"
    overlay_path = agents_dir / "domains" / f"{domain}.yaml"
    if not overlay_path.exists():
        return {}
    try:
        data = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        veto_raw: dict = data.get("veto_patterns", {})
        result: dict[str, list[tuple[re.Pattern, str]]] = {}
        for agent_key, patterns in veto_raw.items():
            compiled = []
            for entry in patterns:
                if isinstance(entry, list) and len(entry) == 2:
                    try:
                        compiled.append((re.compile(entry[0], re.IGNORECASE), entry[1]))
                    except re.error:
                        pass
            if compiled:
                result[agent_key] = compiled
        return result
    except Exception:
        return {}


def fast_veto_check(agent: str, output: str) -> Optional[VetoDecision]:
    """Couche 0 : détection déterministe de veto sans appel LLM.

    Teste les patterns génériques, les patterns agent statiques (BTP), puis
    les patterns domaine-spécifiques chargés depuis agents/domains/{DOMAIN}.yaml.

    Retourne un VetoDecision bloquant si un pattern critique est trouvé,
    None sinon → l'appelant passe alors en couche 1 (LLM structured_veto).
    """
    agent_lower = agent.lower()
    domain_compiled = _load_domain_compiled()

    # Patterns génériques d'abord (toujours appliqués)
    for pattern, condition_levee in _COMPILED["_generic"]:
        m = pattern.search(output)
        if m:
            return VetoDecision(
                veto=True,
                agent=agent,
                severity="bloquant",
                motif=f"Pattern critique détecté (générique) : «{m.group(0)}»",
                condition_levee=condition_levee,
            )

    # Patterns domaine actif (priorité sur les patterns statiques BTP)
    for pattern, condition_levee in domain_compiled.get(agent_lower, []):
        m = pattern.search(output)
        if m:
            return VetoDecision(
                veto=True,
                agent=agent,
                severity="bloquant",
                motif=f"Pattern domaine {agent_lower} : «{m.group(0)}»",
                condition_levee=condition_levee,
            )

    # Patterns statiques spécifiques à l'agent (BTP — fallback si domaine non-BTP sans pattern)
    for pattern, condition_levee in _COMPILED.get(agent_lower, []):
        m = pattern.search(output)
        if m:
            return VetoDecision(
                veto=True,
                agent=agent,
                severity="bloquant",
                motif=f"Pattern {agent_lower} détecté : «{m.group(0)}»",
                condition_levee=condition_levee,
            )

    return None
