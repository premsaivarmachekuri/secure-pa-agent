---
name: phase1-tests
description: Add or run Phase 1 tests T1 happy, T2 injection blocked, T8 stub tokens. Use when writing pytest or proving POST /chat contracts.
when-to-use: T1 T2 T8 pytest POST /chat l1_called tools_exposed
paths: tests/**/*.py
---

# Phase 1 tests

UC-1, UC-2, UC-4: `context.md` §10. Sign-off: `context.md` §14.

## Own

`tests/` only. Do not weaken assertions to make the kernel pass.

## Do

1. T1: `caseworker` evaluates `M-48219` CPT `72148` M54.5 → `ok`; `tools_exposed` = `eligibility_min`, `policy_lookup`; no `pa_submit`.
2. T2: injection prompt → `blocked`; `l1_called = false`.
3. T8: no `GROQ_API_KEY` → tokens > 0, cost > 0.
4. Run pytest; one manual `POST /chat` for T1 is sign-off, not a second test suite.
