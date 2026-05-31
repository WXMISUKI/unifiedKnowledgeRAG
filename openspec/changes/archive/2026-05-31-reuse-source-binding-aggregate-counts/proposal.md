## Why

Source binding evidence now exposes compact aggregate counts, but downstream handoff and deployed-smoke summaries still recompute equivalent values from source rows. Reusing the provider-owned counts makes the evidence chain more consistent while retaining compatibility with older persisted reports.

## What Changes

- Prefer top-level `total_source_count`, `bindable_source_count`, `status_counts`, and `recommended_action_counts` when summarizing source binding evidence.
- Preserve fallback row aggregation for older source binding evidence files or deployed providers that do not yet expose compact counts.
- Keep all summaries read-only and evidence-only.
- Do not add binding execution, policy, approval, audit, ingestion, retrieval, answer composition, or GraphRAG behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: provider handoff and deployed smoke summaries reuse source binding aggregate counts when present.
- `provider-roadmap`: records this as lightweight Phase 2/Phase 6 evidence consistency work.

## Impact

- Affected code: provider handoff bundle and deployed provider smoke services
- Affected evidence: handoff bundle summaries and deployed smoke check details
- Compatibility: old source binding evidence remains supported through row-based fallback
- No new runtime dependencies
