---
name: l3-tools-rbac
description: Implement L3 tool allowlist and role visibility. Use when changing eligibility_min, policy_lookup, chart_snippet, or pa_submit exposure.
when-to-use: eligibility_min policy_lookup pa_submit tools_exposed caseworker clinician_reviewer RBAC
paths: agent/**/*tool*, data/**, tests/**/*tool*
---

# L3 tools and RBAC

BR-S4, BR-D1, UC-1/UC-3, S3/S6: `context.md` §6, §9–10. Tool and role strings: `.grok/rules/naming.md`.

## Own

Allowlist + role → `tools_exposed`. Fixtures in `data/` for plan + `pa_required` only (no SSN in tool return). Redaction of leftover SSN is `redact-fixtures`.

## Do

1. `caseworker`: `eligibility_min`, `policy_lookup` only. Never attach `pa_submit`.
2. `clinician_reviewer`: may add stub `chart_snippet` and `pa_submit` (`auth_request_id` stub, no live portal).
3. Eligibility / PA-required flags come from fixtures, not L1.
4. Do not implement injection detection here (`l4-security-gate`).
