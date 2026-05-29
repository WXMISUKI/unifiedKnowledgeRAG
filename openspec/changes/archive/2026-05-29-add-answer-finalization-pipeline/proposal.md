## Why

The deterministic answer composer now performs prompt packaging, prompt rendering, output parsing, output validation, and response assembly inline. Future hosted or local LLM composers would otherwise duplicate this safety-critical finalization logic.

## What Changes

- Add a shared answer finalization pipeline service.
- Make deterministic composer produce candidate answer text and delegate parsing, validation, metadata, and fail-closed response assembly to the finalizer.
- Preserve current answer response behavior and metadata.
- Cover the finalizer's invalid-output path directly in service tests.

## Capabilities

### New Capabilities

### Modified Capabilities
- `document-rag`: Refactors cited answer composition through a shared finalization pipeline without changing the public answer contract.

## Impact

- Runtime: centralizes prompt package, render, parser, validator, and response assembly.
- Tests: adds focused finalizer tests for valid and invalid candidate answer text.
- Docs: updates README composer notes to name the finalization pipeline.
