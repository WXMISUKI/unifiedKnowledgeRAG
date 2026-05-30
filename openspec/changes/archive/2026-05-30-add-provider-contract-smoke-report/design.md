## Context

The provider already has stable HTTP contracts and focused tests for individual endpoints. The missing piece is an executable, repeatable evidence artifact that validates the provider as an integrated capability surface: health/readiness, capability invocation metadata, RAG retrieval, cited answer orchestration, and the planned GraphRAG boundary.

This smoke path should be usable on a developer laptop and later in CI without starting an external server. It must avoid infrastructure decisions and use the current default fixture backend unless the caller explicitly runs the provider with a different environment.

## Goals / Non-Goals

**Goals:**

- Provide a local smoke runner that uses the existing FastAPI app contract.
- Return machine-readable check results with enough details for integration troubleshooting.
- Export JSON and Markdown evidence files on demand.
- Keep the smoke path deterministic and dependency-free.

**Non-Goals:**

- Do not benchmark retrieval quality or choose embedding/vector database vendors.
- Do not add production monitoring, CI wiring, or remote health checks.
- Do not implement GraphRAG execution; graph query remains a planned structured boundary.
- Do not change public HTTP contracts.

## Decisions

- Implement the smoke runner as an application service, not only as a script.
  - Rationale: tests and CLI export can share one source of truth.
  - Alternative considered: a standalone script with duplicated assertions. Rejected because it would drift from tests.

- Use `fastapi.testclient.TestClient` against `create_app()`.
  - Rationale: it validates the real router contracts without requiring uvicorn, ports, or network access.
  - Alternative considered: shelling out to a live HTTP server. Rejected for local determinism and simpler CI adoption.

- Treat planned GraphRAG as a positive smoke check when it returns structured `GRAPH_NOT_IMPLEMENTED` details.
  - Rationale: this proves the boundary is explicit and machine-readable without pretending GraphRAG is implemented.

- Export both JSON and Markdown.
  - Rationale: JSON is suitable for automation, while Markdown is easier for local review and future handoff notes.

## Risks / Trade-offs

- [Risk] Smoke checks can become too broad and duplicate all endpoint tests. -> Keep the checks to contract integration essentials and assert summary fields rather than every endpoint detail.
- [Risk] Generated evidence files can become noisy if committed every run. -> The export script writes to a stable docs path only when explicitly run; tests exercise in-memory report generation.
- [Risk] Environment variables can make local smoke results non-deterministic. -> The default path remains fixture/deterministic; failures include endpoint and reason details for diagnosis.
