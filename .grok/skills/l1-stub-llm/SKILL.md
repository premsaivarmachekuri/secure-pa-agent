---
name: l1-stub-llm
description: Implement L1 Groq-or-stub recommend-only interface. Use when changing stub tokens/cost, GROQ_API_KEY-empty path, or recommendation text.
when-to-use: stub L1 Groq tokens cost recommend needs_docs refer_reviewer GROQ_API_KEY
paths: agent/**/*llm*, agent/**/*l1*, tests/**/*stub*
---

# L1 stub LLM

BR-O3, UC-4, NFR-2/NFR-5: `context.md` §9–11. Recommend-only language: `AGENTS.md`.

## Own

The only generative call. Same interface with or without `GROQ_API_KEY`.

## Do

1. Run only if L4 passed. Empty key → stub, still tokens > 0 and cost > 0.
2. Text is `recommend` | `needs_docs` | `refer_reviewer` (language: `AGENTS.md`).
3. Do not invent coverage (`M-10002` inactive is fixture-driven via L3).
4. Do not implement gates, tools, or Session store here.
