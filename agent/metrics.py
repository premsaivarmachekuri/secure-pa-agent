"""In-process counters for GET /metrics (BR-O2)."""

from __future__ import annotations

from threading import Lock

_lock = Lock()
_state = {
    "requests": 0,
    "ok": 0,
    "blocked": 0,
    "rejected": 0,
    "l1_called": 0,
    "tokens": 0,
    "cost": 0.0,
}


def record(status: str, *, l1_called: bool, tokens: int, cost: float) -> None:
    with _lock:
        _state["requests"] += 1
        if status in _state:
            _state[status] += 1
        if l1_called:
            _state["l1_called"] += 1
        _state["tokens"] += int(tokens)
        _state["cost"] += float(cost)


def snapshot() -> dict:
    with _lock:
        return dict(_state)


def reset() -> None:
    with _lock:
        for key in list(_state):
            _state[key] = 0 if key != "cost" else 0.0
