from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture()
def client(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.setenv("ALLOW_PHI", "false")
    monkeypatch.setenv("SESSION_DB", str(tmp_path / "sessions.sqlite"))
    from agent.metrics import reset
    from agent.security import reset_rate_limit

    reset()
    reset_rate_limit()
    from agent.app import app

    return TestClient(app)
