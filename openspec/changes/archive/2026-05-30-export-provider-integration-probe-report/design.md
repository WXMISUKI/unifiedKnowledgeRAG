## Overview

Extend `provider_integration_client` with export functions similar to provider contract smoke evidence:

- `provider_integration_probe_report_to_dict(...)`
- `render_provider_integration_probe_markdown(...)`
- `export_provider_integration_probe_report(...)`

Add `scripts/export_provider_integration_probe.py` as the local CLI entry point. It uses FastAPI `TestClient` against `create_app()` so it does not require uvicorn or network access.

## Decisions

- Default output directory: `docs/integration/provider-binding/`.
- Default filenames: `provider-integration-probe.json` and `provider-integration-probe.md`.
- The report keeps `bindable=false` when probe requirements fail and the CLI exits non-zero in that case.
- Markdown is compact and meant for review; JSON is the authoritative machine-readable artifact.
- Preserve read-only behavior: the exporter only calls manifest, preflight, and capabilities through the existing probe.

## Non-Goals

- No remote HTTP client factory.
- No authentication, retries, TLS, service discovery, or registry writes.
- No execution of capability `example_request` payloads.
- No MyPrivateAgent repository changes in this slice.

## Compatibility

The change is additive. Existing provider endpoints and smoke exports remain unchanged.
