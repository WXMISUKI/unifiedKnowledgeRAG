## Why

Phase 5 is the right place to make GraphRAG use-case readiness explicit, but we still need a local contract that says when a relationship-heavy problem is graph-worthy and when it should stay in document RAG. Without that, the Phase 5 boundary remains implied instead of reviewable.

## What Changes

- Add a local Phase 5 graph use-case readiness contract document.
- Define the kinds of questions that should justify GraphRAG readiness work.
- Define the kinds of questions that should remain in document RAG.
- Keep GraphRAG execution, graph storage, ontology workflows, and entity extraction out of scope.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records the contract as Phase 5 use-case-driven GraphRAG boundary work.

## Impact

- Affected docs/evidence: `docs/benchmark/chinese-seed/graph-use-case-readiness/phase5-graph-use-case-readiness-contract.md`
- Affected docs: `docs/roadmap/lightweight_provider_roadmap.md`, `docs/progress/provider-improvement-tracker.md`
- No runtime default changes, no new HTTP API, no new dependencies
