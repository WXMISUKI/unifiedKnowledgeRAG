## Context

`/api/rag/answer` is now the provider-owned cited answer endpoint. It currently composes answers through a deterministic function, which is appropriate for contract testing but too tightly coupled for the next phase. The project needs a boundary where hosted chat models, local LLMs, or future graph-aware composers can be added without changing the endpoint contract.

This change introduces the boundary only. It intentionally does not choose Qwen, OpenAI, vLLM, Ollama, or another production model.

## Goals / Non-Goals

**Goals:**
- Add an answer composer interface with a deterministic default implementation.
- Select the composer through configuration.
- Fail closed for unsupported hosted/local composers.
- Preserve existing answer endpoint behavior for the default path.
- Record composer provider and model metadata in the answer envelope.

**Non-Goals:**
- Implement a hosted Qwen/OpenAI adapter.
- Implement a local LLM runtime adapter.
- Add streaming, prompt templates, conversation memory, or tool planning.
- Change retrieval, evidence gating, or citation semantics.

## Decisions

1. Keep deterministic composer as default.

   Rationale: tests and local usage must remain offline, repeatable, and free of API keys. This also keeps the endpoint usable while provider choices are discussed.

   Alternative considered: make `hosted` the default. Rejected because data egress and paid model selection are still open decisions.

2. Add fail-closed hosted/local placeholders.

   Rationale: operators can see the intended configuration surface, but accidental use returns a structured provider error rather than silently falling back or calling an unapproved model.

   Alternative considered: silently fall back to deterministic. Rejected because it hides misconfiguration and makes answer provenance unclear.

3. Return provider errors when the configured composer is unavailable.

   Rationale: composer unavailability is a system/configuration failure, different from insufficient evidence. Insufficient evidence remains a successful answer envelope with `answer_status=insufficient_evidence`.

## Risks / Trade-offs

- This adds another adapter layer before any LLM integration -> The layer is intentionally small and prevents model-specific decisions from leaking into the HTTP contract.
- Hosted/local settings may look usable before adapters exist -> Fail-closed errors and README notes make the boundary explicit.
- Future LLM composer may need richer prompt metadata -> The composer interface can be extended in a later change once the model/provider decision is approved.
