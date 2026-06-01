## Why

Cross-phase evidence is now complete enough that reviewers need one machine-readable release readiness view over Phase 2-6 signals. Without this export, handoff acceptance and runtime-promotion posture remain scattered across many artifacts and easy to misread.

## What Changes

- Add a local Phase 7 provider release readiness export under `docs/operations/provider-release-readiness/`.
- Summarize required handoff gates and optional cross-phase review signals in one report.
- Expose two explicit booleans: local handoff readiness and runtime default promotion readiness.
- Include the report in provider handoff bundle and handoff refresh as optional evidence.
- Keep this change read-only and evaluation-only.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: handoff bundle/refresh can summarize optional Phase 7 release readiness evidence.
- `provider-roadmap`: records Phase 7 cross-phase release-readiness visibility work.

## Impact

- Affected code: new Phase 7 readiness service/export script and handoff integration.
- Affected tests: new readiness tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: local Phase 7 readiness JSON and Markdown artifacts.
- Runtime defaults remain unchanged.
