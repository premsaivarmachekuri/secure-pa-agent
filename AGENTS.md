# Builder rules — Secure PA Agent

Grok Build / Zed coding agent only. Coordinators never see this file.

**Canonical sources (do not copy into skills or other rules):**

| What | File |
|---|---|
| Product facts, entities, requirements, UCs | `context.md` |
| Business narrative | `docs/BRD.md` |
| Harness map (skills, hooks, agents) | `docs/GROK_HARNESS.md` |
| Scope delta | `.grok/rules/phase1-scope.md` |
| Naming delta | `.grok/rules/naming.md` |
| Builder security delta | `.grok/rules/security.md` |

## Non-negotiables

1. Recommend only. Never approve / deny / book MRI. Never write “I approved the MRI”.
2. Implement only BR-P1–P3, BR-S1–S7, BR-D1–D3, BR-O1–O3, UC-1/2/4 in `context.md` §9–10.
3. Code entry: `agent/orchestrator.py`. Every turn: L4 → L3 → L2 → L1.
4. `caseworker` tools: `eligibility_min`, `policy_lookup`. `pa_submit` is role-gated, not prompt-gated.
5. Eligibility and PA-required come from fixtures/tools, never from L1.
6. Status is only `ok` | `blocked` | `rejected`. Stub L1 still emits tokens > 0 and cost > 0.
7. No live EHR, Availity, UHC, or real PHI. `ALLOW_PHI=false`. Never commit `.env` or keys.
8. Stack: Python 3.12, FastAPI, SQLite, port 8000, `uvicorn --workers 1`.
9. Tests: T1 happy, T2 injection blocked, T8 stub tokens (`context.md` §10).
10. Do not duplicate this file, `context.md`, or the BRD into skills. Point; do not paste.

Harness files live under `.grok/`. Product code lives under `agent/`, `data/`, `tests/`. Do not mirror skills into `.agents/skills/`.

This repo is an FDE portfolio artifact: named controls, reviewable diffs, and pytest/hook evidence over slides.
