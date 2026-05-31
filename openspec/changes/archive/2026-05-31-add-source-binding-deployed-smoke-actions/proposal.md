## Why

Deployed provider smoke already verifies that the live source binding review endpoint is reachable and not blocked, but its evidence only reports source count and bindable count. Deployment reviewers need the same compact status and recommended-action rollups available in handoff evidence so live deployment smoke can explain what requires review without opening the full endpoint payload.

## What Changes

- Enrich deployed provider smoke `provider_source_bindings` check details with source binding status counts.
- Include source binding recommended action counts in deployed smoke evidence.
- Keep the deployed smoke probe read-only and limited to existing discovery endpoints.
- Preserve existing pass/fail semantics: `ready` and `review` source binding evidence pass the smoke check, while `blocked` or invalid evidence blocks it.
- No runtime defaults, API paths, parser support, indexing behavior, retrieval behavior, answer composition, authentication behavior, or GraphRAG execution are changed.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `provider-roadmap`: Record this as lightweight Phase 6 deployed integration evidence with Phase 2 source binding context.
- `knowledge-provider`: Require deployed provider smoke source binding details to summarize source statuses and recommended actions from existing endpoint evidence.

## Impact

- Affected code: `app/services/deployed_provider_smoke.py`.
- Affected tests: deployed provider smoke tests around source binding details and blocked evidence.
- Affected docs/specs: OpenSpec deltas and roadmap note only.
- Dependencies: none.
