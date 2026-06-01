## Why

After the deployed field-validation contract, readiness export, and deployed handoff consistency smoke are complete, reviewers still need an explicit decision record to avoid ambiguous interpretation of the current live-url posture.

## What Changes

- Add a local decision record for the current Phase 6 deployed field-validation review cycle.
- Explicitly capture the current verdict, open gates, and next-step conditions.
- Keep the slice documentation-only.

## Capabilities

### New Capabilities

- `deployed-field-validation-decision-record`: read-only decision record for Phase 6 deployed field-validation review.

### Modified Capabilities

- `provider-roadmap`: records this decision record as bridge-governance evidence.
- `knowledge-provider`: records the decision artifact as boundary-safe documentation, not runtime promotion.

## Impact

- Affected docs: `docs/operations/deployed-field-validation/phase6-deployed-field-validation-decision-record.md`.
- Runtime defaults remain unchanged.
