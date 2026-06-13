# MyPrivateAgent Provider Use Loop

## Purpose

This runbook closes the local use loop for `unifiedKnowledgeRAG` as a lightweight external knowledge provider for MyPrivateAgent.

It proves local caller usability. It does not promote production deployment, retrieval backend defaults, GraphRAG execution, source-to-agent binding, or MyPrivateAgent runtime behavior.

## Current Local Evidence

Latest refreshed provider-side evidence:

- Local usable run-loop: `docs/local-run/local-usable-run-loop.md`
- Deployed provider smoke: `docs/integration/deployed-provider-smoke/deployed-provider-smoke.md`
- Provider handoff refresh: `docs/integration/provider-handoff-refresh/provider-handoff-refresh.md`

Local use is allowed when:

- `/live`, `/ready`, and `/health` are ready.
- Provider manifest reports `provider_id=unifiedKnowledgeProvider`.
- Provider preflight is bindable.
- Source binding summary is ready.
- Local usable run-loop returns `decision=go`.

`deployed-provider-smoke` or handoff may still report `review` because deployment readiness, model artifacts, API key posture, Qdrant/BGE/pgvector candidates, or other production gates remain review-level. That review state is not a blocker for local MyPrivateAgent use when the primitive access checks are ready.

## Provider Startup

Start the provider from this repository:

```powershell
conda activate GRAPHRAG
uvicorn app.main:app --reload --port 8020
```

Confirm readiness:

```powershell
Invoke-RestMethod http://127.0.0.1:8020/health
Invoke-RestMethod http://127.0.0.1:8020/api/provider/preflight
Invoke-RestMethod http://127.0.0.1:8020/api/provider/source-bindings
```

Refresh provider-side evidence:

```powershell
python scripts/export_local_usable_run_loop.py --base-url http://127.0.0.1:8020
python scripts/export_deployed_provider_smoke.py --base-url http://127.0.0.1:8020
python scripts/export_provider_handoff_refresh.py
```

## MyPrivateAgent Enablement

In `D:\AI\AIcode\MyPrivateAgent`, enable the external knowledge provider with caller-owned configuration:

```powershell
$env:ENABLE_KNOWLEDGE_CAPABILITY_PROVIDER="true"
$env:KNOWLEDGE_CAPABILITY_PROVIDER_BASE_URL="http://127.0.0.1:8020"
```

Then start or restart MyPrivateAgent so its capability registry can include:

- `knowledge.rag.retrieve`
- `knowledge.graph.query`

Document RAG retrieval is the usable path for this closure. Graph query remains a planned boundary and must stay separately gated.

## Caller Verification

On the MyPrivateAgent side, verify the provider through its existing caller smoke or explicit local trial path. The provider-side expected result is:

- MyPrivateAgent discovers the provider capability catalog.
- `knowledge.rag.retrieve` can call `POST /api/rag/retrieve`.
- Returned evidence includes documents, citations, and `metadata.evidence_pack`.
- MyPrivateAgent keeps default chat retrieval injection disabled unless a separate caller-side change explicitly promotes it.

## Boundaries

This closure does not do any of the following:

- Create source-to-agent bindings.
- Write MyPrivateAgent `.env` or runtime config.
- Enable default `/api/chat` retrieval injection.
- Promote Qdrant, pgvector, BGE-M3, hybrid search, rerank, or query rewrite.
- Execute GraphRAG.
- Own final answer policy, audit, approval, permissions, heartbeat governance, or control-plane registration.

## Reopen Rules

After this closure, provider-side implementation should reopen only for a concrete trigger:

- `real_caller_feedback_trigger`
- `provider_owned_gap_trigger`
- `repeated_cross_source_failure_class_trigger`
- `runtime_strategy_evaluation_trigger`
- deployment owner request for a real environment

Without one of these triggers, keep the provider baseline stable and use MyPrivateAgent as the place to continue caller-side integration.
