## Why

The provider can now ingest, index, retrieve, and evaluate evidence, but callers still receive only retrieval context rather than a usable cited answer. The next highest-value slice is to turn the retrieval foundation into a provider-owned answer orchestration contract that can answer when evidence is sufficient and refuse when it is not.

## What Changes

- Add a cited RAG answer endpoint that orchestrates existing document retrieval before composing an answer.
- Return structured answer status, answer text, citations, source evidence, and orchestration metadata.
- Add an evidence sufficiency gate so the provider fails closed with an explicit insufficient-evidence status instead of fabricating answers.
- Keep the first answer composer deterministic and extractive so the contract can be validated without choosing a production LLM provider.
- Preserve the existing `/api/rag/retrieve` contract and existing retrieval backend behavior.

## Capabilities

### New Capabilities

### Modified Capabilities
- `document-rag`: Adds provider-owned cited answer orchestration on top of existing retrieval evidence.

## Impact

- API: adds a new RAG answer endpoint without breaking `/api/rag/retrieve`.
- Contracts: adds request/response models for cited answers, answer status, citations, and metadata.
- Runtime: adds an answer orchestration service that reuses configured retrieval backends and existing source readiness checks.
- Tests: adds focused contract tests for answered, insufficient-evidence, unknown-source, and index-not-ready cases.
- Docs: updates README with local usage examples and scope boundaries.
