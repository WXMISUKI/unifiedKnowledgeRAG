## Why

Capabilities now expose status, invocation metadata, and schema references, but degraded or planned statuses do not explain why. Upper-layer agents need a short machine-readable reason to decide whether to retry, degrade gracefully, or show an operator-facing hint.

## What Changes

- Add an optional `reason` field to capability entries.
- Populate `knowledge.rag.answer.reason` when answer composer readiness is degraded.
- Populate `knowledge.graph.query.reason` to explain the planned boundary.
- Preserve existing capability ids, statuses, descriptions, invocation metadata, and schema refs.

## Capabilities

### New Capabilities

### Modified Capabilities
- `knowledge-provider`: Adds optional capability status reason metadata.

## Impact

- API: enriches `GET /api/capabilities` with optional status reasons.
- Contracts: extends `Capability` with a nullable reason.
- Tests: verifies degraded answer and planned graph capabilities expose useful reasons.
- Docs: updates README capability discovery notes.
