"""Code entry. Every turn: L4 → L3 → L2 → L1."""

from __future__ import annotations

from typing import Any

from agent import llm, metrics, security, session, tools
from agent.redact import redact_obj, redact_text


def handle(
    *,
    user_id: str | None,
    role: str | None,
    session_id: str | None,
    prompt: str | None,
) -> dict[str, Any]:
    text = prompt or ""
    fail = security.gate(
        user_id=user_id, role=role, session_id=session_id, prompt=text
    )
    if fail is not None:
        status, reason = fail
        response = _base(
            status=status,
            user_id=user_id,
            role=role,
            session_id=session_id,
            text=f"{status}: {reason}",
            tools_exposed=[],
            l1_called=False,
            tokens=0,
            cost=0.0,
        )
        metrics.record(status, l1_called=False, tokens=0, cost=0.0)
        return redact_obj(response)

    assert user_id and role and session_id
    window = session.load(session_id)
    exposed, tool_results = tools.run_tools(role, text)
    member_id = (tool_results.get("refs") or {}).get("member_id") or window.get(
        "member_id"
    )
    bound = window.get("member_id")
    if bound and member_id and bound != member_id:
        response = _base(
            status="rejected",
            user_id=user_id,
            role=role,
            session_id=session_id,
            text="rejected: session is bound to one Patient",
            tools_exposed=exposed,
            l1_called=False,
            tokens=0,
            cost=0.0,
        )
        metrics.record("rejected", l1_called=False, tokens=0, cost=0.0)
        return redact_obj(response)

    draft = llm.complete(text, tool_results, role)
    body = redact_text(draft["text"])
    tokens = int(draft["tokens"])
    cost = float(draft["cost"])
    response = _base(
        status="ok",
        user_id=user_id,
        role=role,
        session_id=session_id,
        text=body,
        tools_exposed=exposed,
        l1_called=True,
        tokens=tokens,
        cost=cost,
    )
    response["tool_results"] = tool_results
    session.store(
        session_id,
        member_id=member_id,
        role=role,
        prompt=text,
        response=response,
        status="ok",
    )
    metrics.record("ok", l1_called=True, tokens=tokens, cost=cost)
    return redact_obj(response)


def _base(
    *,
    status: str,
    user_id: str | None,
    role: str | None,
    session_id: str | None,
    text: str,
    tools_exposed: list[str],
    l1_called: bool,
    tokens: int,
    cost: float,
) -> dict[str, Any]:
    return {
        "status": status,
        "text": text,
        "user": user_id,
        "role": role,
        "session_id": session_id,
        "tools_exposed": tools_exposed,
        "l1_called": l1_called,
        "tokens": tokens,
        "cost": cost,
    }
