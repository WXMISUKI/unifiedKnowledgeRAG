## Context

The current handoff bundle summarizes:

- provider integration probe
- provider contract smoke
- deployment readiness
- reindex readiness

The bundle intentionally does not regenerate those prerequisites. That was the right boundary for a read-only index, but it means reviewers need a separate refresh step before trusting the bundle after changes.

## Approach

Add `provider_handoff_refresh` as a service-level orchestrator that calls existing local export functions:

1. `export_provider_integration_probe_report(...)`
2. `export_provider_contract_smoke_report(...)`
3. `export_deployment_readiness_report(...)`
4. `export_reindex_readiness_report(...)`
5. `export_provider_handoff_bundle_report(...)`

The refresh command then writes its own summary:

- `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json`
- `docs/integration/provider-handoff-refresh/provider-handoff-refresh.md`

## Status Rules

The refresh summary is conservative:

- `blocked` if any step raises an exception or returns a blocked/failing status.
- `review` if all steps complete but at least one report is in review.
- `ready` if all steps complete and every report is ready/passed/bindable.

The default local environment is expected to remain `review` because deployment readiness still flags mock/non-Qdrant production promotion notes.

## Read-Only Boundary

This workflow writes evidence files only. It does not start a server, add HTTP APIs, create ingestion jobs, rebuild indexes, download models, call Qdrant, or execute GraphRAG. It may run the existing local contract smoke because that is already part of the provider's executable contract evidence and uses FastAPI TestClient.

## Error Handling

If a step fails, the workflow records the step failure and still writes the refresh summary. Later steps are skipped after the first failure so the report clearly identifies the earliest blocker.
