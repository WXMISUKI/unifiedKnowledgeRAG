## Context

The provider-side access gate has already been simplified and closed:

- Phase 18 narrowed the primitive access gate.
- Phase 24 returned `decision=go` for MyPrivateAgent document RAG repo-side trial readiness.
- The next useful signal is the actual caller-side trial outcome, not more readiness preparation.

The Phase 25 report should therefore be an input-driven closure artifact. It reads an explicit MyPrivateAgent live trial outcome JSON path and answers whether the provider needs action.

## Goals / Non-Goals

**Goals:**
- Read a caller-provided MyPrivateAgent live trial outcome JSON file.
- Classify the provider feedback state as `ready`, `review`, or `blocked`.
- Emit provider action as `no_provider_action_required`, `provider_review_required`, or `provider_blocked`.
- Preserve compact evidence facts for reviewer traceability.
- Export JSON and Markdown artifacts.

**Non-Goals:**
- Do not run MyPrivateAgent code.
- Do not call provider HTTP endpoints.
- Do not create source-to-agent bindings.
- Do not promote retrieval backends, embedding models, hybrid behavior, reranking, or GraphRAG execution.
- Do not mutate source documents, indexes, audit logs, or runtime defaults.

## Decisions

- Require an explicit `--trial-outcome-path`.
  - Rationale: avoids hidden cross-repository scanning and makes the caller evidence source auditable.
  - Alternative considered: automatically read from `D:\AI\AIcode\MyPrivateAgent`. Rejected because provider should not assume caller repository layout.

- Treat caller `go` plus provider retrieve `ready` as provider closure.
  - Rationale: if MyPrivateAgent can retrieve answerable evidence and downstream grounded-answer composition is ready, the provider has no follow-up action in this slice.
  - Alternative considered: re-run provider smoke as part of Phase 25. Rejected because Phase 25 is feedback closure, not another readiness workflow.

- Classify provider retrieve failure as `blocked`.
  - Rationale: a live trial blocked by provider HTTP/retrieve failure is actionable in this repository.

- Classify insufficient evidence or citation/evidence-pack review states as `review`.
  - Rationale: these may be corpus/query quality issues or provider evidence packaging issues; they need human review before declaring a provider bug.

## Risks / Trade-offs

- The outcome file schema is owned by MyPrivateAgent and may evolve. The parser will be tolerant and fail closed when key fields are missing.
- A `review` result can include caller-side policy issues. The report will keep provider action wording conservative and include boundary notes.
- This phase records feedback but does not repair provider bugs. Concrete fixes should be separate focused changes only after this report identifies a provider-owned issue.
