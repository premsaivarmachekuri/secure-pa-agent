"""One-off sanity check for builder hooks. Not a product test."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(script: str, payload: dict) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / script)],
        input=json.dumps(payload).encode(),
        capture_output=True,
    )
    return proc.returncode, proc.stdout.decode().strip()


ok_edit = {"toolInput": {"path": "agent/orchestrator.py", "content": "x"}}
env_edit = {"toolInput": {"path": ".env", "content": "GROQ_API_KEY=secret"}}
payer = {"toolInput": "curl https://api.availity.com"}
harness_edit = {"toolInput": {"path": ".grok/config.toml"}}

checks = [
    ("secret-guard.py", ok_edit, 0, False),
    ("secret-guard.py", env_edit, 2, True),
    ("no-live-payer.py", ok_edit, 0, False),
    ("no-live-payer.py", payer, 2, True),
    ("pytest-after-edit.py", ok_edit, 0, True),
    ("pytest-after-edit.py", harness_edit, 0, False),
]

failed = 0
for script, payload, expect_code, expect_stdout in checks:
    code, out = run(script, payload)
    has_out = bool(out)
    good = code == expect_code and has_out == expect_stdout
    if not good:
        failed += 1
        print("FAIL", script, "code", code, "out", out)
    else:
        print("PASS", script, expect_code)

sys.exit(1 if failed else 0)
