# Phase 6 Deployed Field Validation Contract

## Status

- Phase: `Phase 6 Deployment And Operations`
- Slice: `document-phase6-deployed-field-validation-contract`
- Type: `documentation-only`
- Decision Boundary: `review-only; no runtime default change`

## Purpose

This contract defines what "deployed field validation" means for a real provider URL. It is the boundary between local readiness evidence and live deployed evidence.

## Decision Model

- `field_validation_state`
  - `await_live_url`: no deployed URL evidence exists yet
  - `review`: a live URL or deployed smoke exists, but not all gates are ready
  - `ready`: deployment readiness, handoff, and deployed smoke are all locally consistent for field validation review
- `decision`
  - `keep_local_review_until_deployed_smoke`: local evidence exists but live URL evidence is missing or incomplete
  - `confirm_deployed_field_validation`: live deployed evidence is present and internally consistent
  - `blocked`: required evidence is missing or invalid

## Required Evidence Inputs

1. `docs/operations/deployment-readiness/deployment-readiness.json`
2. `docs/integration/provider-handoff/provider-handoff-bundle.json`
3. `docs/integration/deployed-provider-smoke/deployed-provider-smoke.json`

## Live URL Expectations

- The deployed smoke must record an explicit `base_url`.
- The deployed smoke must summarize `/health`, provider manifest, preflight, source bindings, and handoff checks only.
- If `PROVIDER_API_KEY` is configured in the deployment, the smoke must reflect authenticated `/api/*` access without storing secrets.

## Open Gates That Must Stay Visible

- deployed provider smoke missing or stale
- deployment readiness still review-level
- handoff evidence still review-level
- live URL not yet captured in a deployable smoke report

If any required gate is open, the expected outcome is `decision=keep_local_review_until_deployed_smoke`.

## Non-Goals

- no deployment automation
- no live traffic orchestration
- no runtime default change
- no control-plane ownership transfer
- no GraphRAG execution implementation

## Operator Note

This contract only defines review semantics. Any live deployment validation must be captured in a separate readiness export or smoke report before it can be treated as field validation evidence.
