---
name: l4-security-gate
description: Implement runtime L4 identity, injection, RBAC context, rate and size gates. Use when changing blocked/rejected status, request headers, or l1_called=false paths.
when-to-use: injection blocked rejected rate limit X-User-Id X-Role X-Session-Id l1_called
paths: agent/**/*secur*, agent/**/*gate*, tests/**/*secur*
---

# L4 security gate

BR-S1–S3, UC-2, S2/S10: `context.md` §6, §9–10. Headers and status names: `.grok/rules/naming.md`.

## Own

Runtime Python under `agent/` that runs **before** tools, memory, and L1.

## Do

1. Require headers `X-User-Id`, `X-Role`, `X-Session-Id`. Missing Session → `rejected`, `l1_called=false`.
2. Injection / ignore-rules / dump-tools / print-SSN → `blocked`, `l1_called=false`. Do not call L1.
3. Oversize prompt or 21st request/minute → `rejected`, `l1_called=false`.
4. Do not implement tool allowlists here (`l3-tools-rbac`). Do not store turns here (`l2-session-memory`).
