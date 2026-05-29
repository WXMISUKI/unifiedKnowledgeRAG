## Why

The provider exposes `knowledge.rag.answer` and an answer composer boundary, but health and capability status do not yet report whether the configured composer can actually run. This makes misconfigured hosted/local composer settings visible only at invocation time instead of during readiness checks.

## What Changes

- Add answer composer readiness metadata to provider health.
- Make `knowledge.rag.answer` capability status reflect configured composer readiness.
- Preserve retrieval and graph readiness behavior.
- Keep hosted/local composers fail-closed until future model integration changes approve them.

## Capabilities

### New Capabilities

### Modified Capabilities
- `knowledge-provider`: Adds answer composer readiness reporting to health and capability discovery.

## Impact

- API: enriches `GET /health` with an `answer` component.
- API: `GET /api/capabilities` reports `knowledge.rag.answer` as `degraded` when the configured composer is unavailable.
- Runtime: adds a lightweight readiness helper for answer composer configuration.
- Tests: adds provider contract coverage for ready and degraded answer readiness.
