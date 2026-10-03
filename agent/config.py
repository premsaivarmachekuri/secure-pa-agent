"""Runtime flags. Secrets stay in env; never commit .env."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

MAX_TURNS = 6
MAX_PROMPT_CHARS = 8192
RATE_LIMIT_PER_MINUTE = 20
STUB_TOKENS = 48
STUB_COST = 0.0012

ROLES = frozenset({"caseworker", "clinician_reviewer", "admin"})
CASEWORKER_TOOLS = ("eligibility_min", "policy_lookup")
REVIEWER_EXTRA = ("chart_snippet", "pa_submit")


def allow_phi() -> bool:
    return os.environ.get("ALLOW_PHI", "false").lower() in {"1", "true", "yes"}


def groq_api_key() -> str:
    return (os.environ.get("GROQ_API_KEY") or "").strip()


def session_db_path() -> Path:
    raw = os.environ.get("SESSION_DB")
    if raw:
        return Path(raw)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR / "sessions.sqlite"
