## Context

Future hosted or local answer composers will need to turn the user query and retrieved evidence into a model prompt. If every adapter builds prompts independently, citation rules and evidence formatting will drift. The deterministic composer already has the evidence and citations it needs, so this change introduces a small prompt package boundary now while behavior is still easy to validate.

## Goals / Non-Goals

**Goals:**
- Build a cited-answer prompt package from query plus gated evidence.
- Include stable prompt package metadata in answered responses.
- Keep prompt rules provider-owned and model-provider-neutral.
- Preserve current deterministic answer output and endpoint contract.

**Non-Goals:**
- Call any LLM.
- Expose full prompt messages as a public API contract.
- Add streaming, prompt template rendering engines, or model-specific system prompts.
- Solve multi-hop reasoning or reranking.

## Decisions

1. Keep the full prompt package internal and expose only summary metadata.

   Rationale: callers need auditability, not the full prompt surface. Future model adapters can consume the full package internally without locking the public API to exact prompt wording.

2. Include allowed citations in metadata.

   Rationale: citation constraints are central to RAG answer safety and useful for tests, audits, and later LLM adapter validation.

3. Pass the query into `AnswerComposer.compose`.

   Rationale: LLM composers need the query to build prompts. Adding it now avoids another interface churn when hosted/local composers are implemented.

## Risks / Trade-offs

- Metadata grows slightly -> The added prompt package summary is compact and only appears on answered results.
- Prompt wording may evolve later -> The public contract uses prompt package id and policy metadata, not exact prompt text.
