## Why

The local provider, PDF-derived markdown trial, and local business corpus trial are all `go` for the company profile sample. The next useful step is to package that result for a caller without pretending the source has been formally registered.

This helps MyPrivateAgent or another caller review the trial source id, markdown artifact, overlay, chunks, citation policy, and current limitations before deciding whether to proceed with a real integration path.

## What Changes

- Add a local corpus caller handoff export over an existing local business corpus trial report.
- Summarize source id, title, markdown path, overlay path, chunks path, trial decision, citations, recommended query, and next actions.
- Classify handoff status as `ready_for_caller_review`, `review`, or `blocked`.
- Preserve explicit boundaries: `registration_status=not_registered`, default source catalog unchanged, no source binding.
- Update docs with the handoff export command and where to find the generated artifacts.

## Capabilities

### New Capabilities

- `local-corpus-caller-handoff`: Local-only caller handoff package for a business corpus trial result.

### Modified Capabilities

- `local-business-corpus-trial-loop`: Clarify that a `go` trial can be exported into a caller-facing handoff without formal source registration.

## Impact

- Affected code: new handoff service, export script, focused tests.
- Affected docs: quickstart, README, roadmap, progress tracker, generated local handoff artifacts.
- Affected APIs: none.
- Dependencies: none.
- Systems: no default source catalog mutation, no formal ingestion, no source binding, no MyPrivateAgent code changes, no backend promotion, no GraphRAG execution.
