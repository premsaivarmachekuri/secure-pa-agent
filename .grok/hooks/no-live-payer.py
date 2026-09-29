#!/usr/bin/env python3
"""Deny builder shell calls toward live Payer / EHR hosts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIVE_PAYER, allow, blob, deny, event  # noqa: E402

if LIVE_PAYER.search(blob(event())):
    deny("Live EHR/Payer calls are out of Phase 1; use fixtures in data/")
allow()
