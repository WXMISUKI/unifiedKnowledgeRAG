## 1. Retrieval Gate

- [x] 1.1 Add a backend-neutral unknown source check that can run before retrieval.
- [x] 1.2 Update `POST /api/rag/retrieve` to reject unknown and not-ready sources before backend retrieval.
- [x] 1.3 Make Qdrant source readiness use persisted index lifecycle status.

## 2. Verification And Docs

- [x] 2.1 Add focused regression tests for pre-retrieval gating and Qdrant ready/not-ready behavior.
- [x] 2.2 Update README guidance for ingestion-before-retrieval with Qdrant and local BGE-M3.
- [x] 2.3 Run OpenSpec and pytest verification, then archive the change.
