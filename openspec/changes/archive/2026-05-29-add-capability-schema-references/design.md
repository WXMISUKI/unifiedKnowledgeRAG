## Context

`/api/capabilities` now gives callers stable ids plus HTTP method/path invocation metadata. For agent integration, the next missing piece is a machine-readable pointer to the request and response contracts. FastAPI already exposes Pydantic models in OpenAPI, so this change can reference those schemas instead of inventing a separate registry format.

## Goals / Non-Goals

**Goals:**
- Add request and response schema refs to HTTP invocation metadata.
- Reference existing OpenAPI component schema names.
- Keep the fields optional so non-HTTP or not-yet-modeled capabilities remain possible.
- Preserve existing endpoint behavior.

**Non-Goals:**
- Inline full JSON schemas in `/api/capabilities`.
- Add examples, auth scopes, tenant policy, rate limits, or streaming metadata.
- Generate schemas manually or duplicate OpenAPI content.

## Decisions

1. Store schema refs as strings.

   Rationale: OpenAPI references such as `#/components/schemas/RagAnswerRequest` are stable, compact, and easy for callers to resolve against `/openapi.json`.

2. Put schema refs inside `invocation`.

   Rationale: request/response schema references describe how to invoke a capability over HTTP. Keeping them with method/path avoids widening the top-level capability model too early.

3. Use optional fields.

   Rationale: planned or non-HTTP future capabilities may not have schema refs immediately.

## Risks / Trade-offs

- Schema names can change if Pydantic models are renamed -> Contract tests pin the current names for the capabilities that matter.
- Callers must fetch `/openapi.json` to dereference schemas -> This is acceptable because FastAPI already serves the canonical schema document.
