# Grok Build harness — Secure PA Agent

| Field | Value |
|---|---|
| Document | HARNESS-PA-AGENT-001 |
| Status | Scaffolded |
| Audience | Builder in Zed + Grok Build |
| Precedence | `context.md` > `docs/BRD.md` > this file > `AGENTS.md` |

How Grok Build implements the product. Coordinators never talk to `.grok/`.

Always-on rules: `AGENTS.md`. Do not copy them here.

---

## Two systems

| | Builder harness | Product runtime |
|---|---|---|
| Path | `.grok/` + `AGENTS.md` | `agent/`, `data/`, `tests/` |
| Who | FDE in Zed / Grok Build | PA coordinator / Clinician reviewer |
| Job | Write Python, pytest, keep Phase 1 in scope | Evaluate PA; recommend only |
| Memory | `~/.grok/sessions` (builder chat) | SQLite Session, `max_turns=6` |
| AI | Grok Build | L1 Groq/stub **after** L4→L3→L2 |

Do not mix: skills are implementation playbooks, not runtime tools; subagents are code workers, not `caseworker` / `clinician_reviewer`; hooks are not runtime L4; Grok `/remember` is not product Session.

---

## Tree (single copy)

```
AGENTS.md
.env.example
.grok/
  config.toml              # [permission] only
  sandbox.toml             # deny **/.env **/*.pem **/*.key
  rules/                   # deltas only → context.md
    naming.md
    phase1-scope.md
    security.md
  skills/                  # procedures; point at context.md
    implement-phase1-kernel/
    l4-security-gate/
    l3-tools-rbac/
    l2-session-memory/
    l1-stub-llm/
    phase1-tests/
    redact-fixtures/
  hooks/                   # shared patterns in _lib.py
    secret-guard.json/.py
    no-live-payer.json/.py
    pytest-after-edit.json
  agents/
    kernel-builder.md
    security-reviewer.md
    test-runner.md
  personas/fde.toml
```

No `.agents/skills/` mirror. No `.grok/workflows/` until the kernel exists. No `agent.md` until the runtime contract exists.

Verify: `grok inspect` then `/hooks-trust`.

---

## Primitive → files

| Primitive | Files | Owns |
|---|---|---|
| Rules | `AGENTS.md`, `.grok/rules/*` | Always-on + deltas |
| Skills | `.grok/skills/*/SKILL.md` | One layer or one test slice |
| Hooks | `.grok/hooks/_lib.py` + per-event | Builder deny of secrets and live Payer |
| Subagents | `.grok/agents/*.md` | Write kernel / read-only review / pytest |
| Persona | `.grok/personas/fde.toml` | Tone |
| Permissions | `.grok/config.toml` | Deny live-Payer curl |
| Sandbox | `.grok/sandbox.toml` | Deny secret paths |

Redaction of product SSN is a **runtime** skill (`redact-fixtures`), not a Grok hook.

---

## Session

1. `grok inspect`
2. `/plan` then `/implement-phase1-kernel`
3. Layer skills in skill order (listed inside that SKILL.md)
4. `/phase1-tests`
5. Subagent `security-reviewer` on the diff

Attach: `docs/BRD.md` + `context.md` + this file + `AGENTS.md`.

---

## Deferred

Product kernel (`agent/orchestrator.py`), workflows, Grok `[memory]`, MCP, user-config `[subagents] enabled`.
