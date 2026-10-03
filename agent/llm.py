"""L1 — Groq or stub, recommend only. Generative AI lives here only."""

from __future__ import annotations

from typing import Any

from agent.config import STUB_COST, STUB_TOKENS, groq_api_key


def complete(prompt: str, tool_results: dict[str, Any], role: str) -> dict[str, Any]:
    _ = groq_api_key()
    # Phase 1: stub path is the contract (UC-4). Live Groq stays behind this function.
    text = _recommend(tool_results, role)
    return {"text": text, "tokens": STUB_TOKENS, "cost": STUB_COST, "stub": True}


def _recommend(tool_results: dict[str, Any], role: str) -> str:
    elig = tool_results.get("eligibility_min") or {}
    policy = tool_results.get("policy_lookup") or {}
    refs = tool_results.get("refs") or {}
    member = refs.get("member_id") or elig.get("member_id") or "unknown"

    if elig.get("active") is False:
        return (
            f"needs_docs: member {member} coverage is inactive. "
            "Stop. Do not invent coverage. Refer coordinator to update eligibility."
        )

    if elig.get("active") and (elig.get("pa_required") or policy.get("pa_required")):
        extra = ""
        if role == "caseworker":
            extra = " Submit is a clinician_reviewer step; pa_submit is not available to caseworker."
        elif role == "clinician_reviewer" and tool_results.get("pa_submit"):
            auth = tool_results["pa_submit"].get("auth_request_id")
            extra = f" Stub packet filed auth_request_id={auth}. Not a Payer decision."
        return (
            f"recommend: lumbar MRI {refs.get('cpt') or ''} {refs.get('diagnosis') or ''} "
            f"for {member} on {elig.get('plan')}. PA required per fixture policy. "
            f"Hand off Session to clinician_reviewer when the packet is complete.{extra}"
        ).strip()

    return (
        f"refer_reviewer: member {member} needs clinician_reviewer review. "
        "Recommend only; this is not an approval."
    )
