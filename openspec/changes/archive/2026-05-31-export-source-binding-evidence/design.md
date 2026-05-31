## Context

Handoff evidence already consolidates integration, contract, deployment, reindex, and optional deployed smoke artifacts. Source bindability is now available over HTTP, but not as a persisted evidence artifact. Since source-to-agent binding is a control-plane decision, the provider should not bind anything; it should provide evidence that can be regenerated and reviewed.

## Goals / Non-Goals

**Goals:**

- Export source binding summary evidence to JSON and Markdown.
- Include source binding evidence in default handoff bundle status.
- Refresh source binding evidence before regenerating the handoff bundle.
- Keep source binding evidence deterministic, local, and read-only.

**Non-Goals:**

- Do not create source-to-agent bindings.
- Do not create ingestion jobs or rebuild indexes.
- Do not execute retrieval, answer composition, embeddings, Qdrant, or GraphRAG.
- Do not make deployed smoke mandatory.

## Decisions

- Treat source binding evidence as required local handoff evidence.
  - Rationale: unlike deployed smoke, it does not require an external URL and is central to safe binding review.
  - Alternative considered: optional evidence; rejected because source bindability is a core handoff concern for this provider.
- Put evidence under `docs/integration/source-bindings/`.
  - Rationale: this is integration-facing binding evidence rather than operations-only readiness.
- Add the refresh step before `provider_handoff_bundle`.
  - Rationale: the bundle should summarize freshly generated source binding evidence.

## Risks / Trade-offs

- The handoff bundle may become blocked when source binding evidence detects drift or not-ready indexes. Mitigation: this is intentional fail-closed behavior before external binding.
- Reports duplicate some fields from live endpoints. Mitigation: the export is a handoff artifact; detailed diagnostics remain in the original APIs.
