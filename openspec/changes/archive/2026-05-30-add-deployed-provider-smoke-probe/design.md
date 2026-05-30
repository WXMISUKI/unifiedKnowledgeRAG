## Context

Local evidence currently validates the provider using FastAPI `TestClient`, which is useful before deployment but does not prove that a running component is reachable through its deployed HTTP base URL. Phase 6 now needs a lightweight external smoke probe that verifies the same binding-critical discovery surface after the provider has been started by Docker, compose, local uvicorn, or a network deployment.

## Goals / Non-Goals

**Goals:**

- Probe a running provider over HTTP using a caller-provided base URL.
- Use provider API key credentials when supplied, while leaving `GET /health` unauthenticated.
- Export JSON and Markdown review evidence with stable status and check details.
- Keep the probe bounded to discovery and handoff endpoints that are safe to call repeatedly.

**Non-Goals:**

- Do not start a server, build an image, or manage deployment orchestration.
- Do not execute RAG retrieval, answer composition, ingestion, indexing, embedding, Qdrant, or GraphRAG.
- Do not implement registration, heartbeat governance, audit policy, TLS, reverse proxy, or secret management.
- Do not replace the local contract smoke; this complements it for already-running deployments.

## Decisions

- Implement a dedicated `deployed_provider_smoke` service rather than extending local contract smoke.
  - Rationale: local contract smoke validates internal contracts with `TestClient`; deployed smoke validates network reachability, auth, and exported handoff state against a base URL.
  - Alternative considered: add base URL support to `provider_contract_smoke`; rejected because that smoke intentionally executes retrieval/answer checks, which would make deployed probing heavier and less safe.
- Use `httpx.Client` behind a small wrapper.
  - Rationale: `httpx` is already in the project and gives deterministic timeout/error handling without adding dependencies.
  - Alternative considered: use `requests`; rejected because it would add another HTTP client dependency.
- Treat `blocked` as a failing process exit, while `review` remains exportable.
  - Rationale: deployment evidence often requires review because local fixture/mock defaults may still be present, but blocked evidence should stop automation.
  - Alternative considered: require `ready` only; rejected because this would make normal development deployments fail even when the component is reachable and safely reviewable.

## Risks / Trade-offs

- Deployed smoke can only validate the exposed discovery and handoff surface, not the deployment owner's reverse proxy, TLS, or network policy. Mitigation: document it as provider component evidence, not full platform certification.
- A deployment with stale local evidence may return `handoff.status=review` or `blocked`. Mitigation: surface this directly and recommend refreshing handoff evidence before binding.
- Supplying API keys through command-line history can leak secrets. Mitigation: support `PROVIDER_API_KEY` environment fallback and never write the key to reports.
