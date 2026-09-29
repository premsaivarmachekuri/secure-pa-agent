---
name: redact-fixtures
description: Implement S4-shaped redact and synthetic fixtures. Use when adding member fixtures, SSN stripping on egress, or Session-store sanitization.
when-to-use: redact SSN fixture M-48219 M-10002 ALLOW_PHI minimum necessary
paths: data/**, agent/**/*redact*
---

# Redact and fixtures

BR-S5–S6, S4/S5: `context.md` §6, §9. Tool return shape (no SSN in eligibility): `l3-tools-rbac`.

## Own

`data/` synthetic members and a single redact helper used on egress **and** L2 writes.

## Do

1. Fixtures: `M-48219` active + PA required; `M-10002` `active=false`. Fixture **file** may include an SSN-shaped field; tool egress must not.
2. Strip SSN-shaped and secret-shaped strings on response and Session persist.
3. `ALLOW_PHI=false`. No real PHI.
4. Do not implement RBAC here. Do not implement injection here.
