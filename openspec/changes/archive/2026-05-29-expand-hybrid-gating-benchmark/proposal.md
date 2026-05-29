# Change: Expand Hybrid Gating Benchmark

## Why

The first hybrid gating candidate passed the local seed, but it only covered full exact identifiers. A production-facing strategy also needs evidence for partial identifiers, multi-identifier questions, and ambiguous same-prefix unsupported identifiers. The current containment check should be tightened so partial query identifiers do not pass merely because they are substrings of a longer evidence identifier.

## What

- Add expanded hybrid gating benchmark fixtures for supported and unsupported identifier-heavy queries.
- Tighten the exact identifier containment gate to compare extracted identifier sets instead of raw substring containment.
- Export expanded Qdrant+BGE-M3 hybrid gating evidence and document the result.

## Non-Goals

- Do not enable hybrid retrieval or gating as a runtime default.
- Do not add a production sparse model, reranker, or GraphRAG dependency.
- Do not change provider HTTP contracts.
