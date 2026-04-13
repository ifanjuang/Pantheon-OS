"""
OrchestraRun — trace d'une exécution multi-agents orchestrée par Zeus.
"""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class OrchestraRun(Base):
    __tablename__ = "orchestra_runs"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    affaire_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("affaires.id", ondelete="SET NULL"), nullable=True
    )
    user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    instruction: Mapped[str] = mapped_column(Text, nullable=False)
    initial_agents: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Phase 1 — plans
    agent_plans: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # Phase 2 — distribution Zeus
    zeus_reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    assignments: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # Décomposition Zeus structurée (subtasks topologiques) — persistée pour audit
    subtasks: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Phase 3 — résultats d'exécution
    agent_results: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # Résultats par sous-tâche : {task_id: {agent_name: result_text}}
    subtask_results: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    agent_run_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Veto Thémis / Héphaïstos (vide si aucun)
    veto_agent: Mapped[str | None] = mapped_column(String(64), nullable=True)
    veto_motif: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Phase 4 — synthèse
    final_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    synthesis_agent: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Erreur séparée du contenu produit (ne mélange plus échec ↔ final_answer)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Human-in-the-loop
    hitl_enabled: Mapped[bool] = mapped_column(nullable=False, default=False)
    # status = "awaiting_approval" quand Zeus attend la validation humaine
    hitl_payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    # {reasoning, assignments, message} — propositions de Zeus à valider
    checkpoint_thread_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # thread_id LangGraph pour reprendre le graphe suspendu

    # Criticité C1-C5
    criticite: Mapped[str] = mapped_column(String(2), nullable=False, default="C2")
    # C1=info | C2=question | C3=décision locale | C4=décision engageante | C5=risque majeur

    # Scoring décisionnel (nœud score_decision)
    score_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    score_verdict: Mapped[str | None] = mapped_column(String(16), nullable=True)
    score_total: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Mémoires écrites (nœud write_memories)
    memories_written: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    wiki_page_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Meta
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="running")
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
