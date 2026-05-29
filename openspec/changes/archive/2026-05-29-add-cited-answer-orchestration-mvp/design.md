## Context

The provider already exposes retrieval evidence through `/api/rag/retrieve`, explicit source readiness checks, ingestion lifecycle APIs, and candidate evidence for Qdrant plus BGE-M3. The missing product-facing layer is answer orchestration: callers still need to turn `answer_context` and evidence documents into a final response themselves.

This change keeps the provider in charge of a small, auditable answer contract while avoiding premature production LLM, reranker, or GraphRAG commitments.

## Goals / Non-Goals

**Goals:**
- Add a cited answer API that reuses the configured document retriever.
- Return explicit answer status values for answered and insufficient-evidence outcomes.
- Preserve citations and source evidence in the response.
- Keep the first answer composer deterministic and testable without external model keys.
- Reuse existing unknown-source and index-readiness guardrails before retrieval work begins.

**Non-Goals:**
- Choose or integrate a production chat model such as Qwen, OpenAI, or a local LLM.
- Promote Qdrant, hybrid retrieval, reranking, or GraphRAG as runtime defaults.
- Replace `/api/rag/retrieve` or alter its response contract.
- Implement streaming generation, conversational memory, or agent planning.

## Decisions

1. Add `/api/rag/answer` beside `/api/rag/retrieve`.

   Rationale: answering is a higher-level orchestration contract, while retrieval remains useful for diagnostics, benchmark tooling, and callers that want raw evidence.

   Alternative considered: extend `/api/rag/retrieve` with answer fields. Rejected because it would blur retrieval diagnostics with answer behavior and increase compatibility risk.

2. Introduce a deterministic extractive composer for MVP.

   Rationale: the project still intentionally gates production LLM choices. A deterministic composer lets tests validate statuses, citations, evidence propagation, and refusal behavior before model selection.

   Alternative considered: integrate Qwen immediately. Rejected because answer contract stability, evidence sufficiency, and citation behavior should be proven before adding hosted-model cost and data residency decisions.

3. Treat empty retrieval as `insufficient_evidence`, not an error.

   Rationale: empty retrieval is already a successful retrieval outcome. Answer orchestration should fail closed by returning a machine-readable status rather than a provider error.

   Alternative considered: return HTTP or provider error for no evidence. Rejected because callers need to distinguish system failures from legitimate "I cannot answer from the indexed evidence" outcomes.

4. Reuse existing readiness and unknown-source checks through a shared orchestration service.

   Rationale: answer generation must not bypass the lifecycle guarantees already established for retrieval.

## Risks / Trade-offs

- Deterministic answers are less fluent than LLM-generated answers -> This is acceptable for MVP because the response contract and refusal behavior are the main value of this change.
- Top retrieved evidence may be related but insufficient -> The MVP uses conservative empty-evidence refusal; later changes can add evidence grading stress evidence to runtime answer gating.
- Multi-chunk synthesis remains limited -> This change keeps the composer simple and leaves parent context, reranking, and multi-hop synthesis for separate evidence-gated changes.
