# Deployment Configuration Reference

This page maps the current deployment readiness evidence to the actual runtime configuration surface. It is a reference, not a policy document.

## Canonical Sources

- `.env.example`
- `docker-compose.example.yml`
- `docs/operations/deployment-readiness/deployment-readiness.json`
- `docs/operations/deployment-readiness/operator-guide.md`

## Environment Variables

| Variable | Default / Example | Purpose |
|---|---|---|
| `PROVIDER_API_KEY` | `replace-with-random-token` | Optional component access token for `/api/*` |
| `RAG_RETRIEVAL_BACKEND` | `fixture` | Retrieval backend selection |
| `RAG_SOURCE_DIR` | `app/data/sources` or `/app/app/data/sources` | Mounted source documents |
| `RAG_INDEX_DIR` | `app/data/indexes/llamaindex` or `/app/app/data/indexes/llamaindex` | Persistent index state |
| `RAG_SCORE_THRESHOLD` | `0.01` | Retrieval score threshold |
| `EMBEDDING_PROVIDER` | `mock` | Embedding adapter selection |
| `EMBEDDING_MODEL` | `mock-hash-v1` | Embedding model label |
| `EMBEDDING_MODEL_PATH` | optional | Local embedding model directory |
| `EMBEDDING_VECTOR_SIZE` | optional | Vector size override |
| `EMBEDDING_HF_ENDPOINT` | optional | Hosted embedding endpoint when used |
| `EMBEDDING_LOCAL_FILES_ONLY` | `false` in code, `true` in compose examples | Offline model resolution preference |
| `BGE_M3_USE_FP16` | `true` | BGE-M3 local inference flag |
| `BGE_M3_BATCH_SIZE` | `12` | BGE-M3 local inference batch size |
| `BGE_M3_MAX_LENGTH` | `8192` | BGE-M3 local inference max length |
| `RAG_ANSWER_MIN_EVIDENCE_COUNT` | `1` | Minimum evidence required for answer generation |
| `RAG_ANSWER_MIN_EVIDENCE_SCORE` | `0.0` | Minimum evidence score threshold |
| `RAG_ANSWER_COMPOSER` | `deterministic` | Answer composer mode |
| `RAG_ANSWER_COMPOSER_MODEL` | `deterministic-extractive-v1` | Composer model label |
| `QDRANT_URL` | `http://localhost:6333` | Vector store URL |
| `QDRANT_API_KEY` | optional | Qdrant API token |
| `QDRANT_COLLECTION` | `knowledge_chunks` | Qdrant collection name |
| `QDRANT_VECTOR_NAME` | `text-dense` | Qdrant vector slot |
| `QDRANT_VECTOR_SIZE` | `1024` | Qdrant vector size |

## Recommended Modes

| Mode | Suggested Values | When To Use |
|---|---|---|
| Local development | `RAG_RETRIEVAL_BACKEND=fixture`, `EMBEDDING_PROVIDER=mock`, `PROVIDER_API_KEY` unset | Fast iteration and evidence review |
| Local compose | `.env.example` values with mounted `./app/data`, `./models` | Reproduce the bundled deployment profile |
| Private deployment candidate | Real embedding candidate, configured model path, explicit `PROVIDER_API_KEY` | Pre-production deployment planning |
| Live deployment check | Existing deployment inputs plus deployed smoke base URL | Verify an already-running provider |

## Mounts And Paths

| Path | Role |
|---|---|
| `./app/data/sources:/app/app/data/sources:ro` | Source documents |
| `./app/data/indexes:/app/app/data/indexes` | Persistent index state |
| `./models:/models:ro` | Optional local model artifacts |

## Evidence Commands

Use these commands to refresh evidence after config changes:

```powershell
python scripts/export_deployment_readiness.py
python scripts/export_reindex_readiness.py
python scripts/export_provider_handoff_refresh.py
```

Use deployed smoke only when a live URL exists:

```powershell
python scripts/export_deployed_provider_smoke.py --base-url http://127.0.0.1:8020
```

## Reading The Evidence

- `deployment-readiness.json` explains why the current state is `review`, `ready`, or `blocked`.
- `reindex-readiness.json` is the pre-deployment source freshness check.
- `provider-handoff-refresh.json` is the maintenance command output that keeps the evidence chain current.

## Boundary Notes

- This reference does not promote fixture, Qdrant, mock, or hybrid candidates to runtime defaults.
- This reference does not own registration, heartbeat governance, audit policy, or source-to-agent binding.
- This reference should be updated whenever `app/config.py` or the deployment example files change.
