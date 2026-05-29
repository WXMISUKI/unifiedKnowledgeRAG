## 1. Contracts

- [x] 1.1 Add cited answer request, result, and response contract models.
- [x] 1.2 Add answer orchestration tests for answered and insufficient-evidence envelopes.

## 2. Runtime

- [x] 2.1 Implement deterministic cited answer orchestration on top of the configured document retriever.
- [x] 2.2 Add `POST /api/rag/answer` while preserving existing retrieval behavior.

## 3. Verification and Docs

- [x] 3.1 Add guardrail tests for unknown source and not-ready source answer requests.
- [x] 3.2 Update README usage notes for cited answer orchestration.
- [x] 3.3 Run focused tests and strict OpenSpec validation.
