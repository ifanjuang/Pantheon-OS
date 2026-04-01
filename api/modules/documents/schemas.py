from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    affaire_id: UUID | None
    nom: str
    couche: str
    type_doc: str
    mime_type: str
    taille_octets: int
    storage_key: str
    created_at: datetime

    model_config = {"from_attributes": True}


class SearchRequest(BaseModel):
    query: str
    affaire_id: UUID
    top_k: int = 5
    source_type: str | None = None


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    contenu: str
    meta: dict
    score: float


class IngestResponse(BaseModel):
    document_id: UUID
    nom: str
    storage_key: str
    chunks_created: int
