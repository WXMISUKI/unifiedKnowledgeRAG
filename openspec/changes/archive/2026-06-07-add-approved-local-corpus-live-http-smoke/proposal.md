## Why

The approved `company_profile_2025_trial` source now passes an in-process acceptance smoke, but MyPrivateAgent and other callers will consume it over a running local HTTP provider. A minimal live HTTP smoke closes this provider-side local usability gap before moving the next work into the caller repository.

## What Changes

- Add a live HTTP smoke for an already running provider at a configurable base URL.
- Validate catalog visibility, source document manifest availability, multiple answerable company-profile questions, citation allowlist behavior, and an unrelated negative-control query over HTTP.
- Export JSON and Markdown reports under `docs/local-run/approved-local-corpus-live-http/`.
- Keep this as a provider-side local trial gate: no source registration, source-to-agent binding, MyPrivateAgent orchestration, backend promotion, OCR startup, vector database calls, or GraphRAG execution.

## Capabilities

### New Capabilities

- `approved-local-corpus-live-http-smoke`: Covers live HTTP usability status for a registered approved local corpus source.

### Modified Capabilities

- `approved-local-corpus-acceptance-smoke`: The in-process acceptance rules can be reused by a separate live HTTP caller path without changing the in-process contract.

## Impact

- Affected code: a small HTTP client adapter, a live HTTP smoke export service or wrapper, a CLI export script, and focused tests.
- Affected docs: quickstart, README, lightweight roadmap, and provider improvement tracker.
- Runtime API shape remains unchanged.
