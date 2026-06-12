## Why

MyPrivateAgent now exports a repo-side trial outcome that keeps the caller report readable while placing the provider Phase 25-compatible payload under `provider_feedback_input`. Phase 25 currently reads only the flat payload shape, so passing the whole MyPrivateAgent artifact stays conservative even when the nested payload is complete.

This change closes the last small handoff gap in the caller-provider feedback loop without expanding provider retrieval behavior.

## What Changes

- Phase 25 feedback input loading accepts either the original flat caller outcome shape or a MyPrivateAgent repo-side trial outcome containing `provider_feedback_input`.
- The flat payload contract remains supported.
- Focused tests cover the nested payload path and the existing flat payload path.
- The caller input contract documents the nested compatibility shape.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `myprivateagent-live-trial-outcome-feedback`: accepts nested `provider_feedback_input` as the Phase 25 feedback payload source.

## Impact

- Affected code:
  - `app/services/phase25_myprivateagent_live_trial_outcome_feedback.py`
- Affected tests:
  - `tests/test_phase25_myprivateagent_live_trial_outcome_feedback.py`
- Affected docs:
  - `docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-outcome-input-contract.md`
- Non-goals:
  - No provider HTTP calls
  - No retrieval strategy changes
  - No query rewrite, rerank, hybrid retrieval, or GraphRAG execution
