## Why

The cited answer endpoint now exists, but its first MVP answers whenever retrieval returns any document. The next highest-value safety slice is to make answer generation fail closed when retrieved evidence does not satisfy a configurable sufficiency policy.

## What Changes

- Add provider settings for answer evidence sufficiency, including minimum evidence count and minimum top evidence score.
- Apply the sufficiency policy before composing an answered response.
- Return `answer_status=insufficient_evidence` with evidence and gate metadata when retrieved documents fail the policy.
- Preserve the deterministic composer and existing retrieval endpoint behavior.
- Keep default settings conservative and compatible with the current local fixture path while allowing stricter thresholds in runtime or tests.

## Capabilities

### New Capabilities

### Modified Capabilities
- `document-rag`: Adds configurable evidence sufficiency gate behavior to cited answer orchestration.

## Impact

- Configuration: adds answer sufficiency settings to `Settings` and environment parsing.
- Runtime: updates answer orchestration to evaluate evidence before returning `answered`.
- API: no new endpoint; enriches `metadata` for answer envelopes.
- Tests: adds focused coverage for low-score and insufficient-count gate outcomes.
- Docs: updates README with the new answer gate configuration knobs.
