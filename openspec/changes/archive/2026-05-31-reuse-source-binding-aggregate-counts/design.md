## Context

`GET /api/provider/source-bindings` and its export now include compact aggregate counts. Existing handoff bundle and deployed smoke code can already summarize source binding rows, but this duplicates logic that the provider now owns directly.

The change should improve consistency without breaking persisted evidence generated before the compact count fields existed.

## Goals / Non-Goals

**Goals:**

- Prefer compact source binding counts when available.
- Keep fallback row aggregation for backward compatibility.
- Keep the summaries deterministic and side-effect-free.
- Avoid changing readiness decisions or runtime defaults.

**Non-Goals:**

- Changing source binding readiness rules.
- Creating bindings or adding binding policy.
- Regenerating evidence from the handoff endpoint.
- Running ingestion, retrieval, answer composition, or GraphRAG.

## Decisions

- Use a small normalization helper for integer counts.
  This keeps malformed or missing count fields from breaking evidence review.

- Use compact count dictionaries when they are present and shaped as dictionaries.
  The provider-owned aggregate fields are the preferred source of truth for current evidence.

- Fall back to row aggregation for older evidence.
  Persisted reports and already-deployed providers should remain reviewable.

- Preserve the current output names in deployed smoke details.
  Deployed smoke already exposes `source_count`, `bindable_source_count`, `source_status_counts`, and `recommended_action_counts`; only their preferred input changes.

## Risks / Trade-offs

- Malformed compact count fields could hide row details -> fallback only applies when compact fields are missing or not dictionaries.
- Slightly more helper code -> keeps the compatibility behavior explicit and tested.
