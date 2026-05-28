## 1. Specification

- [x] 1.1 Create OpenSpec proposal for `add-knowledge-provider-v1`
- [x] 1.2 Create OpenSpec design for provider boundary and first implementation slice
- [x] 1.3 Create `knowledge-provider` spec covering health, capabilities, catalog, and graph boundary
- [x] 1.4 Create `document-rag` spec covering sources and retrieval behavior
- [x] 1.5 Validate the OpenSpec change

## 2. Provider Scaffold

- [x] 2.1 Add Python package structure under `app/`
- [x] 2.2 Add Pydantic HTTP contract models
- [x] 2.3 Add static source catalog service
- [x] 2.4 Add deterministic document retrieval service
- [x] 2.5 Add FastAPI routers for health, capabilities, catalog, RAG, and graph endpoints

## 3. Verification

- [x] 3.1 Add focused provider contract tests
- [x] 3.2 Verify tests fail before implementation
- [x] 3.3 Implement minimal code until tests pass
- [x] 3.4 Run the focused pytest suite
- [x] 3.5 Run OpenSpec validation

## 4. Documentation

- [x] 4.1 Update README with local run and smoke test commands
- [x] 4.2 Record that GraphRAG is a v1 contract boundary but not implemented in the first runtime slice
