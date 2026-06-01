# Phase 6 BGE-M3 Artifact Readiness

- Report: `phase6-bge-m3-artifact-readiness-v1`
- Status: `review`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-01T08:16:02.465882+00:00`

## Summary

| Metric | Value |
|---|---|
| Total Signals | `6` |
| Ready Signals | `1` |
| Review Signals | `5` |
| Blocked Signals | `0` |
| Open Signal IDs | `["embedding_provider_candidate", "model_path_and_manifest_presence", "required_file_inventory", "checksum_coverage", "private_network_copy_posture"]` |

## Artifact Snapshot

| Field | Value |
|---|---|
| Embedding Provider | `mock` |
| Embedding Model | `mock-hash-v1` |
| Embedding Local Files Only | `False` |
| Model Path | `None` |
| Path Exists | `False` |
| Manifest Exists | `False` |
| Required Files Present | `0/0` |
| Weight Files Count | `0` |
| Checksum Coverage | `0/0` |
| Checksum Algorithm | `unknown` |
| Deployment Readiness Status | `review` |

## Signals

| Signal | Status | Summary | Recommended Action |
|---|---|---|---|
| `embedding_provider_candidate` | `review` | embedding_provider=mock | `set_embedding_provider_to_bge_m3_local_for_candidate_review` |
| `model_path_and_manifest_presence` | `review` | path_exists=False; manifest_exists=False | `configure_embedding_model_path_and_manifest` |
| `required_file_inventory` | `review` | required_files=0/0; weight_files=0 | `rebuild_or_copy_complete_bge_m3_artifact` |
| `checksum_coverage` | `review` | checksum_coverage=0/0; algorithm=unknown | `regenerate_manifest_with_sha256_checksums` |
| `deployment_readiness_linkage` | `ready` | deployment_readiness_status=review | `no_action_required` |
| `private_network_copy_posture` | `review` | runtime_local_files_only=False; manifest_local_files_only=False | `enable_local_files_only_for_private_network_artifacts` |

## Notes

- This report is local, read-only artifact readiness evidence for Phase 6 deployment review.
- It supports Phase 3 promotion review as a bridge artifact but does not promote embedding defaults.
- Use matching artifact directory and manifest when copying models into private-network deployments.
