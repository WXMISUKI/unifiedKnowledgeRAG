## Why

Evidence artifacts are refreshed and aligned with current code/spec, but the progress tracker still contains a historical "24 cases" statement that can be misread as current state.

## What Changes

- Update `docs/progress/provider-improvement-tracker.md` to mark the `24 cases` statement as historical.
- Clarify that current canonical baseline is `26` cases.
- Explicitly document that evidence refresh is now maintained via:
  `python scripts/export_provider_handoff_refresh.py`

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- Documentation consistency for evidence lifecycle and maintenance flow.

## Impact

- Affected docs: `docs/progress/provider-improvement-tracker.md`
- No runtime code changes
- No strategy/default behavior changes
