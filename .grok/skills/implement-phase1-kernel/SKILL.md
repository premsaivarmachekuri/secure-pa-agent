---
name: implement-phase1-kernel
description: Scaffold the Phase 1 kernel layout and wire orchestrator L4→L3→L2→L1. Use when starting the product service, FastAPI routes, or agent/orchestrator.py.
when-to-use: Phase 1 kernel scaffold FastAPI POST /chat orchestrator
paths: agent/**/*.py, data/**, tests/**, requirements.txt
---

# Implement Phase 1 kernel

Requirements and UCs: `context.md` §7, §9–10. Do not paste them.

## Create (once)

- `agent/orchestrator.py` — single entry; call L4 then L3 then L2 then L1
- `agent/app.py` — FastAPI: `POST /chat`, `GET /health`, `GET /metrics`
- `data/` — synthetic fixtures only
- `tests/` — empty until `/phase1-tests`
- `requirements.txt` — Python 3.12, FastAPI, uvicorn

## Do

1. Load this skill, then the layer skills in order: `l4-security-gate` → `l3-tools-rbac` → `l2-session-memory` → `l1-stub-llm` → `redact-fixtures` → `phase1-tests`.
2. Do not implement a layer’s internals here; each layer skill owns its files.
3. Stop if the request is outside `.grok/rules/phase1-scope.md`.
