#!/usr/bin/env python3
"""Remind T1/T2/T8 after product-code edits. Not a test runner."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import allow, event  # noqa: E402

data = event()
tool = data.get("toolInput") or data.get("tool_input") or {}
path = str(tool.get("path", "") if isinstance(tool, dict) else tool)
if "agent/" in path.replace("\\", "/") or path.replace("\\", "/").startswith("agent"):
    print("After agent/ edits, run skill phase1-tests (T1 T2 T8).")
allow()
