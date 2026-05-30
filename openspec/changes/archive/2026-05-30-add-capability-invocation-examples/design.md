## Overview

Add optional example request metadata to each `CapabilityInvocation`. The examples are owned by the provider, are serializable, and are intended for control-plane binding, documentation, and local smoke validation.

## Decisions

- Store examples on `CapabilityInvocation` as `example_request: dict[str, Any] | None`.
- Keep examples minimal and deterministic by using existing fixture source ids and the planned graph namespace.
- Treat examples as integration hints. They MUST NOT imply production embedding model, vector database, reranker, graph store, or hosted answer composer choices.
- Validate only the presence and basic shape of examples in capability smoke. Runtime contract tests already validate the actual RAG endpoints and graph planned boundary.

## Non-Goals

- No automatic execution of capability examples by `GET /api/capabilities`.
- No generated SDK/client in this slice.
- No new vector database, embedding model, graph store, or model-provider dependency.

## Compatibility

The added field is optional and additive in the HTTP response model. Existing consumers that ignore unknown fields remain compatible, while MyPrivateAgent can use the examples to construct first-call probes.
