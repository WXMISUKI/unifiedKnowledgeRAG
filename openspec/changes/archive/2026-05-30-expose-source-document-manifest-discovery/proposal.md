## Why

The provider now exposes a source document manifest endpoint, but external callers still need a stable discovery path to find and preflight that endpoint. For a component used by MyPrivateAgent, the next lightweight step is to make the diagnostic API visible through provider manifest, capability metadata, and binding checks without adding retrieval or indexing behavior.

This advances roadmap Phase 0 and Phase 2: Phase 0 integration evidence stays current, and Phase 2 document diagnostics become discoverable.

## What Changes

- Add a provider capability id for source document manifest diagnostics.
- Add manifest endpoint metadata for the source document manifest route template.
- Allow preflight/schema checks to validate read-only GET capabilities that do not have a request body schema.
- Extend smoke and integration probe expectations so callers can verify the new diagnostic capability before binding.
- Update README guidance for MyPrivateAgent-style callers.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: discovery, preflight, and smoke evidence SHALL include the source document manifest capability.
- `document-rag`: source document manifest diagnostics SHALL be discoverable through capability metadata.

## Impact

- Affects provider manifest, capabilities, preflight, provider smoke, integration probe defaults, README, and tests.
- No new dependency, storage layer, vector query, ingestion behavior, graph behavior, or runtime retrieval default change.
