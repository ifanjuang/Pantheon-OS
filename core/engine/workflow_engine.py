"""WorkflowEngine — executes a sequence of agent steps."""
from __future__ import annotations
import asyncio
from typing import Any


class WorkflowEngine:
    """Runs workflow steps sequentially or in parallel based on the execution plan."""

    def __init__(self, registry: Any, state: Any):
        self._registry = registry
        self._state = state

    async def run(self, plan: dict) -> dict:
        results: dict[str, Any] = {}
        for step in plan.get("steps", []):
            step_id = step["id"]
            agents = step.get("agents", [])
            instruction = step.get("instruction", "")
            parallel = step.get("parallel", False)
            depends_on = step.get("depends_on", [])

            # resolve dependencies
            context = {dep: results.get(dep) for dep in depends_on}
            context["instruction"] = instruction

            if parallel and len(agents) > 1:
                tasks = [self._run_agent(a, context) for a in agents]
                outputs = await asyncio.gather(*tasks)
                results[step_id] = dict(zip(agents, outputs))
            else:
                for agent_name in agents:
                    results[step_id] = await self._run_agent(agent_name, context)

        return results

    async def _run_agent(self, agent_name: str, context: dict) -> dict:
        agent_cls = self._registry.get(agent_name)
        if agent_cls is None:
            return {"error": f"Agent {agent_name!r} not found"}
        # Minimal stub — concrete agents override run()
        return {"agent": agent_name, "status": "ok", "context": context}
