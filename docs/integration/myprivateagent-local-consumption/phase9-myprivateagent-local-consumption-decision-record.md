# Phase 9 MyPrivateAgent Local Consumption Decision Record

- Decision ID: `phase9-myprivateagent-local-consumption-decision-record-v1`
- Decision Date: `2026-06-01`
- Scope: `myprivateagent local consumption readiness`
- Decision: `ready_for_local_myprivateagent_consumption_review`
- Status: `approved-for-current-slice`

## Current Validation Snapshot

| Item | Current Value |
|---|---|
| Phase 9 local-consumption contract | `ready` |
| Phase 7 provider release readiness | `review` (`release_state=ready_for_local_handoff`) |
| Phase 8 live URL validation readiness | `review` |
| Runtime default promotion | `not approved` |

## Evidence Basis

| Evidence | Current Status | Key Signal |
|---|---|---|
| `phase9-myprivateagent-local-consumption-contract` | `ready` | local URL, auth mode, and ownership boundary are explicit |
| `phase7-provider-release-readiness` | `review` | `ready_for_local_provider_handoff=true`, promotion gates remain open |
| `phase8-live-url-validation-readiness` | `review` | live-url evidence remains review-only |
| `deployed-provider-smoke` | `review` | local deployed smoke exists and is non-blocking |

## Open Gates

1. Runtime promotion gates remain open by design.
2. Private-network/online deployment decisions are deferred to later deployment changes.
3. Provider API key protection remains optional in local development and should be enabled before wider exposure.

## Decision Outcome

The current Phase 9 verdict is to keep local MyPrivateAgent consumption in review-ready state while preserving runtime defaults and control-plane ownership boundaries.

## Next-Step Entry Conditions

1. Keep generating refreshed handoff evidence after each accepted slice.
2. Enable `PROVIDER_API_KEY` when moving beyond trusted local development.
3. Evaluate runtime default promotion only in a separate evidence-backed promotion change.
