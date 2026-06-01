## Summary

Create a lightweight contract document that defines how deployed field validation must be interpreted once a live base URL exists.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations.
- Nature: documentation-only governance contract.
- Non-goal: runtime default switching, deployment automation, traffic management, or control-plane ownership changes.

## Contract Content

- Decision and review-state model:
  - `field_validation_state`: `await_live_url` | `review` | `ready`
  - `decision`: `keep_local_review_until_deployed_smoke` | `confirm_deployed_field_validation` | `blocked`
- Required evidence classes:
  - deployment readiness report
  - provider handoff bundle
  - deployed provider smoke report, when a live URL exists
- Live URL expectations:
  - explicit `base_url` provenance
  - protected `/api/*` access behavior when API key is configured
  - summary of deployed handoff and source binding status
- Open-gate expectations:
  - no automatic promotion
  - no deployment orchestration
  - no control-plane ownership transfer

## Verification

- `openspec validate document-phase6-deployed-field-validation-contract --strict`
