from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AgentRunRequest(BaseModel):
    instruction: str
    affaire_id: UUID
    agent: str = "athena"  # themis | argus | hermes | mnemosyne | athena
    max_iterations: int = 10


class AgentStep(BaseModel):
    tool: str
    args: dict
    output: str
    duration_ms: int


class AgentRunResponse(BaseModel):
    id: UUID
    affaire_id: UUID | None
    instruction: str
    result: str | None
    status: str
    steps: list[AgentStep]
    iterations: int
    duration_ms: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
