## Context

`unifiedKnowledgeRAG` is an external knowledge provider component. It is expected to run locally for public-network testing and later inside private-network enterprise deployments. The project already exports contract smoke and integration probe evidence, but operators still need one consolidated readiness report before binding or deployment.

## Goals / Non-Goals

**Goals:**
- Provide a local deployment readiness report with health, preflight, smoke, configuration, model artifact, and operation notes.
- Keep the report executable without a running external server by using the in-process FastAPI test client and existing services.
- Make readiness status conservative and machine-readable.

**Non-Goals:**
- Do not add an HTTP endpoint.
- Do not start Qdrant, download models, rebuild indexes, or run ingestion.
- Do not select production infrastructure or promote Qdrant/BGE-M3/hybrid behavior.

## Decisions

1. Export a local report rather than adding a new API.
   - Rationale: deployment readiness is an operator artifact, not a runtime capability callers need on every request.

2. Use existing service truth sources.
   - Health comes from `build_health_response`.
   - Binding readiness comes from `build_provider_preflight_response`.
   - Contract behavior comes from `run_provider_contract_smoke`.
   - Configuration comes from `Settings`.

3. Treat local model artifact checks as diagnostic.
   - If `EMBEDDING_MODEL_PATH` is configured, report whether the path and `model-manifest.json` exist.
   - If it is not configured, report `not_configured` rather than failing the default mock setup.

4. Keep status simple.
   - `ready` only when health, preflight, and smoke pass.
   - `review` when core checks pass but there are deployment notes to review.
   - `blocked` when health, preflight, or smoke fails.

## Risks / Trade-offs

- A single report can become a dumping ground -> Limit it to deployment readiness facts and notes, not benchmark details.
- Model artifact checks can be environment-specific -> Keep them diagnostic and path-based.
- Generated timestamps change reports -> Accept this for operator evidence, similar to smoke reports.
