# Deployment Readiness Runbook

Use this runbook when you want to move from the current `review` state toward a deployment candidate without changing runtime defaults.

## 1. Review The Current State

Start here:

- [operator-guide.md](operator-guide.md)
- [config-reference.md](config-reference.md)
- `docs/operations/deployment-readiness/deployment-readiness.json`

Confirm the current blockers:

- `embedding_provider` is `mock`
- `rag_retrieval_backend` is `fixture`
- `model_artifacts` are not configured
- `PROVIDER_API_KEY` is not configured
- `deployed_provider_smoke` is missing unless you already have a live URL

## 2. Choose The Target Mode

Decide which deployment path you are preparing:

- Local development
- Local compose
- Private deployment candidate
- Live deployment check

Use [config-reference.md](config-reference.md) to map the mode to concrete settings.

## 3. Apply Configuration

Update the environment and mounts that match the target mode:

- `.env` or environment variables
- `./app/data/sources`
- `./app/data/indexes`
- `./models` when using a local embedding model

Do not change runtime defaults unless the deployment target explicitly requires it.

## 4. Refresh Evidence

After changing configuration or mounted state, rerun:

```powershell
python scripts/export_deployment_readiness.py
python scripts/export_reindex_readiness.py
python scripts/export_provider_handoff_refresh.py
```

Treat the refreshed outputs as the current source of truth.

## 5. Recheck The Result

Reopen the generated evidence and verify:

- `deployment-readiness.json`
- `reindex-readiness.json`
- `provider-handoff-refresh.json`

You want to see whether the state remains `review`, moves to `ready`, or stays `blocked` for a specific reason that still needs work.

## 6. Run Deployed Smoke Only When Live

If there is a real provider base URL, run:

```powershell
python scripts/export_deployed_provider_smoke.py --base-url http://127.0.0.1:8020
```

Use the resulting evidence to confirm reachability and live binding-review surfaces.

## 7. Stop At The Boundary

Stop here if the remaining work would require:

- promotion of Qdrant, BGE-M3, or hybrid retrieval to runtime default
- GraphRAG execution promotion
- deployment automation or governance ownership changes

Those are separate evidence-backed slices, not this runbook.

## 8. Keep It Current

When runtime configuration or source/index state changes, rerun:

```powershell
python scripts/export_provider_handoff_refresh.py
```

This runbook is current only when the evidence chain is current.
