## Context

The benchmark harness currently evaluates three cases: one refund policy case, one logistics FAQ case, and one empty retrieval case. That is enough for a smoke test but not enough to support infrastructure decisions. A useful next step is to add representative case categories while staying within the current local fixture corpus.

## Goals / Non-Goals

**Goals:**

- Broaden local benchmark coverage.
- Add category and difficulty metadata.
- Report category-level rates.
- Keep all cases compatible with the current fixture backend.

**Non-Goals:**

- No new production corpus ingestion.
- No external evaluation library.
- No new embedding/vector/reranker dependency.
- No pass/fail thresholds for production decisions yet.

## Decisions

1. Add `category` and `difficulty` to cases.

   These fields let reports answer whether a backend fails on paraphrase, policy, FAQ, evidence, or empty retrieval cases.

2. Keep expected citation as the primary correctness target.

   Citation match is more useful than answer text matching because the provider contract is evidence-first.

3. Keep the current fixture backend unchanged.

   If the expanded cases expose weakness, that should become benchmark evidence rather than a silent retrieval implementation change.

## Risks / Trade-offs

- More cases can reveal imperfect fixture scoring -> acceptable; this harness is for visibility.
- Category-level rates are coarse with small samples -> good enough until real corpus cases are added.
- Manual cases can be biased -> future work should include real usage logs or domain-authored cases.

## Migration Plan

1. Extend case schema.
2. Expand case fixture data.
3. Add category summaries.
4. Add focused tests and docs.
5. Validate and archive.
