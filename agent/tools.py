"""L3 Tools — role allowlist + fixture lookups. Not AI."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Any

from agent.config import CASEWORKER_TOOLS, DATA_DIR, REVIEWER_EXTRA
from agent.redact import redact_obj

MEMBER_RE = re.compile(r"\bM-\d+\b")
CPT_RE = re.compile(r"\b\d{5}\b")
DX_RE = re.compile(r"\bM\d{2}\.\d\b")


def _load(name: str) -> dict[str, Any]:
    path = DATA_DIR / name
    return json.loads(Path(path).read_text(encoding="utf-8"))


def tools_for(role: str) -> list[str]:
    names = list(CASEWORKER_TOOLS)
    if role == "clinician_reviewer":
        names.extend(REVIEWER_EXTRA)
    return names


def parse_refs(prompt: str) -> dict[str, str | None]:
    member = MEMBER_RE.search(prompt)
    cpt = CPT_RE.search(prompt)
    dx = DX_RE.search(prompt)
    return {
        "member_id": member.group(0) if member else None,
        "cpt": cpt.group(0) if cpt else None,
        "diagnosis": dx.group(0) if dx else None,
    }


def eligibility_min(member_id: str | None) -> dict[str, Any]:
    members = _load("members.json")
    if not member_id or member_id not in members:
        return {"member_id": member_id, "active": False, "plan": None, "pa_required": False}
    row = members[member_id]
    return {
        "member_id": row["member_id"],
        "active": bool(row["active"]),
        "plan": row.get("plan"),
        "pa_required": bool(row.get("pa_required")),
    }


def policy_lookup(cpt: str | None) -> dict[str, Any]:
    policies = _load("policy.json")
    if not cpt or cpt not in policies:
        return {"cpt": cpt, "pa_required": False, "criteria": None}
    row = policies[cpt]
    return {
        "cpt": row["cpt"],
        "pa_required": bool(row.get("pa_required")),
        "criteria": row.get("criteria"),
        "diagnosis": row.get("diagnosis"),
    }


def chart_snippet(member_id: str | None) -> dict[str, Any]:
    members = _load("members.json")
    row = members.get(member_id or "", {})
    return redact_obj(
        {
            "member_id": member_id,
            "note": "Synthetic lumbar imaging note; min necessary only",
            "ssn": row.get("ssn"),
        }
    )


def pa_submit_stub() -> dict[str, Any]:
    return {"auth_request_id": f"stub-{uuid.uuid4().hex[:12]}", "portal": "stub"}


def run_tools(role: str, prompt: str) -> tuple[list[str], dict[str, Any]]:
    exposed = tools_for(role)
    refs = parse_refs(prompt)
    results: dict[str, Any] = {"refs": refs}
    if "eligibility_min" in exposed:
        results["eligibility_min"] = eligibility_min(refs["member_id"])
    if "policy_lookup" in exposed:
        results["policy_lookup"] = policy_lookup(refs["cpt"])
    if "chart_snippet" in exposed:
        results["chart_snippet"] = chart_snippet(refs["member_id"])
    if "pa_submit" in exposed and re.search(r"\bsubmit\b", prompt, re.I):
        results["pa_submit"] = pa_submit_stub()
    return exposed, redact_obj(results)
