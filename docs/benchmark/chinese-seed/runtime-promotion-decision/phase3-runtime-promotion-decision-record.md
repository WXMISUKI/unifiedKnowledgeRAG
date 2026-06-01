# Phase 3 Runtime Promotion Decision Record

- Decision ID: `phase3-runtime-promotion-decision-record-v1`
- Decision Date: `2026-06-01`
- Scope: `Phase 3 retrieval promotion review`
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
| `phase3-retrieval-promotion-readiness` | `review` | `open_gates=7` |
| `phase3-candidate-runtime-diagnostics` | `review` | runtime prerequisites still open |
| `phase3-candidate-latency-resource-diagnostics` | `review` | deployment/runtime posture is review |
| `phase3-hybrid-fusion-threshold-calibration` | `review` | `fusion=rrf`, `score_filter=disabled-for-rrf-fusion-score`, threshold semantics not promotion-ready |
| `phase3-hybrid-cross-case-fp-fn-smoke` | `ready` | coverage checks pass, but no direct runtime promotion implication |
| `phase3-aggregation-relation-negative-control-smoke` | `ready` | negative-control behavior visible, still candidate context |
| `deployment-readiness` | `review` | embedding/retrieval/provider key/model artifact gates open |

## Open Promotion Gates

1. Customer-like benchmark still needs broader production-like corpus and additional false-positive/false-negative复核。
2. Hybrid calibration remains evaluation-only because current evidence is RRF fusion with `score_filter` disabled, and dense threshold recommendation is not directly equivalent to runtime hybrid promotion.
3. Deployment-side latency/resource and live URL smoke evidence are still incomplete for production promotion.
4. Embedding model artifact and provider deployment configuration are not yet in ready posture.

## Decision Outcome

本轮 Phase 3 结论是继续保持默认 runtime 不变，不进行 Qdrant/BGE-M3/hybrid/aggregation/relation-aware grading 的默认生产提升。当前切片目标已达到：我们补齐了决策依据与证据引用，避免单点候选指标导致误提升。

## Next Promotion Preconditions

1. 引入更接近客户语料的 benchmark 与跨场景 FP/FN 复核结果。
2. 补齐部署现场 URL 的 smoke 证据、延迟与资源评估结果。
3. 在同一运行语义下完成 hybrid 融合与阈值校准复核，并形成可追踪对比。
4. 仅在以上 gate 明确通过后，进入下一轮 runtime promotion decision record。
