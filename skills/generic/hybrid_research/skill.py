"""Hybrid research skill — local DB + pgvector + web."""
from core.contracts.skill import SkillBase


class HybridResearch(SkillBase):
    skill_id = "hybrid_research"
    name = "Recherche hybride"
    agents = ["hermes", "hades", "argos"]

    async def run(self, context: dict) -> dict:
        return {"status": "ok", "skill": self.skill_id, "query": context.get("query")}
