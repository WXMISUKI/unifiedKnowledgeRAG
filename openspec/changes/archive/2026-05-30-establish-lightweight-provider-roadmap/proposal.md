## Why

The provider has enough foundation that continuing only change-by-change can drift into over-design or scattered optimization. We need a lightweight roadmap that keeps the project focused on trustworthy retrieval evidence for external callers, not a heavy agent platform.

## What Changes

- Establish a lightweight staged roadmap for the provider.
- Define phase gates in terms of evidence, contracts, and reversible implementation slices.
- Reaffirm that MyPrivateAgent remains the control plane and final-response orchestrator.
- Reaffirm that this provider is the knowledge data plane: retrieve evidence, expose citations, report readiness, and keep infrastructure choices behind explicit gates.
- Document non-goals so future changes do not add agent runtime, policy, approval, or broad orchestration responsibilities to this module.

## Capabilities

### New Capabilities

- `provider-roadmap`: project-level roadmap and phase gates for lightweight knowledge-provider development.

### Modified Capabilities

None.

## Impact

- Adds roadmap documentation under `docs/roadmap/`.
- Adds a canonical OpenSpec capability for phase gates and project direction.
- Does not change runtime APIs, retrieval behavior, vector database defaults, GraphRAG behavior, or MyPrivateAgent integration code.
