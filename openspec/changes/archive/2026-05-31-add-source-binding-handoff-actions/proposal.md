## Why

The provider handoff bundle already includes source binding evidence, but its source-binding artifact summary only reports the overall status and bindable count. External control planes and deployment reviewers need a compact action-oriented summary so they can see whether source binding evidence is ready, reviewable, or blocked without opening the full source-binding report first.

## What Changes

- Enrich the provider handoff bundle summary for `source_binding_summary` evidence with source status counts.
- Include recommended action counts from source binding evidence in the handoff artifact summary.
- Keep the handoff bundle read-only and file-backed; it must not regenerate evidence, call HTTP endpoints, execute retrieval, create ingestion jobs, or change binding decisions.
- No runtime defaults, API paths, authentication behavior, parser support, indexing behavior, retrieval behavior, answer composition, or GraphRAG execution are changed.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `provider-roadmap`: Record this as lightweight Phase 2/6 source binding handoff evidence work.
- `knowledge-provider`: Require the provider handoff bundle to summarize source binding status and recommended actions from existing source binding evidence.

## Impact

- Affected code: `app/services/provider_handoff_bundle.py`.
- Affected tests: provider handoff bundle tests around source binding artifact summaries.
- Affected docs/specs: OpenSpec deltas only; public endpoint paths and persisted evidence file locations stay the same.
- Dependencies: none.
