# Naming (builder delta)

Canonical catalog is `context.md` §4. Do not invent aliases or rename entities.

Code identifiers (use these strings exactly):

- Roles: `caseworker`, `clinician_reviewer`, `admin`
- Tools: `eligibility_min`, `policy_lookup`, `chart_snippet`, `pa_submit`
- Status: `ok`, `blocked`, `rejected`
- Fixtures: member `M-48219`, CPT `72148`, diagnosis `M54.5`, inactive `M-10002`
- Headers: `X-User-Id`, `X-Role`, `X-Session-Id`

Do not name Grok subagents `caseworker` or `clinician_reviewer`. Those are product roles.
