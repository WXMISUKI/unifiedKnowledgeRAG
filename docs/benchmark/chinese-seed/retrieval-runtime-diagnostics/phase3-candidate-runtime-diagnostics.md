# Phase 3 Candidate Runtime Diagnostics

- Report: `phase3-candidate-runtime-diagnostics-v1`
- Status: `review`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-04T06:27:59.176124+00:00`

## Summary

| Metric | Value |
|---|---|
| Total Checks | `6` |
| Ready Checks | `0` |
| Review Checks | `6` |
| Blocked Checks | `0` |
| Open Prerequisites | `["candidate_retrieval_backend", "candidate_embedding_provider", "local_embedding_artifact", "provider_api_guard", "phase3_readiness_export", "deployed_smoke_evidence"]` |

## Runtime Snapshot

| Setting | Value |
|---|---|
| Retrieval Backend | `fixture` |
| Embedding Provider | `mock` |
| Embedding Model | `mock-hash-v1` |
| Embedding Model Path | `None` |
| Provider API Key Configured | `False` |
| Qdrant URL | `http://localhost:6333` |
| Qdrant Collection | `knowledge_chunks` |

## Prerequisites

| Prerequisite | Status | Summary | Recommended Action |
|---|---|---|---|
| `candidate_retrieval_backend` | `review` | backend=fixture; candidate_backends=qdrant,qdrant-hybrid | `run_candidate_backend_benchmark_review` |
| `candidate_embedding_provider` | `review` | embedding_provider=mock; mock_provider_requires_promotion_evidence=true | `switch_to_candidate_embedding_for_evaluation` |
| `local_embedding_artifact` | `review` | artifact_status=not_configured; path_exists=False; manifest_exists=False | `validate_local_embedding_artifact` |
| `provider_api_guard` | `review` | provider_api_key_configured=False | `configure_provider_api_key_for_deployment_review` |
| `phase3_readiness_export` | `review` | status=review; decision=keep_runtime_defaults; open_gates=7 | `review_evidence_notes` |
| `deployed_smoke_evidence` | `review` | status=review; base_url=http://127.0.0.1:8020 | `review_evidence_notes` |

## Notes

- This report is local, read-only candidate runtime evidence for Phase 3 promotion review.
- It summarizes runtime-adjacent prerequisites but does not change retrieval defaults.
- Deployment-site latency and live URL evidence still require post-deployment validation.
