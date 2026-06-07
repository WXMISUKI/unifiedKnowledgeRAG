## Why

The local provider already exposes RAG interfaces and MyPrivateAgent can call them. The current risk is not missing governance evidence; it is whether a real local business corpus can be used through the existing lightweight provider path without making the project heavier.

This change adds one small usability check that summarizes the existing local business corpus trial, in-process acceptance smoke, and optional live HTTP smoke into a single `go / review / blocked` result.

## What Changes

- Add a lightweight local RAG business corpus usability report.
- Reuse existing corpus trial and approved local corpus smoke services.
- Add a CLI that can run in local-only mode or include live HTTP checks against an already running provider.
- Keep the output compact and caller-oriented: source readiness, retrieve/answer usability, citation validity, and next action.

## Non-Goals

- Do not add another numbered phase evidence chain.
- Do not start the provider service.
- Do not change default `/api/rag/*` behavior.
- Do not change MyPrivateAgent behavior.
- Do not create source-to-agent binding.
- Do not run OCR, vector database promotion, GraphRAG, deployment, or production indexing.
- Do not add frontend UI.

## Impact

- Affected code:
  - new small service under `app/services/`
  - new script under `scripts/`
- Affected specs:
  - new `local-rag-business-corpus-usability-check`
- Affected tests:
  - focused service and CLI tests
