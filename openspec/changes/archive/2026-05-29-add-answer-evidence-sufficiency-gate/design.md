## Context

`/api/rag/answer` currently composes an answered response when retrieval returns any document. That is useful for proving the answer envelope, but it is too permissive for enterprise use because weak evidence, too few evidence items, or backend score drift could still produce an answered status.

This change adds a small deterministic sufficiency policy before answer composition. It does not replace future evidence grading, reranking, or LLM-based answer validation; it gives the answer endpoint a configurable fail-closed baseline.

## Goals / Non-Goals

**Goals:**
- Add configuration for minimum evidence count and minimum top evidence score.
- Return `insufficient_evidence` when retrieved documents fail the configured policy.
- Include policy metadata in every answer result so callers can audit why an answer was or was not produced.
- Keep defaults compatible with the existing local fixture and benchmark tests.

**Non-Goals:**
- Choose a production threshold for all backends.
- Implement semantic evidence grading, reranking, or LLM self-checking.
- Change retrieval scoring or `/api/rag/retrieve`.
- Hide retrieved documents from insufficient-evidence responses when they were returned by retrieval.

## Decisions

1. Gate on `min_evidence_count` and `min_top_score`.

   Rationale: these two signals are simple, backend-neutral enough for a first runtime guard, and easy to validate. They do not pretend to solve semantic sufficiency.

   Alternative considered: only gate on empty documents. Rejected because this is already the current MVP and does not protect against weak evidence.

2. Preserve retrieved documents in insufficient-evidence responses.

   Rationale: callers and debugging tools need to see what was retrieved and why the provider refused to answer. The answer text and citations stay empty because the provider did not endorse the evidence as sufficient.

   Alternative considered: omit documents on gate failure. Rejected because it makes diagnosis harder and hides retrieval quality signals.

3. Keep the default policy compatible.

   Rationale: benchmark-driven thresholds are still in progress, and scores are not yet calibrated across fixture, LlamaIndex, and Qdrant. Operators can tighten the policy with environment variables when running stricter experiments.

## Risks / Trade-offs

- Score scales vary by backend -> The policy is configurable and metadata exposes the backend and score threshold.
- A high threshold can produce false negatives -> The default remains permissive until benchmark evidence justifies stricter runtime defaults.
- Count and score cannot prove semantic answerability -> Future evidence grading and reranker changes remain necessary before production LLM answers.
