## Why

The provider already exposes graph schemas and verifies the planned graph query boundary in contract smoke, but contract smoke does not directly validate graph schema discovery. External callers need local smoke evidence that the graph namespace metadata is discoverable before any future GraphRAG execution is approved.

## What Changes

- Add a read-only graph schema discovery check to provider contract smoke.
- Record graph count, graph ids, entity type count, relation type count, status, and graph store label in smoke details.
- Preserve the existing planned graph query boundary check and fail-closed semantics.
- Do not add graph query execution, graph storage connections, entity extraction, ontology workflows, or GraphRAG dependencies.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `provider-roadmap`: Record this as lightweight Phase 5 graph boundary evidence, not GraphRAG execution promotion.
- `knowledge-provider`: Require provider contract smoke to validate graph schema discovery separately from planned graph query execution.

## Impact

- Affected code: `app/services/provider_contract_smoke.py`.
- Affected tests: `tests/test_provider_contract_smoke.py`.
- Affected evidence: exported provider contract smoke JSON/Markdown includes one additional check.
- Dependencies: none.
