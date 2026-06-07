## Context

The provider already exposes the required local HTTP endpoints:

- `GET /api/rag/sources`
- `GET /api/rag/sources/{source_id}/documents`
- `POST /api/rag/retrieve`
- `POST /api/rag/answer`

The previous approved local corpus acceptance smoke exercises the same behavior in-process through `TestClient`. This change adds the missing caller-shaped path: an already running local provider is called through HTTP, using the same default source and business cases.

## Goals / Non-Goals

**Goals:**

- Produce a deterministic `go` / `review` / `blocked` live HTTP report for `company_profile_2025_trial`.
- Reuse the acceptance smoke case semantics where practical.
- Keep the implementation thin and testable without requiring a real service in unit tests.
- Make real-service verification easy after the user starts `uvicorn` on port `8020`.

**Non-Goals:**

- Do not start or manage the FastAPI server.
- Do not register sources or create source-to-agent bindings.
- Do not run MyPrivateAgent orchestration or modify MyPrivateAgent.
- Do not promote Qdrant, BGE, hybrid retrieval, rerankers, or answer composers.
- Do not start OCR services, parse raw PDFs, call vector databases, or execute GraphRAG.

## Decisions

1. **Use an explicit HTTP client adapter instead of changing RAG routes.**
   - Rationale: the public API contract is already sufficient; the gap is live consumption evidence.
   - Alternative considered: add new provider endpoints. Rejected because it would expand runtime surface for a smoke-only need.

2. **Keep in-process and live HTTP reports separate.**
   - Rationale: the existing acceptance smoke remains fast and serverless, while the live smoke records network reachability and caller-shaped behavior.
   - Alternative considered: overload the existing script with a `--base-url`. Rejected to keep output paths and operational meaning clear.

3. **Use mockable HTTP transport in tests and real HTTP only for final verification.**
   - Rationale: focused tests should not depend on a developer service process; the live export command can still be run against `http://127.0.0.1:8020`.

## Risks / Trade-offs

- Service not running or wrong port -> report `blocked` with a connection reason instead of hiding the failure.
- API key guard enabled -> support optional provider API key header while keeping secret values out of reports.
- Retrieval quality drift -> report `review` when answerable or negative-control cases no longer meet expectations.
