# Phase 3 Candidate Latency/Resource Diagnostics

- Report: `phase3-candidate-latency-resource-diagnostics-v1`
- Status: `review`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-03T03:41:22.295715+00:00`

## Summary

| Metric | Value |
|---|---|
| Total Signals | `6` |
| Ready Signals | `1` |
| Review Signals | `5` |
| Blocked Signals | `0` |
| Open Signal IDs | `["deployment_readiness_snapshot", "runtime_diagnostics_snapshot", "local_embedding_artifact", "provider_api_guard", "deployed_smoke_evidence"]` |

## Latency Profile

| Metric | Value |
|---|---|
| Backend | `fixture` |
| Total Cases | `32` |
| Hit Rate | `0.9062` |
| Citation Match Rate | `0.9062` |
| Empty Handling Rate | `0.75` |
| Average Latency (ms) | `0.2368` |
| Median Latency (ms) | `0.239` |
| P95 Latency (ms) | `0.362` |
| Max Latency (ms) | `0.388` |
| Slowest Case | `logistics-lost-package-cross-team` |
| Slowest Case Latency (ms) | `0.388` |

## Resource Posture

| Setting | Value |
|---|---|
| Deployment Readiness Status | `review` |
| Runtime Diagnostics Status | `review` |
| Retrieval Backend | `fixture` |
| Embedding Provider | `mock` |
| Embedding Model | `mock-hash-v1` |
| Embedding Model Path | `None` |
| Model Artifact Status | `not_configured` |
| Provider API Key Configured | `False` |
| Qdrant API Key Configured | `False` |
| Qdrant URL | `http://localhost:6333` |
| Qdrant Collection | `knowledge_chunks` |

## Signals

| Signal | Status | Summary | Recommended Action |
|---|---|---|---|
| `benchmark_latency_profile` | `ready` | backend=fixture; total_cases=32; average_latency_ms=0.2368; median_latency_ms=0.2390; p95_latency_ms=0.3620 | `no_action_required` |
| `deployment_readiness_snapshot` | `review` | status=review; rag_backend=fixture; embedding_provider=mock; model_artifacts_status=not_configured | `review_deployment_readiness_notes` |
| `runtime_diagnostics_snapshot` | `review` | status=review; decision=keep_runtime_defaults; open_prerequisites=6 | `review_runtime_diagnostics_notes` |
| `local_embedding_artifact` | `review` | status=not_configured; path_exists=False; manifest_exists=False | `validate_local_embedding_artifact` |
| `provider_api_guard` | `review` | provider_api_key_configured=False | `configure_provider_api_key_for_deployment_review` |
| `deployed_smoke_evidence` | `review` | status=review; base_url=http://127.0.0.1:8020 | `review_evidence_notes` |

## Notes

- This report is local, read-only candidate latency/resource evidence for Phase 3 promotion review.
- It combines benchmark latency profile evidence with deployment and runtime posture snapshots.
- Latency values are environment-sensitive and should be compared against matching deployment conditions.
