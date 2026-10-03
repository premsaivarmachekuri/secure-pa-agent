"""Strip SSN-shaped and secret-shaped strings on egress and L2 writes."""

from __future__ import annotations

import json
import re
from typing import Any

SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
SECRET = re.compile(
    r"(?:GROQ_API_KEY|API_KEY|Bearer)\s*[=:]\s*\S+|"
    r"-----BEGIN [A-Z ]+PRIVATE KEY-----",
    re.I,
)


def redact_text(value: str) -> str:
    value = SSN.sub("[REDACTED]", value)
    value = SECRET.sub("[REDACTED]", value)
    return value


def redact_obj(value: Any) -> Any:
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            if str(key).lower() in {"ssn", "social_security", "secret", "api_key"}:
                out[key] = "[REDACTED]"
            else:
                out[key] = redact_obj(item)
        return out
    if isinstance(value, list):
        return [redact_obj(item) for item in value]
    return value


def redact_jsonable(value: Any) -> str:
    return redact_text(json.dumps(redact_obj(value), default=str))
