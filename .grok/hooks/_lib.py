"""Shared patterns for builder PreToolUse hooks. Runtime L4 is not this file."""

from __future__ import annotations

import json
import re
import sys

SECRET_PATH = re.compile(
    r"(?:^|[\\/])\.env(?:$|[\\/])|\.pem$|\.key$|id_rsa|GROQ_API_KEY\s*=\s*\S+",
    re.I,
)
LIVE_PAYER = re.compile(
    r"availity|uhc\.com|unitedhealthcare|uhcprovider|evicore|highmark",
    re.I,
)


def event() -> dict:
    raw = sys.stdin.read() or "{}"
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def deny(reason: str) -> None:
    json.dump({"decision": "deny", "reason": reason}, sys.stdout)
    sys.exit(2)


def allow() -> None:
    sys.exit(0)


def blob(data: dict) -> str:
    tool = data.get("toolInput") or data.get("tool_input") or {}
    if isinstance(tool, str):
        return tool
    return json.dumps(tool, default=str)
