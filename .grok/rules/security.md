# Builder security (delta)

Runtime L4/L3/S requirements live in `context.md` §9 (BR-S1–S7). Implement those in Python under `agent/`. Do not replace runtime L4 with a Grok hook.

**Builder fail-closed (this harness)**

- `PreToolUse` hooks in `.grok/hooks/` block `.env` writes and live-Payer curls
- `[permission]` deny in `.grok/config.toml` wins over allow / always-approve
- Sandbox deny globs in `.grok/sandbox.toml`

**Memory**

- Product Session history is SQLite L2, redacted, `max_turns = 6`
- Grok `/remember` stays off. Never store PHI, member charts, or keys in `~/.grok/`

Trust project hooks once with `/hooks-trust` (stored locally, not in git).
