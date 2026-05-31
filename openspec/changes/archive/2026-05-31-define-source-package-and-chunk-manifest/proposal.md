## Why

The provider is moving from fixture-friendly RAG toward enterprise document onboarding, but callers and operators still lack a compact source-level package description and a stable chunk-level manifest before ingestion. Adding these diagnostics gives MyPrivateAgent and deployment reviewers enough evidence to judge source readiness without adding heavy parsers, policy workflows, or graph infrastructure.

## What Changes

- Add a lightweight source package contract for each RAG source, including source id, owner, version, language, domain, sensitivity, supported formats, default chunking strategy, and citation granularity.
- Add chunk manifest diagnostics for markdown sources, including stable chunk id, citation, strategy, character count, source path, and preview.
- Surface source package and chunk manifest metadata through existing read-only source document and ingestion preflight flows.
- Document that this is Phase 2 ingestion evidence and does not create ingestion jobs, rebuild indexes, parse heavy formats, call embedding/vector stores, or execute GraphRAG.

## Capabilities

### New Capabilities

### Modified Capabilities

- `document-rag`: Add source package and chunk manifest diagnostics to document RAG source readiness.
- `provider-roadmap`: Record source package and chunk manifest work as lightweight Phase 2 ingestion evidence.

## Impact

- Affected APIs: `GET /api/rag/sources/{source_id}/documents` and `GET /api/ingestion/sources/{source_id}/preflight`
- Affected code: source document manifest service, ingestion preflight service, response contracts, and tests
- Affected docs/specs: README, lightweight roadmap, `document-rag`, and `provider-roadmap`
- No new runtime dependencies, parser framework, OCR, vector database default, ingestion mutation endpoint, or GraphRAG execution
