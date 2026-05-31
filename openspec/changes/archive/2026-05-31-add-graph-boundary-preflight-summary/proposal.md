## Why

The provider already exposes graph schemas and a planned graph query capability, but provider preflight only reports the graph capability status. External callers need a compact preflight summary that confirms which graph namespaces are discoverable while still making it clear that GraphRAG execution remains gated and planned.

## What Changes

- Enrich the provider preflight `graph_boundary` check with graph schema count and graph ids from the existing source catalog.
- Include graph namespace statuses and graph store labels as informational evidence.
- Preserve current bindability semantics: planned graph execution remains acceptable for this lightweight provider slice.
- Keep graph discovery read-only; no graph query execution, graph store connection, entity extraction, ontology workflow, or GraphRAG dependency is added.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `provider-roadmap`: Record this as Phase 5 boundary/readiness evidence that keeps GraphRAG optional and use-case driven.
- `knowledge-provider`: Require provider preflight graph boundary details to summarize discoverable graph schemas without executing graph queries.

## Impact

- Affected code: `app/services/provider_preflight.py`.
- Affected tests: provider preflight tests around `graph_boundary`.
- Affected docs/specs: OpenSpec deltas and roadmap note.
- Dependencies: none.
