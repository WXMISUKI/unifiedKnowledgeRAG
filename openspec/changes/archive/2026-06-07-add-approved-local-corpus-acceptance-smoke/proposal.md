## Why

The approved `company_profile_2025_trial` source is now provider-visible and can answer a single smoke query, but that does not yet prove the registered local corpus is useful for a small set of business questions. A lightweight acceptance smoke gives a clear `go` / `review` / `blocked` signal before moving the corpus into MyPrivateAgent-side trial usage.

## What Changes

- Add a repository-local acceptance smoke over the approved local corpus source.
- Validate catalog visibility, source document manifest availability, multiple answerable company-profile questions, citation allowlist behavior, and an unrelated negative-control query.
- Export JSON and Markdown reports under `docs/local-run/approved-local-corpus-acceptance/`.
- Keep the smoke lightweight and local: no external server startup, OCR, Qdrant/BGE promotion, source binding, MyPrivateAgent orchestration, or GraphRAG execution.

## Capabilities

### New Capabilities

- `approved-local-corpus-acceptance-smoke`: Covers local acceptance status for a registered approved local corpus source.

### Modified Capabilities

- `approved-local-corpus-source-registration`: Registered local sources can feed a separate acceptance smoke.
- `local-usable-run-loop`: Local usability evidence can include an approved local corpus acceptance smoke without changing the generic run-loop contract.

## Impact

- Affected code: a new acceptance smoke service, a CLI export script, and focused tests.
- Affected docs: quickstart, README, lightweight roadmap, and provider improvement tracker.
- Runtime API shape remains unchanged.
