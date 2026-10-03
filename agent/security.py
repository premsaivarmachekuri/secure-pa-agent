"""L4 Security — identity, injection, size, rate. Not AI."""

from __future__ import annotations

import re
import time
from collections import defaultdict, deque
from threading import Lock

from agent.config import MAX_PROMPT_CHARS, RATE_LIMIT_PER_MINUTE, ROLES

INJECTION = re.compile(
    r"ignore\s+(all\s+)?(previous\s+)?(instructions|rules)|"
    r"jailbreak|"
    r"dump\s+tools|"
    r"list\s+(all\s+)?tools|"
    r"print\s+(the\s+)?ssn|"
    r"show\s+(the\s+)?ssn|"
    r"reveal\s+(the\s+)?(system\s+)?prompt|"
    r"override\s+(the\s+)?(safety|guard)",
    re.I,
)

_rate_lock = Lock()
_hits: dict[str, deque[float]] = defaultdict(deque)


def reset_rate_limit() -> None:
    with _rate_lock:
        _hits.clear()


def _over_rate(user_id: str) -> bool:
    now = time.monotonic()
    window = 60.0
    with _rate_lock:
        bucket = _hits[user_id]
        while bucket and now - bucket[0] > window:
            bucket.popleft()
        if len(bucket) >= RATE_LIMIT_PER_MINUTE:
            return True
        bucket.append(now)
        return False


def gate(
    *,
    user_id: str | None,
    role: str | None,
    session_id: str | None,
    prompt: str | None,
) -> tuple[str, str] | None:
    """Return (status, reason) on fail, else None to continue."""
    if not (session_id or "").strip():
        return "rejected", "missing_session"
    if not (user_id or "").strip():
        return "rejected", "missing_user"
    if (role or "").strip() not in ROLES:
        return "rejected", "invalid_role"
    text = prompt or ""
    if len(text) > MAX_PROMPT_CHARS:
        return "rejected", "oversize_prompt"
    if _over_rate(user_id.strip()):
        return "rejected", "rate_limit"
    if INJECTION.search(text):
        return "blocked", "injection"
    return None
