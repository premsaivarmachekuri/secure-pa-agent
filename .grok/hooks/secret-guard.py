#!/usr/bin/env python3
"""Deny writes of .env, keys, and inline API secrets."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import SECRET_PATH, allow, blob, deny, event  # noqa: E402

data = event()
text = blob(data)
path = str(
    (data.get("toolInput") or data.get("tool_input") or {}).get("path", "")
    if isinstance(data.get("toolInput") or data.get("tool_input"), dict)
    else ""
)
if SECRET_PATH.search(path) or SECRET_PATH.search(text):
    deny("Secrets must not be written; use .env.example only")
allow()
