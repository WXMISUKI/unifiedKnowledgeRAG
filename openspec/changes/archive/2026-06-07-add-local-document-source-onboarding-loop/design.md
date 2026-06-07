## Context

The project has completed the useful pieces of the local business corpus path:

1. PDF-derived markdown trial creates a markdown corpus artifact.
2. Local business corpus trial validates markdown chunkability and query evidence.
3. Caller handoff packages the trial for review.
4. Approved local source registration materializes the markdown into provider sources.
5. Acceptance smoke validates catalog, document manifest, retrieve, answer, citation allowlist, and negative-control behavior.

The gap is operational friction. A developer adding a new local business document should have one command that runs the safe sequence and summarizes the result.

## Goals

- Provide one explicit local onboarding command for markdown business documents.
- Reuse existing services instead of duplicating retrieval, registration, or smoke logic.
- Keep every step report visible for debugging.
- Give a final go/review/blocked decision and recommended next action.

## Non-Goals

- Do not parse raw PDFs as a supported provider ingestion format.
- Do not start PaddleOCR, PP-Structure, or any OCR service.
- Do not create formal ingestion jobs or persist index lifecycle state beyond existing approved local source registration.
- Do not create source-to-agent bindings.
- Do not call MyPrivateAgent.
- Do not promote Qdrant, BGE, hybrid retrieval, reranker, or GraphRAG.
- Do not change `/api/rag/*` runtime contracts.

## Pipeline

```text
markdown file
  -> local business corpus trial
  -> local corpus caller handoff
  -> approved local source registration
  -> approved local corpus acceptance smoke
  -> onboarding summary
```

## Decision Rules

- `blocked` if markdown trial, handoff, registration, or acceptance smoke blocks.
- `review` if any step returns review but no step blocks.
- `go` if corpus trial is `go`, handoff is `ready_for_caller_review`, registration is `registered`, and acceptance smoke is `go`.

## Output

The onboarding report should include:

- source id, title, query, markdown path
- final decision and reason code
- per-step status, reason code, and artifact pointers
- registered materialized source path when available
- acceptance case counts
- non-goals and recommended actions

## Risk

The script may overwrite an existing approved local source with the same source id because the existing registration service upserts the registry and materialized markdown. That behavior is acceptable for local developer iteration, but the report must make it visible as local reversible registration rather than production ingestion.
