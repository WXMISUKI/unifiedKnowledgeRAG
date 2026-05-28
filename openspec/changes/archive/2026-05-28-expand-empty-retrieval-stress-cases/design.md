## Context

The retrieval benchmark is now used as decision evidence for Qdrant, BGE-M3, score thresholds, and future reranker or hybrid retrieval work. The positive cases cover several Chinese enterprise support patterns, but expected-empty coverage is still narrow.

Expected-empty cases are important because dense retrieval can confidently return semantically nearby but unsupported evidence. This is especially risky in enterprise RAG because unsupported questions should not be answered with unrelated policy snippets.

## Goals / Non-Goals

**Goals:**
- Increase empty retrieval coverage with realistic unsupported business questions.
- Keep fixture baseline deterministic and passing.
- Regenerate Qdrant+BGE single-threshold and threshold sweep evidence.
- Keep this as evaluation hardening only.

**Non-Goals:**
- Do not change retrieval algorithms or default score threshold.
- Do not add empty-intent classification.
- Do not introduce reranker or hybrid retrieval.
- Do not add customer private data.

## Decisions

1. Add only unsupported cases, not new source documents.

   The purpose is to test refusal/no-evidence behavior against the existing source scope. Adding source documents would change what should be answerable and blur the signal.

2. Use plausible enterprise support topics.

   Cases should look like real support questions, not artificial nonsense. This better approximates the false-positive pressure we will see in production.

3. Keep all expected-empty cases citation-free.

   Empty cases use `expected_source_id=null`, `expected_citation=null`, and `expect_empty=true`, preserving the benchmark contract.

## Risks / Trade-offs

- [Risk] The seed set still remains small compared with production.
  -> Mitigation: document it as a local seed only and require customer-specific expansion before production threshold selection.

- [Risk] More empty cases may lower Qdrant+BGE metrics.
  -> Mitigation: that is useful evidence; do not tune expected outcomes to preserve aggregate scores.
