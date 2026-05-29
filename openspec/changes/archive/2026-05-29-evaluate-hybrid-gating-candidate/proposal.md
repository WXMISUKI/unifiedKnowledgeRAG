# Change: Evaluate Hybrid Gating Candidate

## Why

The Qdrant+BGE-M3 dense+sparse hybrid candidate fixed the exact-term identifier recall gap, but the hybrid empty-stress fixture showed that unsupported identifier-like questions can still return related-looking evidence. This blocks runtime hybrid promotion.

## What

- Add an evaluation-only exact identifier containment gate candidate for hybrid retrieval evidence.
- Export a combined report over exact-term and hybrid empty-stress fixtures so recall and false-positive behavior can be reviewed together.
- Document the result as local seed evidence, not production approval.

## Non-Goals

- Do not change runtime retrieval defaults.
- Do not add public HTTP APIs.
- Do not choose a production sparse model, reranker, or GraphRAG storage dependency.
