## Summary

Add one lightweight exporter that consolidates deployed field validation evidence into a single local readiness artifact.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations.
- Nature: evaluation-only evidence export.
- Non-goal: runtime promotion, deployment automation, live traffic orchestration, or API behavior change.

## Inputs

- Contract:
  - `docs/operations/deployed-field-validation/phase6-deployed-field-validation-contract.md`
- Deployment and integration evidence:
  - `docs/operations/deployment-readiness/deployment-readiness.json`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json`
  - `docs/integration/deployed-provider-smoke/deployed-provider-smoke.json`

## Output

- JSON:
  - `docs/operations/deployed-field-validation/phase6-deployed-field-validation-readiness.json`
- Markdown:
  - `docs/operations/deployed-field-validation/phase6-deployed-field-validation-readiness.md`

Core sections:

- `summary`: total/ready/review/blocked signals.
- `signals`: compact readiness signals with recommended actions.
- `field_validation_state` and `decision`: explicit review state and keep-default posture until live URL evidence is present.

## Handoff Integration

- Add optional handoff artifact id:
  - `phase6_deployed_field_validation_readiness`
- Add non-blocking handoff refresh step before provider handoff bundle.

## Verification

- Focused pytest:
  - `tests/test_phase6_deployed_field_validation_readiness.py`
  - `tests/test_provider_handoff_bundle.py`
  - `tests/test_provider_handoff_refresh.py`
- `openspec validate export-phase6-deployed-field-validation-readiness --strict`
