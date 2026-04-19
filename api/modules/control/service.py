from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID

import yaml
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from modules.agent.models import AgentRun
from modules.orchestra._shared import get_agent_role
from modules.orchestra.models import OrchestraRun
from .schemas import ErrorEntry, ModuleStatus, RunSummary, TraceEvent

log = get_logger("control.service")

_MODULES_YAML = Path(__file__).parents[3] / "modules.yaml"
_MANIFESTS_DIR = Path(__file__).parents[2]


class ControlService:
    @staticmethod
    def get_modules() -> list[ModuleStatus]:
        try:
            with open(_MODULES_YAML) as f:
                data = yaml.safe_load(f)
        except Exception:
            return []

        result = []
        for mod in data.get("modules", []):
            name = mod["name"]
            enabled = mod.get("enabled", True)
            version, prefix, description, depends_on = "1.0.0", f"/{name}", "", []

            manifest_path = _MANIFESTS_DIR / name / "manifest.yaml"
            if manifest_path.exists():
                try:
                    with open(manifest_path) as f:
                        m = yaml.safe_load(f) or {}
                    version = m.get("version", "1.0.0")
                    prefix = m.get("prefix", f"/{name}")
                    description = m.get("description", "")
                    depends_on = m.get("depends_on", [])
                except Exception:
                    pass

            result.append(
                ModuleStatus(
                    name=name,
                    status="loaded" if enabled else "disabled",
                    version=str(version),
                    prefix=prefix,
                    description=description,
                    depends_on=depends_on,
                )
            )
        return result

    @staticmethod
    async def get_runs(
        db: AsyncSession,
        limit: int = 50,
        status: str | None = None,
        criticite: str | None = None,
    ) -> list[RunSummary]:
        stmt = select(OrchestraRun).order_by(desc(OrchestraRun.created_at)).limit(limit)
        if status:
            stmt = stmt.where(OrchestraRun.status == status)
        if criticite:
            stmt = stmt.where(OrchestraRun.criticite == criticite)

        rows = (await db.execute(stmt)).scalars().all()
        result = []
        for run in rows:
            agents: list[str] = []
            if run.agent_results:
                agents = list(run.agent_results.keys())[:6]
            elif run.assignments:
                agents = [a.get("agent", "") for a in run.assignments if a.get("agent")][:6]
            result.append(
                RunSummary(
                    run_id=str(run.id),
                    criticite=run.criticite or "C1",
                    status=run.status,
                    instruction_excerpt=(run.instruction or "")[:80],
                    agents_involved=agents,
                    started_at=run.created_at,
                    duration_ms=run.duration_ms,
                    veto_severity=run.veto_severity,
                    affaire_id=str(run.affaire_id) if run.affaire_id else None,
                    error_message=run.error_message,
                )
            )
        return result

    @staticmethod
    async def get_trace(db: AsyncSession, run_id: UUID) -> list[TraceEvent]:
        run = await db.get(OrchestraRun, run_id)
        if not run:
            return []

        events: list[TraceEvent] = []
        t0 = run.created_at
        dur = run.duration_ms or 5000

        events.append(
            TraceEvent(
                type="orchestra.started",
                run_id=str(run_id),
                timestamp=t0,
                agent="orchestra",
                role="system",
                payload={"criticite": run.criticite, "instruction": (run.instruction or "")[:100]},
            )
        )

        if run.preprocessed_input:
            events.append(
                TraceEvent(
                    type="hermes.classified",
                    run_id=str(run_id),
                    timestamp=t0 + timedelta(milliseconds=300),
                    agent="hermes",
                    role=get_agent_role("hermes"),
                    payload={
                        "criticite": run.preprocessed_input.get("suggested_criticite", run.criticite),
                        "intent": run.preprocessed_input.get("intent", ""),
                        "precheck": run.precheck_verdict or "approved",
                    },
                )
            )

        assigned_agents: list[str] = []
        if run.assignments:
            assigned_agents = [a.get("agent", "") for a in run.assignments if a.get("agent")]
            events.append(
                TraceEvent(
                    type="zeus.routing_completed",
                    run_id=str(run_id),
                    timestamp=t0 + timedelta(milliseconds=800),
                    agent="zeus",
                    role=get_agent_role("zeus"),
                    payload={"agents": assigned_agents, "count": len(assigned_agents)},
                )
            )

        # Per-agent results (timestamps approximés depuis les durations)
        n = len(assigned_agents) or 1
        for i, agent_name in enumerate(assigned_agents):
            frac = 0.15 + 0.55 * i / n
            agent_t = t0 + timedelta(milliseconds=dur * frac)
            excerpt = ""
            if run.agent_results:
                excerpt = str(run.agent_results.get(agent_name, ""))[:80]
            events.append(
                TraceEvent(
                    type=f"{agent_name}.run_completed",
                    run_id=str(run_id),
                    timestamp=agent_t,
                    agent=agent_name,
                    role=get_agent_role(agent_name),
                    payload={"excerpt": excerpt},
                )
            )

        if run.veto_agent:
            events.append(
                TraceEvent(
                    type="veto.raised",
                    run_id=str(run_id),
                    timestamp=t0 + timedelta(milliseconds=dur * 0.75),
                    agent=run.veto_agent,
                    role=get_agent_role(run.veto_agent),
                    payload={
                        "severity": run.veto_severity,
                        "motif": (run.veto_motif or "")[:120],
                    },
                )
            )

        if run.hitl_enabled and run.hitl_payload:
            events.append(
                TraceEvent(
                    type="hitl.awaiting_approval",
                    run_id=str(run_id),
                    timestamp=t0 + timedelta(milliseconds=dur * 0.85),
                    agent="zeus",
                    role=get_agent_role("zeus"),
                    payload={"message": (run.hitl_payload.get("message") or "")[:100]},
                )
            )

        if run.status in ("completed", "failed", "awaiting_approval") or run.final_answer:
            synthesis = run.synthesis_agent or "zeus"
            events.append(
                TraceEvent(
                    type=f"orchestra.{run.status}",
                    run_id=str(run_id),
                    timestamp=t0 + timedelta(milliseconds=dur),
                    agent=synthesis,
                    role=get_agent_role(synthesis),
                    payload={
                        "status": run.status,
                        "duration_ms": run.duration_ms,
                        "has_veto": run.veto_agent is not None,
                        "memories_written": run.memories_written,
                        "score_verdict": run.score_verdict,
                    },
                )
            )

        events.sort(key=lambda e: e.timestamp)
        return events

    @staticmethod
    async def get_errors(db: AsyncSession, limit: int = 50) -> list[ErrorEntry]:
        stmt_orch = (
            select(OrchestraRun)
            .where(OrchestraRun.status == "failed")
            .order_by(desc(OrchestraRun.created_at))
            .limit(limit // 2)
        )
        orch_rows = (await db.execute(stmt_orch)).scalars().all()

        stmt_agent = (
            select(AgentRun).where(AgentRun.status == "failed").order_by(desc(AgentRun.created_at)).limit(limit // 2)
        )
        agent_rows = (await db.execute(stmt_agent)).scalars().all()

        errors: list[ErrorEntry] = []

        for run in orch_rows:
            errors.append(
                ErrorEntry(
                    severity="error",
                    source="orchestra",
                    message=run.error_message or "Orchestra run failed",
                    run_id=str(run.id),
                    timestamp=run.created_at,
                )
            )
            if run.veto_agent and run.veto_severity == "bloquant":
                errors.append(
                    ErrorEntry(
                        severity="warning",
                        source=run.veto_agent,
                        message=f"Veto bloquant : {(run.veto_motif or '')[:80]}",
                        run_id=str(run.id),
                        timestamp=run.created_at,
                    )
                )

        for run in agent_rows:
            errors.append(
                ErrorEntry(
                    severity="error",
                    source="agent",
                    message=run.error_message or "Agent run failed",
                    run_id=None,
                    timestamp=run.created_at,
                )
            )

        errors.sort(key=lambda e: e.timestamp, reverse=True)
        return errors[:limit]
