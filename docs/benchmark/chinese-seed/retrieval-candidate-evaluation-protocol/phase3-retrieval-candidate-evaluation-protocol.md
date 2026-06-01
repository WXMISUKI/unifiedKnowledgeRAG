# Phase 3 Retrieval Candidate Evaluation Protocol

## Scope

This protocol standardizes Phase 3 retrieval candidate review for local evidence workflows. It defines what must be reviewed before any runtime promotion proposal is allowed.

This is a read-only governance artifact:

- It does not change runtime defaults.
- It does not approve candidate promotion.
- It does not change provider HTTP contracts.

## Current Position

- Current decision remains `keep_runtime_defaults`.
- Current open gate count remains `7`.
- Candidate families under review:
  - `qdrant_vector_store`
  - `bge_m3_local_embedding`
  - `hybrid_retrieval`
  - `hybrid_gating`
  - `multi_chunk_aggregation`
  - `relation_aware_grading`
  - `deployed_smoke`

Reference artifact:

- `docs/benchmark/chinese-seed/retrieval-promotion-readiness/phase3-retrieval-promotion-readiness.json`

## Gate Matrix

| Gate | Evidence focus | Required evidence class | Review decision rule |
|---|---|---|---|
| Qdrant vector store | retrieval quality + deployment viability | customer-like benchmark, FP/FN review, latency/deploy diagnostics | Keep opt-in unless quality and deployment evidence both pass |
| BGE-M3 local embedding | local model readiness + deployment viability | artifact diagnostics, private-network validation, quality/latency comparison | Keep opt-in unless artifact and deployment evidence both pass |
| Hybrid retrieval | recall gain with precision control | customer-like benchmark expansion, FP/FN cross-case review, score/fusion diagnostics | Keep non-default unless recall and precision both pass |
| Hybrid gating | identifier precision with false-negative control | alias/noisy-id coverage, split-chunk FN review, cross-case controls | Keep evaluation-only unless FN and FP behavior are both acceptable |
| Multi-chunk aggregation | split-chunk recovery without over-broad joins | same-document negative controls, relation-oriented controls, citation granularity checks | Keep review-only unless positive recovery and negative controls both pass |
| Relation-aware grading | relation-sensitive grading signal quality | broader relation fixtures, unsupported-relation controls, mismatch diagnostics | Keep evaluation-only unless relation coverage is broad and stable |
| Deployed smoke | live endpoint integration evidence | deployed URL smoke report after deployment | Do not block local iteration; required before deployment promotion |

## Required Evidence Classes

1. Customer-like benchmark coverage:
   Include policy nuance, identifier noise, cross-domain expected-empty traps, and split-chunk relationship cases.
2. Cross-case FP/FN review:
   Validate false-positive and false-negative behavior at case level, not only aggregate hit rate.
3. Runtime diagnostics:
   Record embedding provider/model path state, retrieval backend state, key configuration visibility, and model artifact state.
4. Deployment viability:
   Record latency and deployment-site evidence separately from local fixture-only evidence.

## Promotion Guardrails

Promotion proposal is allowed only when all of the following are true for the target gate family:

1. Required evidence classes are present and current.
2. Cross-case FP/FN evidence is reviewable and acceptable.
3. Runtime diagnostics do not show unresolved prerequisite gaps.
4. Deployment-side evidence exists when deployment behavior is part of the gate.

If any condition remains open, decision stays `keep_runtime_defaults`.

## Non-Goals

- Selecting final production embedding vendor.
- Switching default retrieval backend to Qdrant.
- Enabling hybrid retrieval as runtime default.
- Enabling GraphRAG query execution.
- Expanding parser stack to PDF/Word/Excel/OCR/table.
