## Context

MyPrivateAgent owns source-to-agent binding decisions, but it needs provider-owned facts to make those decisions safely: source catalog status, index lifecycle status, file fingerprint drift, parser readiness, and recommended ingestion actions. Today those facts exist, but they are spread across multiple surfaces. The next useful slice is a small aggregate discovery endpoint, not a heavier control plane.

## Goals / Non-Goals

**Goals:**

- Provide one read-only summary of source bindability for all configured knowledge bases.
- Reuse existing catalog, source document manifest, ingestion preflight, and index lifecycle services.
- Return machine-readable status and recommended actions for external callers.
- Advertise the endpoint through the provider manifest.

**Non-Goals:**

- Do not create source-to-agent bindings.
- Do not create ingestion jobs, rebuild indexes, or mutate lifecycle state.
- Do not execute retrieval, answer composition, embeddings, Qdrant calls, or GraphRAG.
- Do not introduce ACL policy, tenant policy, approval workflow, or audit ownership.

## Decisions

- Implement a provider-owned aggregate endpoint at `GET /api/provider/source-bindings`.
  - Rationale: it belongs to provider discovery and binding review rather than source document content APIs.
  - Alternative considered: extend `/api/catalog`; rejected because catalog should stay compact and not include deeper preflight/drift diagnostics by default.
- Use `ready`, `review`, and `blocked` as summary statuses.
  - Rationale: this matches existing handoff and deployment evidence vocabulary.
  - Alternative considered: return only `bindable=true/false`; rejected because operators need to distinguish reviewable drift/metadata issues from hard blockers.
- Keep recommendation text deterministic and provider-neutral.
  - Rationale: the caller owns binding policy, but provider can recommend `bind_source_from_control_plane`, `run_ingestion_job_before_binding`, or `review_source_fingerprint_before_binding`.

## Risks / Trade-offs

- Aggregation may duplicate facts from other endpoints. Mitigation: only summarize stable fields and keep detailed diagnostics in the original endpoints.
- A source could be technically ready but still business-ineligible for a specific agent. Mitigation: operation notes explicitly state that external control planes own source-to-agent binding policy.
