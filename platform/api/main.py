"""
Pantheon Next — Hermes-backed Domain Layer API entry point.

This API no longer boots the previous autonomous runtime by default.
It exposes Pantheon Next definitions that Hermes Agent can execute and OpenWebUI
can surface/retrieve. Legacy runtime components remain in the repository for
post-pivot audit, not automatic startup.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pantheon_domain.router import router as domain_router
from pantheon_runtime.router import router as runtime_router

app = FastAPI(
    title="Pantheon Next Domain Layer API",
    description=(
        "Pantheon Next defines agents, workflows, skill contracts, memory rules "
        "and knowledge strategy for a Hermes-backed / OpenWebUI-facing system. "
        "It is a governance/context API, not the final OpenAI-compatible model backend."
    ),
    version="2.0.0-domain-layer",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://openwebui:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(domain_router)
app.include_router(runtime_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "mode": "hermes_backed_domain_layer",
        "doctrine": "Pantheon Next defines. Hermes executes. OpenWebUI exposes and retrieves.",
    }


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {
        "service": "Pantheon Next Domain Layer API",
        "health": "/health",
        "domain_snapshot": "/domain/snapshot",
        "context_pack": "/runtime/context-pack",
        "docs": "/docs",
    }
