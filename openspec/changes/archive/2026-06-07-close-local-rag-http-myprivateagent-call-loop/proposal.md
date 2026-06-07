## Why

The local business corpus is now usable inside the provider and the provider is reachable on live HTTP. The next useful closure is to prove the same source can be called from MyPrivateAgent through the real local HTTP contract.

This change closes the local RAG access loop without adding another feature phase: provider HTTP usability plus MyPrivateAgent caller-side corpus trial must both be `go`.

## What Changes

- Add a compact closure report that consumes:
  - provider-side local RAG business corpus usability report with live HTTP enabled
  - MyPrivateAgent caller-side local knowledge provider corpus trial report
- Add a CLI to export the closure result.
- Record `go / review / blocked` and next action.

## Non-Goals

- Do not change RAG APIs.
- Do not change MyPrivateAgent default `/api/chat`.
- Do not create source-to-agent binding.
- Do not start either service.
- Do not add OCR, GraphRAG, Qdrant/BGE promotion, deployment, or frontend UI.
- Do not continue a numbered readiness phase chain.

## Impact

- Affected code:
  - one small report service
  - one small export script
- Affected docs:
  - generated local-run closure report
- Affected tests:
  - focused report decision tests
