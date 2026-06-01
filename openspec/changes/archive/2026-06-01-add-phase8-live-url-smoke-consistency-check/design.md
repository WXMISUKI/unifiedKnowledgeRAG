## Design Overview

This change adds a compact Phase 8 consistency smoke that compares two local artifacts:

1. Phase 8 live URL validation readiness export
2. Provider handoff bundle row for `phase8_live_url_validation_readiness`

The smoke checks status and key summary fields:

- `live_validation_state`
- `decision`
- `deployed_smoke_present`
- `deployed_smoke_status`
- `live_url_present`
- `open_gate_count`

## Decisions

- The smoke is `ready` only when every comparison check passes.
- Any mismatch is `blocked` to make evidence drift explicit.
- This check is optional in handoff evidence and does not change required artifact gating.

## Boundaries

- No deployed HTTP calls
- No runtime default promotion
- No ingestion/retrieval/graph execution changes
