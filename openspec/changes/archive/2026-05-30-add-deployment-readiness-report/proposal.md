## Why

The provider now has stable contract, retrieval evidence, answer diagnostics, and fail-closed smoke evidence. The next lightweight roadmap step is Phase 6 deployment/operations evidence so local, public-network, and future private-network deployments can verify readiness without adding platform control-plane behavior.

## What Changes

- Add a local deployment readiness report that summarizes provider health, preflight, contract smoke, runtime configuration, embedding artifact status, and operational notes.
- Export machine-readable JSON and reviewable Markdown under `docs/operations/deployment-readiness/`.
- Add a CLI script for operators to regenerate the report.
- Keep runtime defaults, HTTP APIs, retrieval behavior, vector-store choices, and GraphRAG behavior unchanged.

## Capabilities

### New Capabilities

### Modified Capabilities
- `knowledge-provider`: Provider operations include local deployment readiness evidence for health, preflight, smoke, and configuration review.
- `provider-roadmap`: Phase 6 deployment readiness evidence is represented without turning this project into a general platform control plane.

## Impact

- Affected code: new deployment readiness service and export script.
- Affected docs/evidence: README, roadmap, and generated readiness report files.
- API compatibility: no public API changes.
- Dependencies: none.
