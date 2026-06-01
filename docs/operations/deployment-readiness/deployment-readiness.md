# Deployment Readiness Report

- Report: `deployment-readiness-v1`
- Status: `review`
- Generated At: `2026-06-01T09:28:54.039215+00:00`
- Provider: `unifiedKnowledgeProvider`
- Contract: `knowledge-provider-contract-v1`

## Core Checks

| Check | Status | Details |
|---|---|---|
| Health | `ok` | RAG `ready`, Answer `ready`, Graph `planned` |
| Preflight | `bindable` | `6/6` checks passed |
| Contract Smoke | `passed` | `9/9` checks passed |

## Runtime Configuration

| Setting | Value |
|---|---|
| Retrieval Backend | `fixture` |
| Source Dir | `app\data\sources` |
| Index Dir | `app\data\indexes\llamaindex` |
| Embedding Provider | `mock` |
| Embedding Model | `mock-hash-v1` |
| Embedding Local Files Only | `False` |
| Qdrant URL | `http://localhost:6333` |
| Qdrant Collection | `knowledge_chunks` |
| Qdrant API Key Configured | `False` |
| Provider API Key Configured | `False` |
| Answer Composer | `deterministic` |

## Model Artifacts

| Field | Value |
|---|---|
| Status | `not_configured` |
| Model Path | `None` |
| Path Exists | `False` |
| Manifest Exists | `False` |

## Operation Notes

- This report is local readiness evidence; external control planes still own binding and governance decisions.
- Contract smoke evidence should be regenerated after configuration or dependency changes.
- Embedding provider is mock; use a real local or hosted embedding candidate before production retrieval promotion.
- Retrieval backend is not qdrant; vector-store deployment readiness remains a separate review.
- Provider API key is not configured; set PROVIDER_API_KEY before exposing /api endpoints outside trusted local development.
