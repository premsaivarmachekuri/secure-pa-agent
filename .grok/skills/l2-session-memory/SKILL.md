---
name: l2-session-memory
description: Implement product L2 SQLite Session store. Use when changing session_id, max_turns, one-Patient-one-case, or redacted turn persistence.
when-to-use: session SQLite max_turns L2 memory one Patient
paths: agent/**/*session*, agent/**/*memor*, tests/**/*session*
---

# L2 session memory

BR-P1, BR-D2–D3, S7: `context.md` §5, §9. Not Grok `/remember` or `~/.grok/sessions/`.

## Own

SQLite Session: one Patient, one PA case, `max_turns = 6`, redacted writes.

## Do

1. Key by product `session_id` from `X-Session-Id`.
2. Bound history at 6 turns. Same Session on follow-up (pend/resume).
3. Persist only after redact (`redact-fixtures`). Never store raw SSN.
4. Do not decide eligibility here (`l3-tools-rbac`). Do not call Groq here (`l1-stub-llm`).
