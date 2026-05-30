## Context

The provider is intentionally lightweight: it returns trusted evidence, citations, traces, and diagnostics while callers own final answer policy. The newly added `evidence_pack-v1` helps callers decide what can be cited. However, a caller also needs executable evidence that the provider fails closed when no evidence is found.

## Goals / Non-Goals

**Goals:**
- Add an executable smoke check for insufficient-evidence retrieve and answer behavior.
- Keep the check local and deterministic with the fixture backend.
- Record compact smoke details in JSON and Markdown evidence.

**Non-Goals:**
- Do not change retrieval ranking or thresholds.
- Do not add a new runtime gate.
- Do not introduce LLM grading, reranking, or GraphRAG checks.

## Decisions

1. Add one smoke check named `rag_insufficient_evidence_pack_contract`.
   - Rationale: a single check can exercise both retrieve and answer with the same unsupported query while keeping the smoke report readable.
   - Alternative considered: separate retrieve and answer checks. Rejected for now because the contract assertion is about one fail-closed evidence pack behavior across both endpoints.

2. Use an unsupported local query against `refund_policy_docs`.
   - Rationale: this matches existing provider contract tests and avoids external data or Qdrant dependencies.

3. Keep compact Markdown details.
   - Rationale: exported smoke should show status, reason, and counts without embedding full response bodies.

## Risks / Trade-offs

- The smoke report check count changes -> Update tests and exported evidence together.
- Fixture behavior could accidentally start matching the unsupported query -> Use the existing moon-warehouse query already covered by API tests.
