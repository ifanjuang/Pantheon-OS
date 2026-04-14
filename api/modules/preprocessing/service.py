"""
PreprocessingService — normalisation d'entrée (Hermès++) et gate Precheck.

Deux fonctions principales :

  preprocess()
    Appelée en tête du graphe Zeus (nœud `preprocess`).
    Transforme une demande brute en PreprocessedInput (cleaned_question,
    reformulated_question, intent, phase/domaine, missing_information,
    confidence, suggested_criticite).

  precheck()
    Appelée entre `zeus_distribute` et `dispatch_subtasks`.
    Évalue si le plan Zeus est bien dimensionné. Verdicts :
      - approved       → exécuter tel quel
      - trim           → subtask_ids à garder (plan surdimensionné)
      - upgrade        → relever la criticité
      - clarification  → infos manquantes bloquantes
      - blocked        → demande hors scope / incompréhensible

Usage orchestra :
  preprocess → plan_agents → zeus_distribute → workflow_precheck
                                                 │
                                 approved|trim|upgrade  clarification|blocked
                                                 ▼                    ▼
                                        dispatch_subtasks            END
"""
from typing import Optional

from core.logging import get_logger
from core.services.llm_service import LlmService
from modules.preprocessing.schemas import PreprocessedInput, PrecheckDecision

log = get_logger("preprocessing.service")


_PREPROCESS_PROMPT = """\
Tu es Hermès, agent d'interface et de qualification ARCEUS.
Transforme une entrée brute en données opérationnelles.

## Entrée brute
{message}

## Contexte agence
- Affaire détectée : {affaire}
- Phase indiquée   : {phase}
- Domaine indiqué  : {domaine}

## Objectif
Produis un JSON strict avec :
1. cleaned_question      : message sans salutations, fautes, ponctuation parasite
2. reformulated_question : même demande reformulée en mode opérationnel
                           (objectif explicite, 1-2 phrases)
3. intent                : "information" | "question" | "decision_locale"
                           | "decision_engageante" | "alerte" | "production"
4. phase_projet          : ESQ/APS/APD/PRO/ACT/VISA/DET/AOR/Hors-phase
                           (null si inconnu)
5. domaine               : Technique/Contractuel/Planning/Relationnel/
                           Administratif/Financier (null si inconnu)
6. project_detected      : nom/numéro/adresse d'affaire trouvé (null sinon)
7. missing_information   : liste des infos critiques manquantes pour trancher
8. confidence            : 0.0-1.0 — confiance globale de l'interprétation
9. suggested_criticite   : C1-C5 estimée
                             C1 = info pure
                             C2 = question
                             C3 = décision locale réversible
                             C4 = décision engageante
                             C5 = risque majeur

Sois strict : si la demande est ambiguë, baisse la confiance et liste
explicitement les infos manquantes.
"""


_PRECHECK_PROMPT = """\
Tu es le gate Precheck ARCEUS. Zeus vient de décomposer la demande en
sous-tâches. Valide ou ajuste AVANT l'exécution coûteuse.

## Demande (reformulée)
{instruction}

## Criticité actuelle
{criticite}

## Plan Zeus
{subtasks_text}

## Contexte preprocessing
Confidence entrée : {confidence}
Infos manquantes  : {missing}

## Verdicts possibles
- "approved"       : plan bien dimensionné → exécuter tel quel
- "trim"           : plan surdimensionné → suggested_subtask_ids à conserver
- "upgrade"        : criticité sous-estimée → suggested_criticite corrigée
- "clarification"  : infos manquantes bloquantes → clarification_message
- "blocked"        : demande hors scope / incompréhensible → clarification_message

## Règles
- C1 (info simple) avec plan ≥ 3 subtasks → trim ou blocked
- C2 (question) avec pattern arena/exploration → trim (solo ou parallel 2 agents suffit)
- Infos contractuelles/techniques critiques manquantes → clarification
- Demande mentionne risque/sécurité/contentieux/péril mais criticité ≤ C3 → upgrade C5
- Demande mentionne engagement ferme / signature / contrat mais criticité ≤ C2 → upgrade C4
- Sinon → approved

reasoning : 1-2 phrases en français.
"""


class PreprocessingService:

    @classmethod
    async def preprocess(
        cls,
        message: str,
        *,
        affaire_hint: Optional[str] = None,
        phase_hint: Optional[str] = None,
        domaine_hint: Optional[str] = None,
    ) -> PreprocessedInput:
        """Normalise une demande brute via LLM + Instructor.

        Fallback silencieux : en cas d'erreur LLM, retourne la demande
        brute avec confidence=0.3 pour ne pas bloquer le graphe Zeus.
        """
        prompt = _PREPROCESS_PROMPT.format(
            message=message[:4000],
            affaire=affaire_hint or "—",
            phase=phase_hint or "—",
            domaine=domaine_hint or "—",
        )
        try:
            result = await LlmService.extract(
                messages=[{"role": "user", "content": prompt}],
                response_model=PreprocessedInput,
                temperature=0.1,
            )
            log.info(
                "preprocessing.done",
                intent=result.intent,
                criticite=result.suggested_criticite,
                confidence=round(result.confidence, 2),
                missing=len(result.missing_information),
            )
            return result
        except Exception as exc:
            log.warning("preprocessing.failed", error=str(exc))
            return PreprocessedInput(
                cleaned_question=message.strip(),
                reformulated_question=message.strip(),
                intent="question",
                phase_projet=phase_hint,
                domaine=domaine_hint,
                project_detected=affaire_hint,
                missing_information=[],
                confidence=0.3,
                suggested_criticite=None,
            )

    @classmethod
    async def precheck(
        cls,
        *,
        instruction: str,
        criticite: str,
        subtasks: list[dict],
        preprocessed: Optional[PreprocessedInput] = None,
    ) -> PrecheckDecision:
        """Évalue si le plan Zeus est bien dimensionné.

        Fallback permissif : en cas d'erreur LLM, retourne "approved"
        pour ne pas bloquer l'orchestration.
        """
        if subtasks:
            subtasks_text = "\n".join(
                f"- [{st.get('id', '?')}] pattern={st.get('pattern')} "
                f"agents={st.get('agents')} → {(st.get('instruction') or '')[:120]}"
                for st in subtasks
            )
        else:
            subtasks_text = "(aucune subtask)"

        prompt = _PRECHECK_PROMPT.format(
            instruction=instruction[:2000],
            criticite=criticite,
            subtasks_text=subtasks_text,
            confidence=(
                f"{preprocessed.confidence:.2f}" if preprocessed else "1.00"
            ),
            missing=(
                ", ".join(preprocessed.missing_information)
                if preprocessed and preprocessed.missing_information
                else "—"
            ),
        )
        try:
            result = await LlmService.extract(
                messages=[{"role": "user", "content": prompt}],
                response_model=PrecheckDecision,
                temperature=0.1,
            )
            log.info(
                "preprocessing.precheck",
                verdict=result.verdict,
                reasoning=result.reasoning[:160],
            )
            return result
        except Exception as exc:
            log.warning("preprocessing.precheck_failed", error=str(exc))
            return PrecheckDecision(
                verdict="approved",
                reasoning=(
                    f"Precheck LLM indisponible — approuvé par défaut. "
                    f"Erreur : {exc}"
                ),
            )
