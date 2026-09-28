# context.md — Secure Prior Authorization Agent

| Field | Value |
|---|---|
| Document | CONTEXT-PA-AGENT-001 |
| Source | BRD-PA-AGENT-001 v1.1 (2026-09-27) |
| Status | Approved for Phase 1 build |
| Precedence | this file > BRD > agent.md > HLD for naming |
| Code entry | `agent/orchestrator.py` |
| Build | Zed + Grok Build |

This file is **project product context**. The BRD states what the business needs. Do not rename canonical entities.

---

## 1. Product

Gated Secure Agent for prior authorization (PA) evaluation.

- Cuts coordinator time on **routine evaluation**
- Is **not** the Payer
- Must not create a new PHI leak
- Groq/stub speaks **only after** L4 → L3 → L2
- Recommend only; never approve / deny / book MRI

## 2. Problem

AHN-class IDN imaging PA: ~40 requests/physician/week; ~200k auths/year.

Today a PA coordinator checks eligibility, copies EHR packets, submits in Highmark Availity / UHC Provider Portal, and chases status. Scheduler will not book MRI without a Payer auth number.

Ungoverned LLMs can leak PHI, escalate via injection, or submit without a licensed Clinician reviewer.

## 3. Phase 1 objectives

| ID | Outcome |
|---|---|
| BO-1 | One Session turn on synthetic `M-48219` → recommend / needs_docs / refer_reviewer |
| BO-2 | Injection → `blocked`; model not called |
| BO-3 | Maker-checker: `caseworker` cannot submit; only `clinician_reviewer` sees `pa_submit` |
| BO-4 | Eligibility tool returns plan + pa_required, never SSN or full claims |
| BO-5 | Every turn: user, role, Session, status, tools_exposed, `l1_called` |
| BO-6 | Stub L1 works without vendor key; tokens/cost still non-zero |

## 4. Entity catalog (do not rename)

| Entity | Type | Job |
|---|---|---|
| Patient | Person | Member `M-48219`. Does not call the agent. |
| Physician | Person | Places lumbar MRI order (CPT `72148`, diagnosis `M54.5`). |
| PA coordinator | Person | Role `caseworker`. Maker. Cannot submit. |
| Clinician reviewer | Person | Role `clinician_reviewer`. Checker. Only role that may `pa_submit`. |
| Scheduler | Person | Books MRI only after Payer auth number. |
| AHN | Organization | Owns EHR, Secure Agent, audit. |
| Payer | Organization | Highmark or UnitedHealthcare. Pays / pends / denies. |
| UM nurse | Person | Payer reviewer. Unchanged. |
| EHR | System | Phase 1 not connected; order assumed done. |
| Payer portal | System | Availity / UHC. Live submit is Phase 4/5. |
| Secure Agent | System | This product. L4→L3→L2→L1 + verify + trace. |
| Session | Record | One Patient, one case. e.g. `pa-2026-09-27-001`. |

Roles in code: `caseworker`, `clinician_reviewer`, `admin`.

## 5. Operating model

Every turn:

```
prompt + SecurityContext
  → L4 Security (NOT AI): identity, sanitize, injection, RBAC, rate
       fail → blocked | rejected  STOP
  → L3 Tools (NOT AI): allowlist; eligibility_min / policy_lookup; redact SSN/secrets
  → L2 Memory (NOT AI): session_id, max_turns=6, one Patient
  → L1 LLM (GEN AI only here): Groq or stub — recommend only
  → verify + trace + metrics
  → AgentResponse  ok | blocked | rejected
```

Payer still decides. Scheduler still books. Patient never uses the product.

## 6. Scenarios (Phase 1 must demo)

Must demonstrate: **S1, S2, S4-shaped redact, S10-shaped reject, stub S6 visibility**.

| ID | Rule |
|---|---|
| S1 | Happy lumbar MRI `M-48219` CPT `72148` → `ok` + recommend or needs_docs. No submit. |
| S2 | Ignore-rules / dump tools / submit / print SSN → L4 `blocked`. L1 and portal never called. |
| S3 | Coordinator asks to submit → `pa_submit` omitted. Status may be `ok`. No packet. |
| S4 | Fixture may contain SSN; egress and Session store strip it. |
| S5 | `M-10002` `active=false` → needs_docs / stop. Model must not invent coverage. |
| S6 | Clinician reviewer: `pa_submit` visible. Stub returns `auth_request_id`. |
| S7 | Pend then resume **same Session**. L2 bounded history. L4 every turn. |
| S8 | Denial: no auto-appeal / auto-deny. Peer-to-peer outside L1. |
| S9 | No consumer ChatGPT path. No PHI without L4. |
| S10 | 21st request/minute or oversize prompt → `rejected`, L1 off. |

## 7. Scope

**In (Phase 1)**

- L4 → L3 → L2 → L1
- Tools: `eligibility_min`, `policy_lookup`; stub visibility for `chart_snippet`, `pa_submit`
- Fixtures: Patient `M-48219`, CPT `72148`, diagnosis `M54.5`
- SQLite Session + metrics
- FastAPI `POST /chat`, `GET /health`, `GET /metrics`
- Stub L1; optional Groq behind same interface
- Tests T1 (happy), T2 (injection blocked), T8 (stub tokens)

**Out**

- Live EHR, live Availity/UHC, real PHI
- Autonomous approve / deny / book
- Postgres, Redis, SSO, VPC, BAA
- Training an ML model
- Replacing UM nurse or Payer policy engine
- Phase 3–5 data centers or live Payer calls

## 8. Jobs to be done

- **JTBD-1 Coordinator:** first-pass recommendation from eligibility + policy; no paste into public chatbot.
- **JTBD-2 Reviewer:** only role that can submit; Session trail of what was recommended.
- **JTBD-3 Privacy:** “ignore rules / dump SSN / submit” stopped before model or portal.

## 9. Business requirements (implement these)

**Process:** BR-P1–P3 (Session = one Patient/one case; recommend only; checker submit). BR-P4–P5 are process rules (Scheduler/Payer outside Phase 1 app).

**Security:** BR-S1–S7

- Gate untrusted input before any model call
- Injection = authorization failure (`blocked`)
- Oversize / missing Session / rate limit → `rejected`
- Role drives tool visibility; coordinator never gets `pa_submit`
- SSN/secret-shaped strings stripped on egress and in Session store
- `ALLOW_PHI=false`; no real PHI
- Secrets never committed (`.env` gitignored)

**Data:** BR-D1–D3 — eligibility/PA-required from fixtures/tools, not the model; `max_turns=6`; SQLite (JSON → SQLite → Postgres path).

**Observability:** BR-O1–O3 — status only `ok` | `blocked` | `rejected`; metrics: outcome, tokens, cost, `l1_called`; stub still non-zero tokens/cost.

## 10. Functional use cases

**UC-1 Happy path** — `caseworker` evaluates `M-48219`, CPT `72148`, M54.5.  
Result: `ok`; tools = `eligibility_min`, `policy_lookup`; text = recommend / needs_docs / refer_reviewer; L1 may run (stub).

**UC-2 Injection** — ignore instructions, list tools, submit, print SSN.  
Result: `blocked`; `l1_called=false`; no submit.

**UC-3 Role fence** — coordinator “submit the PA.”  
Result: `pa_submit` not in `tools_exposed`.

**UC-4 Stub offline** — no `GROQ_API_KEY`.  
Same contracts as live L1; tokens > 0; cost > 0.

Implement **only** BR-P1–P3, BR-S1–S7, BR-D1–D3, BR-O1–O3, UC-1/2/4.

## 11. Non-functional

| ID | Need |
|---|---|
| NFR-1 | Single Docker/Python service from Zed on port 8000 |
| NFR-2 | CI/local tests with empty Groq key |
| NFR-3 | One worker (`uvicorn --workers 1`) |
| NFR-4 | L4/L3/L2 path feels instant on laptop |
| NFR-5 | English, operational API/UI; never “I approved the MRI” |

Identity in Phase 1: headers `X-User-Id`, `X-Role`, `X-Session-Id`.

Stack: Python 3.12, FastAPI, fixtures in `data/`.

## 12. Assumptions and dependencies

- EHR order already exists; this app does not place orders.
- Synthetic `M-48219` is enough to prove the control plane.
- Groq optional; stub acceptable for Phase 1 demo.
- Later: BAA if Groq sees PHI; SSO; Payer/EHR adapters (Phases 4–5).

## 13. Risks (do not violate mitigations)

| Risk | Mitigation |
|---|---|
| Agent treated as the Payer | Recommend only |
| PHI paste to Groq | Synthetic data; `ALLOW_PHI=false` |
| Coordinator submits via prompt | Tool hidden by **role**, not by prompt |
| Incomplete injection regex | Fail closed + tool allowlist + no submit for caseworker |
| “HIPAA compliant” sticker | Architecture + audit; **no certification claim** |

## 14. Phase 1 sign-off

- UC-1, UC-2, UC-4 pass in pytest and once via `POST /chat`
- Coordinator path cannot list `pa_submit`
- No `.env` or API key in git
- This file §15 updated to “Phase 1 complete”

## 15. Implementation status

**Phase 1 in progress** — kernel not signed off.

When signed off, change this line to: **Phase 1 complete.**
