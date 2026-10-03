"""FastAPI surface: POST /chat, GET /health, GET /metrics."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Header
from pydantic import BaseModel, Field

from agent.metrics import snapshot
from agent.orchestrator import handle

app = FastAPI(title="Secure PA Agent", version="0.1.0")


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=0)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> dict[str, Any]:
    return snapshot()


@app.post("/chat")
def chat(
    body: ChatRequest,
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
    x_role: str | None = Header(default=None, alias="X-Role"),
    x_session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    return handle(
        user_id=x_user_id,
        role=x_role,
        session_id=x_session_id,
        prompt=body.prompt,
    )
