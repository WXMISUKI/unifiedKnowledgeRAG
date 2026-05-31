## Why

Phase 4 already has an `evidence_pack-v1` shape in retrieval and answer envelopes, but the caller-facing consumption rules are still spread across code, tests, and smoke checks. We need one read-only contract artifact that explains how callers should consume the pack without turning the provider into the final answer owner.

## What Changes

- Add a local Phase 4 evidence pack consumption contract document under `docs/benchmark/chinese-seed/evidence-pack-consumption-contract/`.
- Make the caller contract explicit for `answerable` and `insufficient_evidence` paths.
- Tie the contract back to the existing evidence pack fields, provenance metadata, and fail-closed behavior already present in the provider.
- Keep the change review-oriented and read-only. No runtime defaults, APIs, or answer policy ownership change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `document-rag`: evidence pack consumption rules become explicit and reviewable for callers.
- `provider-roadmap`: records the consumption contract as Phase 4 evidence packaging work.
- `knowledge-provider`: reflects the caller-facing evidence pack contract in provider evidence language.

## Impact

- Affected docs: `docs/benchmark/chinese-seed/evidence-pack-consumption-contract/phase4-evidence-pack-consumption-contract.md`
- Affected specs: `openspec/specs/document-rag/spec.md`, `openspec/specs/provider-roadmap/spec.md`, `openspec/specs/knowledge-provider/spec.md`
- No runtime behavior changes, no new API endpoints, no new dependencies
