## Context

The project is currently used as a lightweight local provider for MyPrivateAgent. The user wants the service to be locally usable before thinking about deployment. Existing reports are useful but too broad for the day-1 local loop.

The new run-loop should answer one practical question:

> After I start `uvicorn` locally, can this provider be consumed for discovery, retrieval evidence, and a cited answer?

## Goals / Non-Goals

**Goals:**
- Validate an already-running local service over HTTP.
- Exercise operational probes, provider discovery, preflight, retrieval, and answer.
- Return a compact `go`, `review`, or `blocked` conclusion.
- Write JSON and Markdown artifacts for local troubleshooting.
- Keep the quickstart short and actionable.

**Non-Goals:**
- Do not start the server.
- Do not deploy containers or configure remote servers.
- Do not require `PROVIDER_API_KEY` for local default use.
- Do not change retrieval defaults or promote candidate backends.
- Do not download embedding models or start Qdrant/pgvector.
- Do not execute GraphRAG or create source-to-agent bindings.

## Decisions

- Use `httpx.Client` with optional mock transport support.
  - Rationale: matches existing deployed smoke tests and keeps local HTTP behavior realistic.

- Treat `/ready` HTTP 200 or 503 as an expected diagnostic response.
  - Rationale: `/ready` intentionally returns 503 when degraded. For the run-loop, degraded readiness is a review signal unless other checks fail.

- Require successful retrieve evidence for `go`.
  - Rationale: local usability means more than process health; it must return answerable evidence from the fixture source.

- Require answer citations to be within the retrieve citation allowlist for `go`.
  - Rationale: this verifies the minimum caller-safe answer contract without running MyPrivateAgent.

## Risks / Trade-offs

- If local settings are intentionally stricter than defaults, the report may be `review` or `blocked`. That is acceptable because this script is a local diagnostic.
- The script does not replace full handoff refresh or deployment smoke. It is narrower by design.
- The default query/source should remain fixture-friendly and should not imply production corpus quality.
