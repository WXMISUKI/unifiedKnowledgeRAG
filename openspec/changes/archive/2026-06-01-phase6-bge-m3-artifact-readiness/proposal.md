## Why

Phase 6 deployment readiness already knows whether a local embedding model path is configured, but it does not yet give reviewers a dedicated artifact-level proof that the BGE-M3 snapshot is complete, checksumable, and suitable for private-network reuse. Without that bridge, Phase 3 promotion review still depends on a vague "model path exists" signal instead of a concrete artifact readiness contract.

## What Changes

- Add a local BGE-M3 artifact readiness contract and export under `docs/operations/bge-m3-artifact-readiness/`.
- Record checksum-aware manifest and file inventory evidence for the local BGE-M3 snapshot.
- Summarize deployment-adjacent model readiness, private-network copyability, and Phase 3 bridge status in a machine-readable report.
- Surface the artifact readiness export through provider handoff and refresh as optional evidence.
- Keep the work read-only and evaluation-only; do not change runtime defaults, embedding promotion decisions, or public API contracts.

## Capabilities

### New Capabilities
- `bge-m3-artifact-readiness`: checksum-aware local BGE-M3 artifact validation and readiness export for the Phase 6 / Phase 3 bridge.

### Modified Capabilities
- `knowledge-provider`: provider handoff and refresh can summarize optional BGE-M3 artifact readiness evidence.
- `provider-roadmap`: records BGE-M3 artifact readiness as lightweight deployment evidence that supports, but does not decide, Phase 3 promotion.

## Impact

- Affected code: BGE-M3 model bootstrap manifest, new artifact readiness service and export script, handoff bundle/refresh wiring.
- Affected tests: manifest validation, checksum/readiness export, and focused handoff assertions.
- Affected docs/evidence: local JSON and Markdown artifact readiness report under `docs/operations/bge-m3-artifact-readiness/`.
- Runtime defaults remain unchanged.
