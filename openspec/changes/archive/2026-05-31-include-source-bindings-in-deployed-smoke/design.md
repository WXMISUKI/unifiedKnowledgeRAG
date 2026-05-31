## Context

The provider now exposes source binding review as a formal capability through `GET /api/provider/source-bindings`. Local handoff evidence includes source binding summary, but deployed smoke only verifies health, manifest, preflight, and handoff. A deployed component can therefore appear smoke-ready even if the live binding review endpoint is blocked by routing, access guard, or serialization issues.

## Goals / Non-Goals

**Goals:**

- Add a read-only source binding summary HTTP check to deployed smoke.
- Reuse existing optional provider API key headers for the protected `/api/*` endpoint.
- Report source binding status, source count, and bindable source count in the check details.
- Fail closed when the endpoint is unreachable, non-JSON, non-200, or has an invalid/blocked status.

**Non-Goals:**

- Do not execute RAG retrieval, answer composition, ingestion, index rebuilds, embeddings, Qdrant, or GraphRAG.
- Do not create source-to-agent bindings or implement approval/audit policy.
- Do not make local handoff generation require a deployed URL.
- Do not add new deployment infrastructure, health orchestration, metrics, or monitoring.

## Decisions

- Treat source binding smoke status like handoff status: `ready` and `review` pass, while `blocked` or invalid values fail.
  - Rationale: a deployed provider may have reviewable binding evidence and still be useful for external review, but blocked evidence should prevent binding confidence.
- Include only aggregate details in deployed smoke.
  - Rationale: detailed per-source diagnostics remain in the source binding endpoint and local evidence export.
- Keep the source binding check in the same request sequence as other protected API checks.
  - Rationale: this verifies access guard compatibility using the same provider API key behavior.

## Risks / Trade-offs

- More deployed smoke checks can make failures more visible. Mitigation: this is intentional for a promoted binding capability, and the check is still read-only.
- Source binding may be `review` in legitimate deployments. Mitigation: `review` keeps the smoke report reviewable rather than blocked.
- The smoke report duplicates a small source binding summary. Mitigation: only counts and status are included.
