## Why

MyPrivateAgent is ready to move from provider evidence review into a real repo-side trial, but the provider needs one final lightweight readout that says whether the document RAG access path is ready, reviewable, or blocked. This avoids extending the Phase 10-18 evidence chain while giving callers a single closure artifact for trial dispatch.

## What Changes

- Add a Phase 24 provider-side document RAG readiness closure report with a `ready`, `review`, or `blocked` status and a `go`, `review`, or `blocked` decision.
- Reuse existing provider contract smoke, Phase 10/11 access primitives, Phase 16 minimal access loop, and provider handoff refresh evidence instead of creating new platform gates.
- Add a focused export script and tests for the closure report.
- Update the roadmap/progress documentation with the Phase 24 outcome and next caller-side action.
- Keep runtime defaults, retrieval backend selection, source binding, GraphRAG execution, and caller policy ownership unchanged.

## Capabilities

### New Capabilities
- `myprivateagent-document-rag-trial-readiness`: Provider-owned read-only closure report for MyPrivateAgent document RAG repo-side trial readiness.

### Modified Capabilities

## Impact

- Affected code: new Phase 24 service, export script, and focused tests.
- Affected docs: provider roadmap/progress tracker and generated Phase 24 readiness artifacts.
- Affected APIs: none.
- Dependencies: none.
- Systems: `unifiedKnowledgeRAG` remains the lightweight knowledge data-plane provider; MyPrivateAgent still owns trial execution, source-to-agent binding, audit policy, and final answer behavior.
