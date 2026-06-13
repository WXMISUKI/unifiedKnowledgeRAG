## Why

`unifiedKnowledgeRAG` is already usable as a lightweight external knowledge provider, but the next stage needs a clean closure that proves the running provider can be discovered, checked, and consumed by MyPrivateAgent without reopening provider feature expansion.

The current local run loop is `go`, while the deployed smoke still reports `review` because it surfaces the handoff bundle posture. This change closes the MyPrivateAgent provider-use loop by refreshing evidence, documenting the caller handoff, and cleaning stale OpenSpec state without changing runtime defaults.

## What Changes

- Add a focused MyPrivateAgent provider-use closure contract that defines the minimum evidence needed before MyPrivateAgent should treat the local provider as usable.
- Refresh provider-side live evidence for an already-running `http://127.0.0.1:8020` service:
  - local usable run loop
  - deployed provider smoke
  - provider handoff refresh / handoff bundle where possible
- Add or update a concise caller-facing runbook that states how MyPrivateAgent should enable and verify the provider.
- Resolve the stale empty active change `confirm-refund-query-mismatch-failure-class` by either documenting its non-action posture or removing it from the active work queue.
- Preserve lightweight boundaries:
  - no default runtime retrieval backend promotion
  - no GraphRAG execution
  - no source-to-agent binding creation
  - no MyPrivateAgent orchestration inside this provider
  - no query rewrite, rerank, hybrid retrieval, or parser expansion

## Capabilities

### New Capabilities
- `myprivateagent-provider-use-loop-closure`: Defines the provider-side evidence and documentation required to close the local MyPrivateAgent usage loop for `unifiedKnowledgeRAG`.

### Modified Capabilities
- `provider-workstream-rebaseline`: Clarifies that this closure is an allowed deployment/caller-use evidence refresh, not a new access-readiness chain or provider feature expansion.

## Impact

- Affected docs:
  - `docs/progress/provider-improvement-tracker.md`
  - `docs/progress/provider-phase-closure-summary.md`
  - new or updated integration runbook under `docs/integration/`
- Affected evidence artifacts:
  - `docs/local-run/local-usable-run-loop.*`
  - `docs/integration/deployed-provider-smoke/deployed-provider-smoke.*`
  - provider handoff evidence artifacts if regenerated successfully
- Affected OpenSpec state:
  - new closure spec under this change
  - stale active change cleanup for `confirm-refund-query-mismatch-failure-class`
- No API contract, runtime backend, dependency, deployment topology, or GraphRAG behavior changes are intended.
