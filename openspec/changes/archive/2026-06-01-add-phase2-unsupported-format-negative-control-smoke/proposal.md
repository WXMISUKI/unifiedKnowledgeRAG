## Why

Phase 2 demand readiness now exists, but parser-expansion review still needs a compact smoke artifact that continuously exposes unsupported-format and non-markdown negative controls. Without this smoke, reviewers must manually inspect readiness details each time.

## What Changes

- Add a local Phase 2 unsupported-format negative-control smoke report under `docs/smoke/source-format-demand/`.
- Validate readiness presence, markdown positive control, unsupported/non-markdown negative controls, and decision alignment.
- Include this smoke report in provider handoff bundle and handoff refresh as optional evidence.
- Keep the smoke read-only and evaluation-only.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records this as Phase 2 smoke visibility work.
- `knowledge-provider`: handoff bundle/refresh can summarize optional Phase 2 unsupported-format negative-control smoke evidence.

## Impact

- Affected code: new Phase 2 smoke service and export script.
- Affected tests: new smoke tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: local JSON and Markdown smoke artifacts.
- Runtime defaults remain unchanged.
