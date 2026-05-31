# Phase 3 Retrieval Promotion Gap Matrix

- Report: `phase3-retrieval-promotion-gap-matrix-v1`
- Generated At: `2026-05-31`
- Status: `review`
- Scope: `Qdrant`, `BGE-M3`, `hybrid retrieval`, `aggregation`, `relation-aware grading`

## Summary

The current Phase 3 evidence is strong enough to review candidate quality, but not strong enough to promote any retrieval default. The report below keeps the decision surface compact and explicit.

## Gap Matrix

| Gate | Current Evidence | Current Status | Open Gap | Promotion Position |
|---|---|---|---|---|
| Qdrant vector store | `docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json`, `qdrant-bge-m3-threshold-sweep.json`, `qdrant-bge-m3-threshold-recommendation.json`, `qdrant-bge-m3-chunking-comparison.json` | `candidate` | Customer-like corpus benchmark, deployment latency, backup/restore review, private-network deployment evidence | Keep opt-in; do not change runtime default |
| BGE-M3 local embedding | `docs/benchmark/chinese-seed/embedding-candidates/bge-m3-local-candidate.json`, model artifact download workflow | `review_required` | Artifact validation, private-network deployment, quality/latency comparison, deployment readiness evidence | Keep opt-in; do not change runtime default |
| Hybrid retrieval | `docs/benchmark/chinese-seed/exact-term-candidates/qdrant-bge-m3-hybrid-exact-term-smoke.json`, `docs/benchmark/chinese-seed/hybrid-empty-stress/qdrant-bge-m3-hybrid-empty-stress.json` | `candidate` | Broader customer-like false-positive and false-negative review, score/fusion calibration, deploy review | Not default |
| Hybrid gating | `docs/benchmark/chinese-seed/hybrid-gating-candidates/qdrant-bge-m3-hybrid-exact-identifier-gate.json`, `docs/benchmark/chinese-seed/noisy-identifier-gating-candidates/qdrant-bge-m3-hybrid-alias-identifier-gate.json`, `docs/benchmark/chinese-seed/split-chunk-gating-candidates/qdrant-bge-m3-hybrid-exact-identifier-gate.json` | `candidate` | Broader alias/noisy identifier coverage, split-chunk false-negative review, gating policy ownership | Evaluation only |
| Multi-chunk aggregation | `docs/benchmark/chinese-seed/multi-chunk-aggregation-candidates/qdrant-bge-m3-hybrid-multi-chunk-aggregation.json`, `docs/benchmark/chinese-seed/multi-chunk-aggregation-negative-controls/qdrant-bge-m3-hybrid-multi-chunk-aggregation.json`, `docs/benchmark/chinese-seed/relation-aware-aggregation-grading/relation-aware-aggregation-grading.json` | `review` | More relation-heavy customer-like cases, noisy top-k review, latency and citation granularity review | Keep review-only |
| Relation-aware grading | `docs/benchmark/chinese-seed/relation-aware-aggregation-grading/relation-aware-aggregation-grading.json` | `candidate` | Broader relation fixture coverage and production semantics review | Evaluation only |
| Deployed smoke | `docs/integration/deployed-provider-smoke/` | `optional` | Live deployed URL evidence is missing in local development | Run after deployment; do not block local iteration |

## Open Gates

- Customer-like benchmark coverage is still the most important missing review input for production promotion.
- FP/FN review is useful, but it is still review evidence, not approval.
- Deployed smoke remains optional until there is a real deployed base URL to test.

## Decision

Keep `runtime defaults` unchanged until a later evidence-backed slice closes the relevant gates.
