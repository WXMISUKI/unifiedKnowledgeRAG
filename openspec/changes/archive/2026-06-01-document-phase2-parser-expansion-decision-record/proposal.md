## Why

Phase 2 now has both source-format demand readiness and unsupported-format negative-control smoke, but reviewers still need one explicit decision record that freezes this cycle's parser-expansion verdict. Without it, later discussions may misread evidence snapshots as runtime parser promotion approval.

## What Changes

- Add a Phase 2 parser-expansion decision record under `docs/operations/source-format-demand/`.
- Record current evidence basis and explicit verdict to keep Markdown baseline.
- Keep this change documentation-only; no runtime/parser/API behavior change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: adds a traceable Phase 2 parser-expansion decision checkpoint.
- `knowledge-provider`: documents current parser boundary verdict over existing evidence artifacts.

## Impact

- Affected docs: one decision record markdown plus tracker/roadmap refresh.
- No code-path, deployment, or API impact.
