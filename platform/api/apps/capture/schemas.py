from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class CaptureResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    status: str
    transcription: Optional[str] = None
    structured_output: Optional[dict[str, Any]] = None
    duration_seconds: Optional[int] = None
    agent_run_id: Optional[UUID] = None
    error_message: Optional[str] = None
    created_at: str

    model_config = {"from_attributes": True}


class CaptureListResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    status: str
    duration_seconds: Optional[int] = None
    created_at: str

    model_config = {"from_attributes": True}
