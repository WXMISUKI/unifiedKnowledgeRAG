## Context

`/api/capabilities` is becoming the provider's lightweight machine-readable registry. It already carries stable ids, status, invocation method/path, and schema refs. The remaining gap for operational use is that a non-ready status has no local explanation.

The answer composer readiness helper already returns a reason, and graph query already has a planned boundary reason in health. This change carries those reasons into capability discovery without changing endpoint behavior.

## Goals / Non-Goals

**Goals:**
- Add optional capability reason metadata.
- Explain degraded `knowledge.rag.answer` status directly in capability discovery.
- Explain planned `knowledge.graph.query` status directly in capability discovery.
- Keep ready capabilities allowed to omit reason.

**Non-Goals:**
- Add structured error codes to capabilities.
- Add retry policy, severity, ownership, or remediation links.
- Change `/health` or endpoint runtime behavior.

## Decisions

1. Add a nullable top-level `reason` on `Capability`.

   Rationale: status and reason belong together and apply regardless of invocation protocol.

2. Reuse answer composer readiness reason.

   Rationale: keeping the reason source shared prevents `/health` and `/api/capabilities` from drifting.

## Risks / Trade-offs

- Free-text reasons are less machine-actionable than codes -> This is acceptable for the next slice; codes can be added later if orchestration needs branching.
- Ready capabilities may have `reason=null` -> This keeps the response concise and avoids noisy status text.
