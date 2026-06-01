# Phase 3 Hybrid Runtime Promotion Decision Record

- Decision ID: `phase3-hybrid-runtime-promotion-decision-record-v1`
- Decision Date: `2026-06-01`
- Scope: `Phase 3 hybrid runtime promotion review`
- Decision: `keep_runtime_defaults`
- Status: `approved-for-current-slice`

## Current Runtime Defaults Snapshot

| Item | Current Value |
|---|---|
| Retrieval backend | `fixture` |
| Embedding provider | `mock` |
| Runtime score threshold | `0.01` |
| Graph query execution | `planned_not_implemented` |

## Evidence Basis

| Evidence | Current Status | Key Signal |
|---|---|---|
| `phase3-hybrid-runtime-promotion-decision-readiness` | `review` | `required_signals=14`, `open_gate_count=9` |
| `phase3-hybrid-runtime-promotion-decision-smoke` | `ready` | evidence-chain completeness checks pass |
| `phase3-retrieval-promotion-readiness` | `review` | promotion gates still open |
| `phase3-candidate-runtime-diagnostics` | `review` | runtime prerequisites still open |
| `phase3-candidate-latency-resource-diagnostics` | `review` | deployment/runtime posture remains review |
| `phase3-hybrid-fusion-threshold-calibration` | `review` | hybrid threshold semantics remain evaluation-only |
| `phase3-hybrid-cross-case-fp-fn-smoke` | `ready` | risk-case visibility checks pass |
| `phase3-aggregation-relation-negative-control-smoke` | `ready` | negative-control visibility checks pass |
| `phase6-qdrant-bge-private-network-promotion-readiness` | `review` | bridge promotion gates remain open |

## Open Promotion Gates

1. Customer-like benchmark still needs broader production-like corpus and additional false-positive/false-negative review.
2. Deployment-side live URL smoke and operations sign-off are not complete.
3. Runtime and latency diagnostics remain in `review` posture, not promotion-ready posture.
4. Private-network promotion review remains evidence-ready but not runtime-default approval.

## Decision Outcome

本轮 Phase 3 hybrid runtime promotion 结论是继续保持默认 runtime 不变，不进行 Qdrant/BGE-M3/hybrid 默认生产提升。当前切片目标已经达到：我们补齐了 contract、readiness、smoke 和最终 decision record，确保 promotion 决策可追踪、可复核、可归档。

## Next Promotion Preconditions

1. 补齐真实部署 URL 的 deployed smoke 与部署现场延迟/资源评估。
2. 基于更接近客户语料的 benchmark 补充跨场景 FP/FN 复核。
3. 对 hybrid 融合与阈值语义完成同口径复核，并形成稳定对比证据。
4. 仅在以上 gates 明确通过后，进入单独的 runtime default promotion change。
